import os

print(" Iniciando pipeline...")

os.system("python scripts/load_data.py")
os.system("python scripts/clean_data.py")
os.system("python scripts/build_master_dataset.py")

print("Pipeline terminado")