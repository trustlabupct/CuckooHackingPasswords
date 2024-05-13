import sys
import hashlib
import time


def cargar_hashes_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        print(f"Se cargaron {len(hashes)} hashes desde el archivo {ruta_archivo}.")
        return hashes


def crear_tabla_hash(hashes):
    tabla_hash = {}
    for h in hashes:
        tabla_hash[h] = True
    print(f"Se insertaron {len(tabla_hash)} elementos en la tabla hash.")
    return tabla_hash


def comprobar_hashes_en_tabla(tabla_hash, hashes_a_comprobar):
    hashes_encontrados = []
    t_inicio = time.perf_counter()
    for h in hashes_a_comprobar:
        if h in tabla_hash:
            hashes_encontrados.append(h)
    t_fin = time.perf_counter()
    tiempo_total = t_fin - t_inicio
    porcentaje_hashes_encontrados = len(hashes_encontrados) / len(hashes_a_comprobar) * 100
    print(f"Proceso finalizado a las {time.strftime('%H:%M:%S')}. Tienes un {porcentaje_hashes_encontrados:.2f}% de hashes que están en la tabla hash. La comparación ha tardado {tiempo_total:.9f} segundos.")
    return hashes_encontrados


def comparar_hashes_originales(hashes_encontrados, hashes_originales):
    falsos_positivos = 0
    falsos_negativos = 0

    for hash_encontrado in hashes_encontrados:
        if hash_encontrado not in hashes_originales:
            falsos_positivos += 1

    for hash_original in hashes_originales:
        if hash_original not in hashes_encontrados:
            falsos_negativos += 1

    return falsos_positivos, falsos_negativos


def obtener_tamano_estructura_datos(tabla_hash):
    tamano_bytes = sys.getsizeof(tabla_hash)
    return tamano_bytes


def main():
    ruta_archivo_hashes = '/home/kali/Escritorio/limpio.txt'
    ruta_archivo_crackeadas = '/home/kali/Escritorio/alargado.txt'

    # Cargar hashes desde hashes.txt y crear tabla hash
    hashes_originales = cargar_hashes_desde_archivo(ruta_archivo_hashes)
    tabla_hash = crear_tabla_hash(hashes_originales)

    # Cargar hashes a comprobar desde crackeadas.txt
    hashes_a_comprobar = []
    with open(ruta_archivo_crackeadas, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                hash_descifrado = parts[0][4:].upper()  # Quitar los primeros 4 caracteres ($NT$) y convertir a mayúsculas
                hashes_a_comprobar.append(hash_descifrado)

    # Comprobar hashes en tabla hash
    hashes_encontrados = comprobar_hashes_en_tabla(tabla_hash, hashes_a_comprobar)

    # Comparar hashes para obtener falsos positivos y falsos negativos
    falsos_positivos, falsos_negativos = comparar_hashes_originales(hashes_encontrados, hashes_originales)
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")

    # Obtener el tamaño de la estructura de datos
    tamano_tabla_hash = obtener_tamano_estructura_datos(tabla_hash)
    print(f"Tamaño de la tabla hash: {tamano_tabla_hash} bytes")

    print("Fin del programa")


if __name__ == '__main__':
    main()

