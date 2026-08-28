from PyPDF2 import PdfReader

file_name = "Ata_57_Comef_pt.pdf"

# Executa a leitura do PDF
reader = PdfReader(file_name)

for i, page in enumerate(reader.pages):
    print(f"--- Página {i+1} ---")
    print(page.extract_text())