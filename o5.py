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

# Función para obtener el continente válido del usuario


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

# Función para obtener la canción más antigua de la lista


def cancion_mas_antigua():
    cursor.execute('SELECT * FROM canciones ORDER BY año ASC LIMIT 1')
    cancion = cursor.fetchone()
    if cancion:
        print(
            f"La canción más antigua de la lista es '{cancion[1]}' interpretada por {cancion[2]} en el año {cancion[3]}.")
    else:
        print("No hay canciones en la lista.")

# Función para obtener el artista que aparece más veces en la lista


def artista_mas_frecuente():
    cursor.execute(
        'SELECT interprete, COUNT(*) AS cantidad FROM canciones GROUP BY interprete ORDER BY cantidad DESC LIMIT 1')
    artista = cursor.fetchone()
    if artista:
        print(
            f"El artista que aparece más veces en la lista es {artista[0]}, con {artista[1]} canciones.")
    else:
        print("No hay canciones en la lista.")

# Función para obtener el país con más artistas en la lista


def pais_con_mas_artistas():
    cursor.execute(
        'SELECT pais, COUNT(DISTINCT interprete) AS cantidad_artistas FROM canciones GROUP BY pais ORDER BY cantidad_artistas DESC LIMIT 1')
    pais = cursor.fetchone()
    if pais:
        print(
            f"El país con más artistas en la lista es {pais[0]}, con {pais[1]} artistas distintos.")
    else:
        print("No hay canciones en la lista.")

# Función para obtener la cantidad de canciones distintas por cada idioma


def canciones_por_idioma():
    cursor.execute(
        'SELECT idioma, COUNT(DISTINCT cancion) AS cantidad_canciones FROM canciones GROUP BY idioma')
    resultados = cursor.fetchall()
    if resultados:
        print("Cantidad de canciones distintas por cada idioma:")
        for resultado in resultados:
            print(
                f"- Idioma: {resultado[0]}, Canciones distintas: {resultado[1]}")
    else:
        print("No hay canciones en la lista.")

# Función para obtener el continente con más apariciones en la lista


def continente_mas_apariciones():
    cursor.execute(
        'SELECT continente, COUNT(*) AS cantidad FROM canciones GROUP BY continente ORDER BY cantidad DESC LIMIT 1')
    continente = cursor.fetchone()
    if continente:
        print(
            f"El continente con más apariciones en la lista es {continente[0]}, con {continente[1]} canciones.")
    else:
        print("No hay canciones en la lista.")

# Función para obtener la canción que ha estado más % de tiempo al año como número 1


def cancion_mas_tiempo_numero_1():
    cursor.execute('SELECT * FROM canciones')
    canciones = cursor.fetchall()
    if canciones:
        max_porcentaje = 0
        cancion_mas_tiempo = None
        for cancion in canciones:
            id_cancion, nombre_cancion, interprete, año, semanas, pais, idioma, continente = cancion
            # Calcular el porcentaje de tiempo que la canción estuvo como número 1
            porcentaje = (semanas / 52) * 100
            if porcentaje > max_porcentaje:
                max_porcentaje = porcentaje
                cancion_mas_tiempo = (nombre_cancion, interprete, porcentaje)
        if cancion_mas_tiempo:
            print(
                f"La canción que ha estado más % de tiempo al año como número 1 es '{cancion_mas_tiempo[0]}' interpretada por {cancion_mas_tiempo[1]}, con un porcentaje de tiempo del {cancion_mas_tiempo[2]:.2f}%.")
        else:
            print("No se encontró ninguna canción.")
    else:
        print("No hay canciones en la lista.")


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
    print("4. Consultas adicionales")
    print("5. Salir")

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
        # Submenú para consultas adicionales
        while True:
            print("\nSUBMENÚ - Consultas Adicionales:")
            print("1. ¿Cuál es la canción más antigua de la lista?")
            print("2. ¿Qué artista aparece más veces en esta lista?")
            print("3. ¿Qué país tiene más artistas en esta lista?")
            print("4. ¿Cuantas canciones distintas hay por cada idioma?")
            print("5. ¿Cuál es el continente con más apariciones en la lista?")
            print("6. ¿Qué canción ha estado más % de tiempo al año como número 1?")
            print("7. Volver al menú principal")

            opcion_sub = input("Ingrese el número de la opción que desea: ")

            if opcion_sub == "1":
                cancion_mas_antigua()
            elif opcion_sub == "2":
                artista_mas_frecuente()
            elif opcion_sub == "3":
                pais_con_mas_artistas()
            elif opcion_sub == "4":
                canciones_por_idioma()
            elif opcion_sub == "5":
                continente_mas_apariciones()
            elif opcion_sub == "6":
                cancion_mas_tiempo_numero_1()
            elif opcion_sub == "7":
                break
            else:
                print("Opción inválida. Por favor, ingrese un número válido.")
    elif opcion == "5":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")
