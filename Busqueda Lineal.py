import time
import sys

def cargar_hashes_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        print(f"Se cargaron {len(hashes)} hashes desde el archivo.")
        return hashes

def cargar_hashes_descifrados_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        # Omitimos la primera línea del archivo
        hashes_descifrados = []
        for line in f.readlines()[1:]:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                hash_descifrado = parts[0].upper().replace("$NT$", "")  # Convertir a mayúsculas y quitar "$NT$"
                hashes_descifrados.append(hash_descifrado)
        print(f"Se cargaron {len(hashes_descifrados)} hashes descifrados desde el archivo.")
        return hashes_descifrados

def buscar_hashes_lineal(hashes, hashes_descifrados):
    tiempo_inicio = time.perf_counter()

    hashes_encontrados = []
    for hash_orig in hashes:
        if hash_orig in hashes_descifrados:
            hashes_encontrados.append(hash_orig)
    
    porcentaje_hashes = len(hashes_encontrados) / len(hashes_descifrados) * 100

    tiempo_finalizacion = time.perf_counter()
    tiempo_transcurrido = tiempo_finalizacion - tiempo_inicio

    print(f"Comienza el proceso a las {time.strftime('%H:%M:%S')} del {time.strftime('%d/%m/%Y')}")
    print(f"Proceso finalizado a las {time.strftime('%H:%M:%S')} del {time.strftime('%d/%m/%Y')}")
    print(f"Tiempo de ejecución: {tiempo_transcurrido:.9f} segundos")
    print(f"{porcentaje_hashes:.2f}% de hashes de crackeadas.txt encontrados en hashes.txt")

    # Comparar hashes para obtener falsos positivos y falsos negativos
    falsos_positivos = len(hashes_encontrados) - len(hashes)
    falsos_negativos = len(hashes) - len(hashes_encontrados)
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")

    # Obtener el tamaño de la estructura de datos
    tamano_estructura_datos = sys.getsizeof(hashes)
    print(f"Tamaño de la estructura de datos: {tamano_estructura_datos} bytes")


ruta_archivo_hashes = '/home/kali/Escritorio/limpio.txt'
ruta_archivo_crackeadas = '/home/kali/Escritorio/alargado.txt'

hashes = cargar_hashes_desde_archivo(ruta_archivo_hashes)
hashes_descifrados = cargar_hashes_descifrados_desde_archivo(ruta_archivo_crackeadas)
buscar_hashes_lineal(hashes, hashes_descifrados)

