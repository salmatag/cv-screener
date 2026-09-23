from pathlib import Path
import pdfplumber

for fichier in sorted(Path("data").glob("*.pdf")):
    with pdfplumber.open(fichier) as pdf:
        texte = "\n".join((page.extract_text() or "") for page in pdf.pages)
    print("=" * 40)
    print(fichier.name)
    print("=" * 40)
    print(texte)
    print()