import os
import json
from pathlib import Path
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

OFFRE = """Poste : Data Scientist.
Competences requises : Python, pandas, scikit-learn, SQL, machine learning, NLP.
Apprecie : Docker, TensorFlow, Power BI.
Experience : 2 ans minimum."""

PROMPT = """Tu es un assistant de recrutement. Evalue la pertinence du CV par rapport a l'offre.
Reponds UNIQUEMENT en JSON avec les cles : score (entier 0-100),
competences_presentes (liste), competences_manquantes (liste), justification (une phrase).

OFFRE:
{offre}

CV:
{cv}
"""

REFERENCE = {"cv_data.pdf": 2, "cv_data_junior.pdf": 1, "cv_web.pdf": 0}

MOTEURS = [
    ("ollama-1b", "ollama", "llama3.2:1b"),
    ("ollama-3b", "ollama", "llama3.2:3b"),
    ("groq-20b", "groq", None),
]


def extraire_texte(chemin):
    with pdfplumber.open(chemin) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def _groq(prompt):
    from groq import Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    reponse = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(reponse.choices[0].message.content)


def _ollama(prompt, model):
    import ollama
    reponse = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0},
    )
    return json.loads(reponse["message"]["content"])


def scorer(cv_texte, backend, model=None):
    prompt = PROMPT.format(offre=OFFRE, cv=cv_texte)
    return _groq(prompt) if backend == "groq" else _ollama(prompt, model)


ordre_attendu = sorted(REFERENCE, key=REFERENCE.get, reverse=True)
meilleur_attendu = ordre_attendu[0]

print(f"{'Moteur':<12} | {'Scores data/junior/web':<24} | Top-1 | Ordre exact")
print("-" * 72)
for nom, backend, model in MOTEURS:
    scores = {}
    for fichier in sorted(Path("data").glob("*.pdf")):
        scores[fichier.name] = scorer(extraire_texte(fichier), backend, model).get("score", 0)
    ordre = sorted(scores, key=scores.get, reverse=True)
    top1 = "OK" if ordre[0] == meilleur_attendu else "NON"
    exact = "OK" if ordre == ordre_attendu else "NON"
    s = f"{scores.get('cv_data.pdf')}/{scores.get('cv_data_junior.pdf')}/{scores.get('cv_web.pdf')}"
    print(f"{nom:<12} | {s:<24} | {top1:<5} | {exact}")