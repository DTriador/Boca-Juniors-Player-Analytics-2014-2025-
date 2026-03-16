import pandas as pd

print("Calculando Player Impact Score")

df = pd.read_csv("../data/processed/master_dataset.csv")

df.columns = df.columns.str.lower()

# reemplazar valores faltantes
for col in ["goals", "assists", "shots_on_target", "key_passes"]:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# calcular score
df["impact_score"] = (
    df.get("goals", 0) * 4 +
    df.get("assists", 0) * 3 +
    df.get("shots_on_target", 0) * 1.5 +
    df.get("key_passes", 0) * 1
)

# ranking por jugador
ranking = (
    df.groupby("player")["impact_score"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

ranking.to_csv(
    "../data/processed/player_impact_ranking.csv",
    index=False
)

print("player_impact_ranking.csv creado")