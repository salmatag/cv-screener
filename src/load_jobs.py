from datasets import load_dataset

ds = load_dataset("lukebarousse/data_jobs", split="train")
df = ds.to_pandas()
print("Total offres :", len(df))

echantillon = df.sample(5000, random_state=42)
echantillon.to_parquet("data/jobs_sample.parquet")
print("Echantillon sauvegarde :", len(echantillon))
print("Colonnes :", echantillon.columns.tolist())