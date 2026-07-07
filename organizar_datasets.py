import shutil
from pathlib import Path
import argparse

def organizar_sueno(base_path):
    """Organiza archivos .txt de sueño (ej. AA_1_128) desde Carpeta 1 y 2."""
    base_path = Path(base_path)
    carpeta_maestra = base_path / "Participantes"
    carpeta_maestra.mkdir(exist_ok=True)
    
    for subcarpeta in ["Carpeta 1", "Carpeta 2"]:
        ruta_sub = base_path / subcarpeta
        if not ruta_sub.exists():
            print(f"⚠️ No se encontró: {subcarpeta}")
            continue
        
        for archivo in ruta_sub.glob("*.txt"):
            if archivo.is_file():
                # Extrae el ID (ej: 'AA') antes del primer guion bajo
                id_participante = archivo.stem.split('_')[0]
                ruta_destino = carpeta_maestra / id_participante
                ruta_destino.mkdir(parents=True, exist_ok=True)
                
                shutil.move(str(archivo), str(ruta_destino / archivo.name))
                print(f"Mover: {archivo.name} ➡️ Participantes/{id_participante}/")

def organizar_epilepsia(base_path):
    """Organiza archivos de crisis que empiezan con 'SZ' (ej. SZ01_A)."""
    base_path = Path(base_path)
    carpeta_maestra = base_path / "Participantes"
    carpeta_maestra.mkdir(exist_ok=True)
    
    for archivo in base_path.glob("SZ*"):
        if archivo.is_file():
            # Extrae el prefijo (ej: 'SZ01') y se queda con el número ('01')
            prefijo = archivo.stem.split('_')[0]
            id_sujeto = prefijo[2:] 
            
            nombre_carpeta = f"Participante_{id_sujeto}"
            ruta_destino = carpeta_maestra / nombre_carpeta
            ruta_destino.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(archivo), str(ruta_destino / archivo.name))
            print(f"Mover: {archivo.name} ➡️ Participantes/{nombre_carpeta}/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organizador Universal de Datasets EEG")
    parser.add_argument("ruta", type=str, help="Ruta raíz donde están los archivos crudos")
    parser.add_argument("--modo", choices=["sueno", "epilepsia"], required=True, help="Dataset a organizar")
    
    args = parser.parse_args()
    
    if args.modo == "sueno":
        organizar_sueno(args.ruta)
    else:
        organizar_epilepsia(args.ruta)
    print("\n✨ ¡Organización completada con éxito!")