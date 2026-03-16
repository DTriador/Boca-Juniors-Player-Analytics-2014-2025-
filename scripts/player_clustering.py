import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("Ejecutando clustering de jugadores")

# cargar dataset maestro
df = pd.read_csv("data/processed/master_player_stats.csv")

# columnas que usaremos para clustering
features = ["goals", "assists", "minutes"]

# convertir a numérico
for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=features)

# normalizar datos
scaler = StandardScaler()
X = scaler.fit_transform(df[features])

# modelo de clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

# guardar resultado
df.to_csv("data/processed/player_clusters.csv", index=False)

print("Clustering terminado")
print("Archivo generado: data/processed/player_clusters.csv")