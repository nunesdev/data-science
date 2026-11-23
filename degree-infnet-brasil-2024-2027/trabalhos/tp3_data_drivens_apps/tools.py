"""
Ferramentas do agente ReAct para clima (Open-Meteo) e alertas/notícias (DuckDuckGo).
"""

from __future__ import annotations

import json
from typing import Any

import requests
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

_ddg_search: DuckDuckGoSearchRun | None = None


def _get_ddg_search() -> DuckDuckGoSearchRun:
  """Cria o buscador DuckDuckGo sob demanda (requer pacote `ddgs` instalado)."""
  global _ddg_search
  if _ddg_search is None:
    _ddg_search = DuckDuckGoSearchRun()
  return _ddg_search

OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 20


@tool
def buscar_clima(cidade: str) -> str:
  """
  Consulta condições climáticas atuais de uma cidade no Sul do Brasil (ou outra localidade)
  usando a API gratuita Open-Meteo, sem necessidade de chave de API.

  Fluxo interno:
  1. Geocoding: resolve o nome da cidade em latitude/longitude.
  2. Forecast: obtém temperatura atual (2 m) e precipitação no momento.

  Use esta ferramenta quando o usuário perguntar sobre chuva, temperatura, tempo agora,
  previsão imediata ou condições meteorológicas de uma cidade específica (ex.: Porto Alegre,
  Florianópolis, Curitiba).

  Args:
      cidade: Nome da cidade a consultar (pode incluir estado ou país, ex. 'Pelotas, Brasil').

  Returns:
      Texto em português com localização encontrada, coordenadas, temperatura em °C e
      precipitação em mm. Em caso de falha, retorna mensagem de erro descritiva.
  """
  cidade = (cidade or "").strip()
  if not cidade:
    return "Erro: informe o nome de uma cidade válida para consulta climática."

  try:
    geo_params: dict[str, Any] = {
      "name": cidade,
      "count": 1,
      "language": "pt",
      "format": "json",
    }
    geo_response = requests.get(
      OPEN_METEO_GEOCODING_URL,
      params=geo_params,
      timeout=REQUEST_TIMEOUT_SECONDS,
    )
    geo_response.raise_for_status()
    geo_data = geo_response.json()

    results = geo_data.get("results") or []
    if not results:
      return (
        f"Não foi possível localizar a cidade '{cidade}' no serviço de geocodificação. "
        "Tente incluir o estado ou o país (ex.: 'Lajeado, RS, Brasil')."
      )

    place = results[0]
    lat = place.get("latitude")
    lon = place.get("longitude")
    name = place.get("name", cidade)
    admin1 = place.get("admin1", "")
    country = place.get("country", "")

    if lat is None or lon is None:
      return f"Erro: coordenadas indisponíveis para '{name}'."

    forecast_params: dict[str, Any] = {
      "latitude": lat,
      "longitude": lon,
      "current": "temperature_2m,precipitation",
      "timezone": "America/Sao_Paulo",
    }
    forecast_response = requests.get(
      OPEN_METEO_FORECAST_URL,
      params=forecast_params,
      timeout=REQUEST_TIMEOUT_SECONDS,
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    current = forecast_data.get("current") or {}
    temp = current.get("temperature_2m")
    precip = current.get("precipitation")
    time_iso = current.get("time", "N/A")

    local_label = ", ".join(p for p in [name, admin1, country] if p)

    lines = [
      f"Local: {local_label}",
      f"Coordenadas: latitude {lat}, longitude {lon}",
      f"Horário da medição (America/Sao_Paulo): {time_iso}",
    ]
    if temp is not None:
      lines.append(f"Temperatura atual: {temp} °C")
    else:
      lines.append("Temperatura atual: dado indisponível")
    if precip is not None:
      lines.append(f"Precipitação atual: {precip} mm")
      if float(precip) > 0:
        lines.append("Observação: há registro de precipitação no momento da consulta.")
      else:
        lines.append("Observação: sem precipitação registrada no momento da consulta.")
    else:
      lines.append("Precipitação atual: dado indisponível")

    return "\n".join(lines)

  except requests.Timeout:
    return (
      f"Timeout ao consultar o clima para '{cidade}'. "
      "Verifique sua conexão e tente novamente."
    )
  except requests.RequestException as exc:
    return f"Erro de rede ao consultar Open-Meteo para '{cidade}': {exc}"
  except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
    return f"Erro ao interpretar resposta da API de clima para '{cidade}': {exc}"
  except Exception as exc:  # noqa: BLE001 — ferramenta deve sempre retornar string ao agente
    return f"Erro inesperado em buscar_clima para '{cidade}': {exc}"


@tool
def buscar_alertas_noticias(query: str) -> str:
  """
  Busca na web (via DuckDuckGo) alertas da Defesa Civil, avisos de enchente, inundação,
  deslizamentos e notícias recentes relacionadas a eventos climáticos extremos na região
  ou cidade indicada na consulta.

  Use esta ferramenta quando precisar cruzar o clima com o contexto social e de risco:
  evacuações, rodovias interditadas, nível dos rios, comunicados oficiais ou cobertura
  jornalística sobre alagamentos e El Niño no Sul do Brasil.

  Args:
      query: Termos de busca. Inclua cidade/estado e palavras como 'defesa civil',
             'enchente', 'alerta', 'inundação', 'El Niño' (ex.:
             'Porto Alegre defesa civil alerta enchente').

  Returns:
      Trecho de resultados de busca em texto plano. Se a busca falhar, retorna mensagem
      de erro para o agente continuar o raciocínio.
  """
  query = (query or "").strip()
  if not query:
    return "Erro: informe uma consulta de busca (cidade + tema, ex. alerta enchente)."

  try:
    # Enriquece a query para focar em alertas oficiais e enchentes no contexto brasileiro.
    enriched = (
      f"{query} defesa civil alerta enchente inundação Sul Brasil "
      f"El Niño notícias"
    )
    resultado = _get_ddg_search().run(enriched)
    if not resultado or not str(resultado).strip():
      return (
        f"Nenhum resultado relevante retornado para '{query}'. "
        "Sugira ao usuário reformular com nome da cidade e 'defesa civil' ou 'enchente'."
      )
    return str(resultado).strip()

  except Exception as exc:  # noqa: BLE001 — DuckDuckGo pode falhar por rate limit ou rede
    return (
      f"Erro ao buscar alertas e notícias para '{query}' via DuckDuckGo: {exc}. "
      "O agente pode responder com base apenas nos dados climáticos, se disponíveis."
    )


def get_tools() -> list:
  """Retorna a lista de ferramentas registradas para o agente."""
  return [buscar_clima, buscar_alertas_noticias]