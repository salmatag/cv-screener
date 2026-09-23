import ast
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_parquet("data/jobs_sample.parquet")


def to_list(valeur):
    if isinstance(valeur, list):
        return valeur
    if isinstance(valeur, str):
        try:
            resultat = ast.literal_eval(valeur)
            return resultat if isinstance(resultat, list) else []
        except (ValueError, SyntaxError):
            return []
    return []


df["skills"] = df["job_skills"].apply(to_list)
Path("data/figures").mkdir(parents=True, exist_ok=True)

# 1. Top 15 competences
top = df["skills"].explode().dropna().value_counts().head(15)
plt.figure(figsize=(10, 6))
top.sort_values().plot(kind="barh", color="#2b6cb0")
plt.title("Top 15 competences demandees")
plt.xlabel("Nombre d'offres")
plt.tight_layout()
plt.savefig("data/figures/top_skills.png", dpi=120)
plt.close()

# 2. Top competences par metier
metiers = ["Data Scientist", "Data Analyst", "Data Engineer"]
fig, ax = plt.subplots(figsize=(12, 6))
for metier in metiers:
    skills = df[df["job_title_short"] == metier]["skills"].explode().dropna().value_counts().head(8)
    ax.bar(skills.index, skills.values, alpha=0.6, label=metier)
ax.set_title("Top competences par metier")
ax.set_ylabel("Nombre d'offres")
ax.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("data/figures/skills_by_role.png", dpi=120)
plt.close()

# 3. Salaire moyen par metier
salaires = df.groupby("job_title_short")["salary_year_avg"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
salaires.sort_values().plot(kind="barh", color="#38a169")
plt.title("Salaire moyen par metier (USD)")
plt.xlabel("Salaire annuel moyen")
plt.tight_layout()
plt.savefig("data/figures/salary_by_role.png", dpi=120)
plt.close()

print("Figures sauvegardees dans data/figures/")