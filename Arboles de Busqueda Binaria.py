import binascii
import datetime
import string
import time
import sys


class NodoArbol:
    def __init__(self, valor=None):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBusquedaBinaria:
    def __init__(self):
        self.raiz = None

    def agregar_nodo(self, valor):
        if self.raiz is None:
            self.raiz = NodoArbol(valor)
        else:
            self._agregar_nodo(valor, self.raiz)

    def _agregar_nodo(self, valor, nodo_actual):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoArbol(valor)
            else:
                self._agregar_nodo(valor, nodo_actual.izquierda)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoArbol(valor)
            else:
                self._agregar_nodo(valor, nodo_actual.derecha)
        else:
            pass  # valor ya existe en el árbol

    def buscar_nodo(self, valor):
        return self._buscar_nodo(valor, self.raiz)

    def _buscar_nodo(self, valor, nodo_actual):
        if nodo_actual is None:
            return False
        elif nodo_actual.valor == valor:
            return True
        elif valor < nodo_actual.valor:
            return self._buscar_nodo(valor, nodo_actual.izquierda)
        else:
            return self._buscar_nodo(valor, nodo_actual.derecha)
    
    def arbol_inorden(self, nodo_actual):
        if nodo_actual is None:
            return []

        izquierda = self.arbol_inorden(nodo_actual.izquierda)
        derecha = self.arbol_inorden(nodo_actual.derecha)

        return izquierda + [nodo_actual.valor] + derecha
    
    def obtener_profundidad(self):
        return self._obtener_profundidad(self.raiz)

    def _obtener_profundidad(self, nodo_actual):
        if nodo_actual is None:
            return 0

        profundidad_izquierda = self._obtener_profundidad(nodo_actual.izquierda)
        profundidad_derecha = self._obtener_profundidad(nodo_actual.derecha)

        return max(profundidad_izquierda, profundidad_derecha) + 1



def cargar_hashes_desde_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        hashes = [line.strip().split(':')[0] for line in f]
        hashes = [h.split(':')[0] for h in hashes] # quitamos el ':' y el número que va después
        print(f"Se cargaron {len(hashes)} hashes desde el archivo.")
        return hashes


def crear_arbol_busqueda_binaria(hashes):
    arbol = ArbolBusquedaBinaria()
    for h in hashes:
        hash_val_bytes = binascii.unhexlify(h)
        hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
        arbol.agregar_nodo(hash_val_int)
    print(f"Se insertaron {len(hashes)} elementos en el árbol.")
    return arbol

def obtener_tamano_arbol(arbol):
    tamano_nodos = sys.getsizeof(arbol.raiz) * len(arbol.arbol_inorden(arbol.raiz))
    tamano_valores = sys.getsizeof(arbol.raiz.valor) * len(arbol.arbol_inorden(arbol.raiz))
    tamano_total = tamano_nodos + tamano_valores
    return tamano_total


def obtener_contraseñas_descifradas(arbol, ruta_archivo):
    contraseñas_descifradas = []

    with open(ruta_archivo, 'r') as f:
        for line in f:
            if ':' in line:
                hash_descifrado = line.split(':')[0].split('$')[-1].replace('NT', '').strip()
                if all(c in string.hexdigits for c in hash_descifrado):
                    hash_val_bytes = binascii.unhexlify(hash_descifrado)
                    hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
                    if arbol.buscar_nodo(hash_val_int):
                        contraseñas_descifradas.append(hash_descifrado)

    return contraseñas_descifradas
    
def comparar_hashes(arbol, ruta_hashes_originales):
    hashes_originales = cargar_hashes_desde_archivo(ruta_hashes_originales)
    falsos_positivos = 0
    falsos_negativos = 0

    for hash_original in hashes_originales:
        hash_val_bytes = binascii.unhexlify(hash_original)
        hash_val_int = int.from_bytes(hash_val_bytes, byteorder='little')
        if not arbol.buscar_nodo(hash_val_int):
            falsos_positivos += 1

    falsos_negativos = len(arbol.arbol_inorden(arbol.raiz)) - (len(arbol.arbol_inorden(arbol.raiz)) - falsos_positivos)

    print("Resultados de comparación:")
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")

def main():
    ruta_hashes = '/home/kali/Escritorio/limpio.txt'
    ruta_crackeadas = '/home/kali/Escritorio/alargado.txt'

    arbol = crear_arbol_busqueda_binaria(cargar_hashes_desde_archivo(ruta_hashes))

    tiempo_inicio_busqueda = time.perf_counter()
    print(f"Comenzando búsqueda a las {datetime.datetime.now().strftime('%H:%M:%S')}")

    contraseñas_descifradas = obtener_contraseñas_descifradas(arbol, ruta_crackeadas)

    tiempo_finalizacion_busqueda = time.perf_counter()
    tiempo_busqueda = tiempo_finalizacion_busqueda - tiempo_inicio_busqueda

    porcentaje_encontrado = len(contraseñas_descifradas) / len(cargar_hashes_desde_archivo(ruta_crackeadas)) * 100

    print(f"Proceso finalizado a las {datetime.datetime.now().strftime('%H:%M:%S')}. Tenemos un {porcentaje_encontrado}% de hashes encontrados en el árbol.")
    print(f"La búsqueda ha tardado {tiempo_busqueda:.9f} segundos.")

    comparar_hashes(arbol, ruta_hashes)
    
    # Calcular el tamaño ocupado por el árbol en memoria
    profundidad_arbol = arbol.obtener_profundidad()
    tamano_arbol = sys.getsizeof(arbol)


    # Obtener las variables/parámetros que pueden influir en el tamaño del árbol
    variables_parametros = {
        'Número de nodos': len(arbol.arbol_inorden(arbol.raiz)),
        'Tamaño de los valores almacenados': sys.getsizeof(arbol.raiz.valor),
        'Profundidad del árbol': profundidad_arbol
    }

    tamano_arbol = obtener_tamano_arbol(arbol)
    print(f"Tamaño total del árbol: {tamano_arbol} bytes")

    print("Variables/parámetros que pueden influir en el tamaño:")
    for variable, valor in variables_parametros.items():
        print(f"{variable}: {valor}")



if __name__ == '__main__':
    main()

