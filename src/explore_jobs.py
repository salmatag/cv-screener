import ast
import pandas as pd

df = pd.read_parquet("data/jobs_sample.parquet")

print("Exemple job_skills :", repr(df["job_skills"].iloc[0]))


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


print("\nNombre d'offres :", len(df))
print("\n=== TOP 10 METIERS ===")
print(df["job_title_short"].value_counts().head(10))

competences = df["job_skills"].apply(to_list).explode().dropna()
print("\n=== TOP 15 COMPETENCES ===")
print(competences.value_counts().head(15))

print("\n=== TOP 10 COMPETENCES - DATA SCIENTIST ===")
ds = df[df["job_title_short"] == "Data Scientist"]["job_skills"].apply(to_list).explode().dropna()
print(ds.value_counts().head(10))

print("\n=== SALAIRE MOYEN PAR METIER (top 5) ===")
salaires = df.groupby("job_title_short")["salary_year_avg"].mean().sort_values(ascending=False).head(5)
print(salaires.round(0))

print("\n=== TELETRAVAIL ===")
print(df["job_work_from_home"].value_counts(dropna=False))