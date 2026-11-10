"""Configurações centralizadas — facilita troca de modelos em ambiente acadêmico."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    # GPT-2 pequeno: adequado para demonstração local sem GPU obrigatória.
    GPT2_MODEL_ID: str = "gpt2"
    # Modelo MarianMT oficial Helsinki-NLP para EN→FR.
    EN_FR_MODEL_ID: str = "Helsinki-NLP/opus-mt-en-fr"


settings = ModelConfig()
