import sys
import time


def cargar_hashes_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        hashes = [hash[4:].upper() if hash.startswith('$NT$') else hash.upper() for hash in hashes]
        print(f"Se cargaron {len(hashes)} hashes desde el archivo.")
        return hashes


def crear_filtro_binario(hashes):
    hashes_ordenados = sorted(hashes)
    print(f"Se ordenaron {len(hashes_ordenados)} hashes.")
    return hashes_ordenados


def busqueda_binaria(hashes_limpio, hashes_alargado):
    hashes_limpio_ordenados = sorted(hashes_limpio)
    hashes_encontrados = []

    for hash_alargado in hashes_alargado:
        inicio = 0
        fin = len(hashes_limpio_ordenados) - 1
        encontrado = False

        while inicio <= fin:
            medio = (inicio + fin) // 2
            if hashes_limpio_ordenados[medio] == hash_alargado:
                encontrado = True
                break
            elif hashes_limpio_ordenados[medio] < hash_alargado:
                inicio = medio + 1
            else:
                fin = medio - 1

        if encontrado:
            hashes_encontrados.append(hash_alargado)

    cantidad_hashes_encontrados = len(hashes_encontrados)
    porcentaje_encontrado = cantidad_hashes_encontrados / len(hashes_alargado) * 100

    return cantidad_hashes_encontrados, porcentaje_encontrado, hashes_encontrados
    

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


def main():
    ruta_archivo_limpio = '/home/kali/Escritorio/limpio.txt'
    ruta_archivo_alargado = '/home/kali/Escritorio/alargado_shuffled.txt'
    hashes_limpio = cargar_hashes_desde_archivo(ruta_archivo_limpio)
    hashes_alargado = cargar_hashes_desde_archivo(ruta_archivo_alargado)

    # Crear el filtro binario
    filtro_binario = crear_filtro_binario(hashes_limpio)

    # Medición del tiempo inicial
    tiempo_inicial = time.perf_counter()

    # Realizar búsqueda binaria y obtener el resultado
    resultado_busqueda = busqueda_binaria(filtro_binario, hashes_alargado)
    cantidad_hashes_encontrados = resultado_busqueda[0]
    porcentaje_encontrado = resultado_busqueda[1]
    hashes_encontrados = resultado_busqueda[2]

    # Medición del tiempo final
    tiempo_final = time.perf_counter()

    tiempo_total = tiempo_final - tiempo_inicial
    tiempo_formateado = format(tiempo_total, ".6f")
    print(f"Porcentaje de hashes encontrados: {porcentaje_encontrado}%")
    print(f"Tiempo total de búsqueda: {tiempo_formateado} s")

    # Comparar hashes para obtener falsos positivos y falsos negativos
    falsos_positivos, falsos_negativos = comparar_hashes_originales(hashes_encontrados, hashes_limpio)
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")

    # Obtener el tamaño del filtro binario
    tamano_filtro_binario = sys.getsizeof(filtro_binario)
    print(f"Tamaño del filtro binario: {tamano_filtro_binario} bytes")


if __name__ == '__main__':
    main()

