import pandas as pd

print("Construyendo dataset maestro de jugadores")


# CARGAR DATASETS LIMPIOS

standard = pd.read_csv("data/processed/standard_clean_clean.csv")
shooting = pd.read_csv("data/processed/shooting_clean_clean.csv")
passing = pd.read_csv("data/processed/passing_clean_clean.csv")
playing_time = pd.read_csv("data/processed/playing_time_clean_clean.csv")



# NORMALIZAR NOMBRES DE COLUMNAS

standard.columns = standard.columns.str.lower()
shooting.columns = shooting.columns.str.lower()
passing.columns = passing.columns.str.lower()
playing_time.columns = playing_time.columns.str.lower()


# CLAVES PARA UNIR DATASETS

merge_keys = ["player", "season"]



# MERGE DATASETS

master = pd.merge(
    standard,
    shooting,
    on=merge_keys,
    how="left",
    suffixes=("", "_shooting")
)

master = pd.merge(
    master,
    passing,
    on=merge_keys,
    how="left",
    suffixes=("", "_passing")
)

master = pd.merge(
    master,
    playing_time,
    on=merge_keys,
    how="left",
    suffixes=("", "_time")
)


# LIMPIAR DUPLICADOS

master = master.drop_duplicates()


# GUARDAR DATASET FINAL

master.to_csv("data/processed/master_player_stats.csv", index=False)


print("master_player_stats.csv creado correctamente")