import re
from pathlib import Path
import pdfplumber

COMPETENCES = [
    "python", "pandas", "scikit-learn", "tensorflow", "nlp", "sql", "docker",
    "javascript", "react", "node.js", "html", "css", "php",
    "excel", "power bi", "statistiques",
]


def extraire_competences(texte):
    texte_min = texte.lower()
    return [c for c in COMPETENCES if c in texte_min]


def extraire_experience(texte):
    resultat = re.search(r"(\d+)\s*ans?", texte.lower())
    return int(resultat.group(1)) if resultat else None


def extraire_cv(chemin):
    with pdfplumber.open(chemin) as pdf:
        texte = "\n".join((page.extract_text() or "") for page in pdf.pages)
    return {
        "fichier": chemin.name,
        "experience": extraire_experience(texte),
        "competences": extraire_competences(texte),
    }


if __name__ == "__main__":
    for fichier in sorted(Path("data").glob("*.pdf")):
        print(extraire_cv(fichier))