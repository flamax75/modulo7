import shutil
import sqlite3
from tabulate import tabulate
from unidecode import unidecode
import os

# Función para obtener el idioma válido del usuario


def obtener_idioma_valido():
    # Lista de idiomas válidos sin acentos
    idiomas_validos = ['espanol', 'ingles', 'aleman',
                       'frances', 'portugues', 'italiano', 'sueco']
    while True:
        # Convertir la entrada del usuario a minúsculas y eliminar acentos
        idioma = unidecode(input(
            "Ingrese el idioma (español, inglés, alemán, francés, portugués, italiano, sueco, o 'parar' para volver al menú): ").lower())
        if idioma == 'parar':
            return None
        if idioma in idiomas_validos:
            return idioma
        else:
            print("Por favor, ingrese un idioma válido.")


def obtener_continente_valido():
    continentes_validos = [
        'america del sur', 'america del norte', 'europa', 'asia', 'africa', 'oceania']
    while True:
        continente = unidecode(input(
            "Ingrese el continente (América del Sur, América del Norte, Europa, Asia, África, Oceanía, o 'parar' para volver al menú): ").lower())
        if continente == 'parar':
            return None
        if continente in continentes_validos:
            return continente
        else:
            print("Por favor, ingrese un continente válido.")


# Nombre de la base de datos existente
nombre_base_datos = 'canciones.db'
nombre_base_datos_copia = 'canciones_copia.db'

# Verificar si la base de datos de copia ya existe
if not os.path.exists(nombre_base_datos_copia):
    # Hacer una copia de la base de datos original para trabajar con ella
    shutil.copyfile(nombre_base_datos, nombre_base_datos_copia)

# Conectarse a la base de datos
conexion = sqlite3.connect(nombre_base_datos_copia)
cursor = conexion.cursor()

# Función para mostrar la tabla de canciones


def mostrar_tabla_canciones():
    cursor.execute('SELECT * FROM canciones')
    filas = cursor.fetchall()
    if filas:
        encabezados = ["ID", "Canción", "Intérprete", "Año",
                       "Semanas", "País", "Idioma", "Continente"]
        print(tabulate(filas, headers=encabezados, tablefmt="grid"))
    else:
        print("La base de datos está vacía.")


# Agregar la columna "idioma" a la tabla "canciones" si no existe
cursor.execute('PRAGMA table_info(canciones)')
columnas = cursor.fetchall()
columnas_existentes = [columna[1] for columna in columnas]
if 'idioma' not in columnas_existentes:
    cursor.execute('ALTER TABLE canciones ADD COLUMN idioma TEXT')

# Agregar la columna "continente" a la tabla "canciones" si no existe
if 'continente' not in columnas_existentes:
    cursor.execute('ALTER TABLE canciones ADD COLUMN continente TEXT')

# Menú principal
while True:
    print("\nMENU:")
    print("1. Mostrar tabla extraida modificada con columnas de idioma y continente")
    print("2. Ingresar idioma registro por registro")
    print("3. Ingresar continente registro por registro")
    print("4. Salir")

    opcion = input("Ingrese el número de la opción que desea: ")

    if opcion == "1":
        mostrar_tabla_canciones()
    elif opcion == "2":
        cursor.execute('SELECT * FROM canciones WHERE idioma IS NULL')
        filas = cursor.fetchall()
        if filas:
            for registro in filas:
                id_registro, cancion, interprete, año, semanas, pais, idioma, continente = registro
                print(f"\nCanción: {cancion}")
                print(f"Intérprete: {interprete}")
                print(f"Año: {año}")
                print(f"Semanas: {semanas}")
                print(f"País: {pais}")
                idioma_ingresado = obtener_idioma_valido()
                if idioma_ingresado:
                    cursor.execute(
                        'UPDATE canciones SET idioma = ? WHERE id = ?', (idioma_ingresado, id_registro))
                    conexion.commit()
                else:
                    break
            print("\nSe han ingresado los idiomas correctamente.")
        else:
            print("No hay registros sin idioma para completar.")
    elif opcion == "3":
        cursor.execute('SELECT * FROM canciones WHERE continente IS NULL')
        filas = cursor.fetchall()
        if filas:
            for registro in filas:
                id_registro, cancion, interprete, año, semanas, pais, idioma, continente = registro
                print(f"\nCanción: {cancion}")
                print(f"Intérprete: {interprete}")
                print(f"Año: {año}")
                print(f"Semanas: {semanas}")
                print(f"País: {pais}")
                continente_ingresado = obtener_continente_valido()
                if continente_ingresado:
                    cursor.execute(
                        'UPDATE canciones SET continente = ? WHERE id = ?', (continente_ingresado, id_registro))
                    conexion.commit()
                else:
                    break
            print("\nSe han ingresado los continentes correctamente.")
        else:
            print("No hay registros sin continente para completar.")
    elif opcion == "4":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")
