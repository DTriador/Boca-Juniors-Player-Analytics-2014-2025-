import pandas as pd

print("Analizando jugadores de Boca...")

df = pd.read_csv("data/processed/master_player_stats.csv")

# asegurarnos de que goles y asistencias sean numéricos
df["goals"] = pd.to_numeric(df.get("goals", 0), errors="coerce")
df["assists"] = pd.to_numeric(df.get("assists", 0), errors="coerce")
df["minutes"] = pd.to_numeric(df.get("minutes", 0), errors="coerce")

# crear métrica simple de rendimiento
df["performance_score"] = (
    df["goals"].fillna(0) * 4 +
    df["assists"].fillna(0) * 3 +
    df["minutes"].fillna(0) / 90
)

ranking = (
    df.groupby("player")["performance_score"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 jugadores de Boca (2014-2025):\n")
print(ranking.head(10))