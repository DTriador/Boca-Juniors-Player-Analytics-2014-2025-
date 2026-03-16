import pandas as pd
import os


# RUTAS DEL PROYECTO

# carpeta donde están los datos originales organizados por año
RAW_PATH = "data/raw"

# carpeta donde vamos a guardar los datasets procesados
PROCESSED_PATH = "data/processed"

# diccionario donde vamos a guardar todos los dataframes
# cada clave será un tipo de dataset (matchlogs, shooting, etc.)
datasets = {}

print("Buscando archivos...")


# RECORRER TODAS LAS CARPETAS DE TEMPORADAS

for year_folder in os.listdir(RAW_PATH):

    year_path = os.path.join(RAW_PATH, year_folder)

    # verificamos que sea realmente una carpeta
    if os.path.isdir(year_path):

        # guardamos el año como temporada
        season = year_folder

        # recorrer todos los archivos dentro de la carpeta del año
        for file in os.listdir(year_path):

            if file.endswith(".csv"):

                file_path = os.path.join(year_path, file)

                print(f"Cargando: {file}")

                # cargar el csv
                df = pd.read_csv(file_path)

              
                # AGREGAR COLUMNA TEMPORADA
                
                df["season"] = season

                # DETECTAR COMPETENCIA

                if "Comp" in df.columns:
                    df = df.rename(columns={"Comp": "competition"})

                if "Competition" in df.columns:
                    df = df.rename(columns={"Competition": "competition"})


                # IDENTIFICAR EL TIPO DE DATASET

                dataset_name = file.split("_stats_")[-1].replace(".csv", "")

                if "matchlogs" in file:
                    dataset_name = "matchlogs"

                # si el dataset todavía no existe en el diccionario
                # creamos una lista vacía
                if dataset_name not in datasets:
                    datasets[dataset_name] = []

                # agregamos el dataframe a la lista correspondiente
                datasets[dataset_name].append(df)



print("\nUnificando datasets...")


# CONCATENAR TODOS LOS DATASETS POR TIPO

combined_data = {}

for name, df_list in datasets.items():

    # unir todos los años en un solo dataframe
    combined_df = pd.concat(df_list, ignore_index=True)

    combined_data[name] = combined_df

    # guardar dataset combinado
    output_path = os.path.join(PROCESSED_PATH, f"{name}_combined.csv")

    combined_df.to_csv(output_path, index=False)

    print(f"✔ Guardado: {name}_combined.csv")



# CREAR DATASET TEAM_SEASON_SUMMARY

print("\nCreando resumen por temporada...")

# usamos matchlogs porque ahí están los resultados de cada partido
if "matchlogs" in combined_data:

    matchlogs = combined_data["matchlogs"]

    # IDENTIFICAR COLUMNAS DE GOLES

    goals_for_col = None
    goals_against_col = None

    for col in matchlogs.columns:

        if col.lower() in ["gf", "goals_for"]:
            goals_for_col = col

        if col.lower() in ["ga", "goals_against"]:
            goals_against_col = col


    # CALCULAR RESULTADO DEL PARTIDO


    def get_result(row):

        if row[goals_for_col] > row[goals_against_col]:
            return "win"

        elif row[goals_for_col] < row[goals_against_col]:
            return "loss"

        else:
            return "draw"


    matchlogs["result"] = matchlogs.apply(get_result, axis=1)


    # AGRUPAR POR TEMPORADA

    summary = matchlogs.groupby("season").agg(

        matches_played=("season", "count"),
        goals_for=(goals_for_col, "sum"),
        goals_against=(goals_against_col, "sum")

    ).reset_index()


    # CALCULAR VICTORIAS / EMPATES / DERROTAS

    results = matchlogs.groupby(["season", "result"]).size().unstack(fill_value=0)

    summary["wins"] = results.get("win", 0).values
    summary["draws"] = results.get("draw", 0).values
    summary["losses"] = results.get("loss", 0).values


    # guardar dataset
    summary_path = os.path.join(PROCESSED_PATH, "team_season_summary.csv")

    summary.to_csv(summary_path, index=False)

    print("Guardado: team_season_summary.csv")


print("\nPipeline terminado")