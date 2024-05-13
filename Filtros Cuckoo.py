import cuckoofilter
import binascii
import time

def cargar_hashes_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        hashes = []
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                hash_descifrado = parts[0].upper()  # Convertir a mayúsculas
                hashes.append(hash_descifrado)
        print(f"Se cargaron {len(hashes)} hashes desde el archivo {ruta_archivo}.")
        return hashes


def crear_filtro_cuckoo(hashes, capacity, fingerprint_size):
    filtro = cuckoofilter.CuckooFilter(capacity=capacity, fingerprint_size=fingerprint_size)
    for h in hashes:
        hash_val_bytes = binascii.unhexlify(h)
        filtro.insert(hash_val_bytes)
    print(f"Se insertaron {filtro.size()} elementos en el filtro.")
    return filtro


def comprobar_hashes_en_filtro_cuckoo(filtro, hashes_a_comprobar):
    cant_hashes_reales = 0
    hashes_encontrados = []
    hashes_bytes = [binascii.unhexlify(h) for h in hashes_a_comprobar]  # Conversión previa a bytes
    tiempo_inicio = time.perf_counter()
    for hash_val_bytes in hashes_bytes:
        if filtro.contains(hash_val_bytes):
            cant_hashes_reales += 1
            hashes_encontrados.append(binascii.hexlify(hash_val_bytes).decode().upper())
    tiempo_final = time.perf_counter()
    tiempo_total = tiempo_final - tiempo_inicio
    porcentaje_en_filtro = (cant_hashes_reales / len(hashes_a_comprobar)) * 100
    porcentaje_en_filtro_str = f"{porcentaje_en_filtro:.7f}".replace(".", ",")  # Reemplazar el punto por coma
    tiempo_total_str = f"{tiempo_total:.6f}".replace(".", ",")  # Reemplazar el punto por coma
    print(f"Porcentaje de hashes reales en el filtro cuckoo: {porcentaje_en_filtro_str}%")
    print(f"El tiempo de comparación fue de {tiempo_total_str} segundos.")
    return hashes_encontrados

def calcular_falsos_positivos(hashes_originales, hashes_encontrados):
    cant_falsos_positivos = 0
    cant_verdaderos_positivos = 0
    for h in hashes_encontrados:
        if h not in hashes_originales:
            cant_falsos_positivos += 1
        else:
            cant_verdaderos_positivos += 1

    print(f"Cantidad de verdaderos positivos: {cant_verdaderos_positivos}")
    print(f"Cantidad de falsos positivos: {cant_falsos_positivos}")
    print(f"Cantidad total de hashes encontrados: {len(hashes_encontrados)}")



def main():
    ruta_archivo_hashes = '/home/kali/Escritorio/limpio.txt'
    ruta_archivo_crackeadas = '/home/kali/Escritorio/alargado.txt'

    hashes = cargar_hashes_desde_archivo(ruta_archivo_hashes)
    hashes_a_comprobar = []

    with open(ruta_archivo_crackeadas, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            if len(parts) >= 2:
                hash_descifrado = parts[0][4:].upper()  # Quitar los primeros 4 caracteres ($NT$) y convertir a mayúsculas
                hashes_a_comprobar.append(hash_descifrado)

    capacidades = [len(hashes) * i for i in range(1, 5)]
    tamanos_huella = [1, 2, 3, 4]

    for tamano_huella in tamanos_huella:
        for capacidad in capacidades:
            filtro = crear_filtro_cuckoo(hashes, capacidad, tamano_huella)
            print(f"Capacidad: {capacidad}, Tamaño de Huella: {tamano_huella}")
            hashes_encontrados = comprobar_hashes_en_filtro_cuckoo(filtro, hashes_a_comprobar)
            calcular_falsos_positivos(hashes, hashes_encontrados)
            print()

    print("Fin del programa")


if __name__ == '__main__':
    main()


