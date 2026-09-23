import os
import json
from pathlib import Path
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

OFFRE = """
Poste : Data Scientist.
Competences requises : Python, pandas, scikit-learn, SQL, machine learning, NLP.
Apprecie : Docker, TensorFlow, Power BI.
Experience : 2 ans minimum.
"""

PROMPT = """Tu es un assistant de recrutement. Evalue la pertinence du CV par rapport a l'offre.
Reponds UNIQUEMENT en JSON avec les cles : score (entier 0-100),
competences_presentes (liste), competences_manquantes (liste), justification (une phrase).

OFFRE:
{offre}

CV:
{cv}
"""


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


def _ollama(prompt, model="llama3.2:3b"):
    import ollama
    reponse = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0},
    )
    return json.loads(reponse["message"]["content"])


def scorer(cv_texte, backend="ollama"):
    prompt = PROMPT.format(offre=OFFRE, cv=cv_texte)
    if backend == "groq":
        return _groq(prompt)
    return _ollama(prompt)


BACKEND = "ollama"  # donnees personnelles -> local par defaut
#BACKEND = "groq" # donnees envoyees sur cloud 

resultats = []
for fichier in sorted(Path("data").glob("*.pdf")):
    infos = scorer(extraire_texte(fichier), backend=BACKEND)
    infos["fichier"] = fichier.name
    resultats.append(infos)

print(f"Moteur : {BACKEND}\n")
for r in sorted(resultats, key=lambda x: x.get("score", 0), reverse=True):
    print(f"{r.get('score', '?')}/100  {r['fichier']}")
    print(f"        presente   : {r.get('competences_presentes')}")
    print(f"        manquantes : {r.get('competences_manquantes')}")
    print(f"        -> {r.get('justification')}\n")