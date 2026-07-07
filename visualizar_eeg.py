import os
import mne
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import argparse

CANALES_1020 = [
    'Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'C3', 'C4', 'T3', 'T4',
    'T5', 'T6', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz', 'Pz'
]

def verificar_ruta_dinamica(path):
    """Rastrea de forma interactiva dónde se interrumpe un acceso a ruta de archivo."""
    if os.path.exists(path): return True
    print("❌ ERROR: No se encontró el archivo.")
    partes = path.split(os.sep)
    ruta_parcial = partes[0] + os.sep if partes[0] else ""
    for parte in partes[1:]:
        nueva_ruta = os.path.join(ruta_parcial, parte)
        if not os.path.exists(nueva_ruta):
            print(f"⚠️ La ruta es válida hasta: {ruta_parcial}")
            try:
                print(f"📂 Contenido disponible en esa carpeta: {os.listdir(ruta_parcial)}")
            except: pass
            break
        ruta_parcial = nueva_ruta
    return False

def visualizar_eeg(ruta_archivo, sfreq=200):
    if not verificar_ruta_dinamica(ruta_archivo): return

    print("📖 Cargando matriz de datos...")
    ext = os.path.splitext(ruta_archivo)[1].lower()
    
    if ext == '.parquet':
        df = pl.read_parquet(ruta_archivo)
        if "Time_sec" in df.columns: df = df.drop("Time_sec")
        data = df.to_numpy().T
    elif ext == '.csv':
        df = pl.read_csv(ruta_archivo)
        if "Time_sec" in df.columns: df = df.drop("Time_sec")
        data = df.to_numpy().T
    else:
        df = pd.read_csv(ruta_archivo, sep=r'\s+', header=None)
        data = df.values.T 

    nombres_salida = CANALES_1020
    if data.shape[0] != len(CANALES_1020):
        print(f"⚠️ Alerta: El archivo cuenta con {data.shape[0]} señales, pero se esperaban {len(CANALES_1020)}.")
        nombres_salida = [f"EEG_{i}" for i in range(data.shape[0])]

    # Inicialización del entorno MNE y mapeo espacial 10-20
    info = mne.create_info(ch_names=nombres_salida, sfreq=sfreq, ch_types='eeg')
    raw = mne.io.RawArray(data, info)
    montage = mne.channels.make_standard_montage('standard_1020')
    raw.set_montage(montage, on_missing='warn')

    print("🎨 Desplegando visor interactivo de ondas EEG...")
    raw.plot(n_channels=len(nombres_salida), title=f'Registro: {os.path.basename(ruta_archivo)}', scalings='auto')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visor Interactivo Universal de Señales EEG")
    parser.add_argument("archivo", type=str, help="Ruta completa al archivo de datos (.parquet, .csv, .txt)")
    parser.add_argument("--sfreq", type=int, default=200, help="Frecuencia de muestreo (Por defecto: 200)")
    
    args = parser.parse_args()
    visualizar_eeg(args.archivo, args.sfreq)