import os
from pathlib import Path
import pdfplumber
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

OFFRE_DEFAUT = """Poste : Data Scientist.
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


def extraire_texte(chemin):
    if str(chemin).lower().endswith(".pdf"):
        with pdfplumber.open(chemin) as pdf:
            return "\n".join((page.extract_text() or "") for page in pdf.pages)
    return Path(chemin).read_text(encoding="utf-8", errors="ignore")


def _groq(prompt):
    import json
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
    import json
    import ollama
    reponse = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"temperature": 0},
    )
    return json.loads(reponse["message"]["content"])


def scorer(cv_texte, offre, backend):
    prompt = PROMPT.format(offre=offre, cv=cv_texte)
    return _groq(prompt) if backend == "groq" else _ollama(prompt)


def classer(offre, fichiers, backend):
    if not fichiers:
        return [["-", "Ajoute des CV (PDF/TXT).", "", "", "", ""]]
    if not offre.strip():
        return [["-", "Saisis l'offre d'emploi.", "", "", "", ""]]
    resultats = []
    for f in fichiers:
        chemin = f if isinstance(f, str) else f.name
        infos = scorer(extraire_texte(chemin), offre, backend)
        resultats.append([
            Path(chemin).name,
            infos.get("score", 0),
            ", ".join(infos.get("competences_presentes", [])),
            ", ".join(infos.get("competences_manquantes", [])),
            infos.get("justification", ""),
        ])
    resultats.sort(key=lambda r: r[1], reverse=True)
    return [[i + 1] + r for i, r in enumerate(resultats)]


demo = gr.Interface(
    fn=classer,
    inputs=[
        gr.Textbox(label="Offre d'emploi", lines=6, value=OFFRE_DEFAUT),
        gr.File(label="CV (PDF/TXT)", file_count="multiple", file_types=[".pdf", ".txt"]),
        gr.Dropdown(["groq", "ollama"], value="groq", label="Moteur"),
    ],
    outputs=gr.Dataframe(
        headers=["Rang", "Fichier", "Score", "Competences presentes",
                 "Competences manquantes", "Justification"],
        wrap=True,
    ),
    title="Tri de CV selon une offre",
    description="Depose une offre et plusieurs CV. L'IA classe ; l'humain decide.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7863)))
