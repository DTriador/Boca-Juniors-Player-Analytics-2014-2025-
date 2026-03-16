import pandas as pd
import os


# RUTAS
# carpeta donde están los datasets combinados
PROCESSED_PATH = "data/processed"

print("Iniciando limpieza de datos...")

# RECORRER TODOS LOS CSV DE LA CARPETA

for file in os.listdir(PROCESSED_PATH):

    # solo trabajar con los archivos combinados
    if file.endswith("_combined.csv"):

        file_path = os.path.join(PROCESSED_PATH, file)

        print(f"Limpiando: {file}")

        df = pd.read_csv(file_path)


        # ESTANDARIZAR NOMBRES DE COLUMNAS

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("%", "pct")
        )

        # ELIMINAR COLUMNAS INNECESARIAS

        columnas_inutiles = [
            "notes",
            "match_report",
            "report",
            "unnamed:_0"
        ]

        df = df.drop(columns=[col for col in columnas_inutiles if col in df.columns])


        # CONVERTIR COLUMNAS NUMÉRICAS

        for col in df.columns:

            # ignoramos columnas que claramente son texto
            if col not in ["player", "team", "opponent", "competition", "season", "result"]:

                df[col] = pd.to_numeric(df[col], errors="ignore")


        # ELIMINAR FILAS TOTALMENTE VACÍAS
        df = df.dropna(how="all")


        # GUARDAR DATASET LIMPIO

        clean_name = file.replace("_combined", "_clean")

        output_path = os.path.join(PROCESSED_PATH, clean_name)

        df.to_csv(output_path, index=False)

        print(f"✔ Guardado: {clean_name}")


print("\n Limpieza terminada")