import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Generando visualizaciones del análisis...")

# COLORES DEL DASHBOARD

background_color = "#0b1f3a"   
bar_color = "#f2c200"          
text_color = "white"


# CARGAR DATASETS

stats = pd.read_csv("data/processed/master_player_stats.csv")
clusters = pd.read_csv("data/processed/player_clusters.csv")

# CREAR MÉTRICA DE APORTE OFENSIVO

stats["goal_contribution"] = stats["goals"] + stats["assists"]


# 1 TOP 10 JUGADORES

top10 = (
    stats.groupby("player")["goal_contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6), facecolor=background_color)

ax = top10.sort_values().plot(
    kind="barh",
    color=bar_color
)

ax.set_facecolor(background_color)

plt.title(
    "Top 10 jugadores de Boca por contribución ofensiva (2014-2025)",
    color=text_color
)

plt.xlabel("Contribución ofensiva (Goles + Asistencias)", color=text_color)
plt.ylabel("Jugador", color=text_color)

plt.xticks(color=text_color)
plt.yticks(color=text_color)

plt.tight_layout()

plt.savefig(
    "img/python_analysis/top10_players_performance.png",
    facecolor=background_color
)

plt.show()


# 2 GOLES POR TEMPORADA

goals_season = stats.groupby("season")["goals"].sum()

plt.figure(figsize=(10,6), facecolor=background_color)

ax = goals_season.plot(
    marker="o",
    color=bar_color,
    linewidth=3
)

ax.set_facecolor(background_color)

plt.title("Goles de Boca Juniors por temporada", color=text_color)

plt.xlabel("Temporada", color=text_color)
plt.ylabel("Cantidad de goles", color=text_color)

plt.xticks(color=text_color)
plt.yticks(color=text_color)

plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    "img/python_analysis/goals_per_season.png",
    facecolor=background_color
)

plt.show()

# 3 PERFILES DE JUGADORES (CLUSTERS)

plt.figure(figsize=(8,6), facecolor=background_color)

ax = sns.scatterplot(
    data=clusters,
    x="goals",
    y="assists",
    hue="cluster",
    palette="Set2",
    s=100
)

ax.set_facecolor(background_color)

plt.title(
    "Perfiles de jugadores según rendimiento ofensivo",
    color=text_color
)

plt.xlabel("Goles", color=text_color)
plt.ylabel("Asistencias", color=text_color)

plt.xticks(color=text_color)
plt.yticks(color=text_color)

plt.legend(title="Perfil")

plt.tight_layout()

plt.savefig(
    "img/python_analysis/player_clusters.png",
    facecolor=background_color
)

plt.show()

print("Gráficos generados correctamente")