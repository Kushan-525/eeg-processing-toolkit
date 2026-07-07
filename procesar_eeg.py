import polars as pl
import numpy as np
import os
import glob
import re
import argparse

# Configuración del estándar internacional de 19 canales EEG
CANALES_1020 = [
    'Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'C3', 'C4', 'T3', 'T4',
    'T5', 'T6', 'P3', 'P4', 'O1', 'O2', 'Fz', 'Cz', 'Pz'
]
N_CHANNELS = len(CANALES_1020)

def procesar_archivo_eeg(path_entrada, es_txt=False):
    directorio = os.path.dirname(path_entrada)
    nombre_base = os.path.splitext(os.path.basename(path_entrada))[0]
    
    # Asignación dinámica de frecuencia de muestreo
    if es_txt:
        sfreq = 128  # Estándar para tus archivos de sueño .txt
    else:
        match = re.search(r'(\d+)', os.path.basename(directorio))
        sfreq = 200 if (match and int(match.group(1)) <= 12) else 250

    print(f"📦 Procesando: {os.path.basename(path_entrada)} | Frecuencia: {sfreq}Hz")
    
    try:
        if es_txt:
            # Lectura directa y veloz de archivos planos espaciados
            df = pl.read_csv(path_entrada, has_header=False, separator=" ", new_columns=CANALES_1020)
            n_samples = len(df)
        else:
            # Lectura de datos binarios flotantes crudos
            raw_data = np.fromfile(path_entrada, dtype='float32')
            if len(raw_data) == 0: return
            
            n_samples = len(raw_data) // N_CHANNELS
            raw_data = raw_data[:n_samples * N_CHANNELS]
            data_reshaped = raw_data.reshape(n_samples, N_CHANNELS)
            df = pl.DataFrame(data_reshaped, schema=CANALES_1020)
        
        # Inserción del vector de tiempo de alta precisión
        time_vec = np.arange(n_samples) / sfreq
        df = df.insert_column(0, pl.Series("Time_sec", time_vec))
        
        # Guardado optimizado en la misma carpeta local (Parquet Snappy + JSON)
        path_parquet = os.path.join(directorio, f"{nombre_base}.parquet")
        path_json = os.path.join(directorio, f"{nombre_base}.json")
        
        df.write_parquet(path_parquet, compression="snappy")
        df.write_json(path_json)
        
        size_pq = os.path.getsize(path_parquet) / (1024 * 1024)
        print(f"   ✅ Guardados localmente: Parquet ({size_pq:.2f}MB) y JSON.")
        
    except Exception as e:
        print(f"   ❌ Error en procesamiento: {e}")

def ejecutar_pipeline(ruta_raiz):
    if not os.path.exists(ruta_raiz):
        print(f"Error: La ruta {ruta_raiz} no existe o no es accesible.")
        return

    # Buscar archivos binarios crudos de epilepsia
    patrones_bin = ["*.cnt", "*.CNT", "*.dat", "*.bin", "Sz*"]
    archivos_bin = []
    for p in patrones_bin:
        archivos_bin.extend(glob.glob(os.path.join(ruta_raiz, "**", p), recursive=True))
    archivos_bin = [f for f in list(set(archivos_bin)) if os.path.isfile(f) and not f.endswith(('.csv', '.parquet', '.json', '.txt'))]

    # Buscar archivos estructurados .txt de sueño
    archivos_txt = glob.glob(os.path.join(ruta_raiz, "**", "*.txt"), recursive=True)

    print(f"🔍 Detectados localmente: {len(archivos_bin)} binarios y {len(archivos_txt)} archivos de texto.")
    
    for f in archivos_bin: procesar_archivo_eeg(f, es_txt=False)
    for f in archivos_txt: procesar_archivo_eeg(f, es_txt=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Unificado de Procesamiento EEG")
    parser.add_argument("ruta", type=str, help="Ruta local de la carpeta 'Participantes'")
    args = parser.parse_args()
    
    ejecutar_pipeline(args.ruta)
    print("\n--- PIPELINE FINALIZADO ---")