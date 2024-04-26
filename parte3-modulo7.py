import sqlite3
from tabulate import tabulate
import os
import unicodedata

# Función para eliminar los tildes de una cadena


def remover_tildes(cadena):
    return ''.join(char for char in unicodedata.normalize('NFD', cadena) if unicodedata.category(char) != 'Mn')


# Nombre de la base de datos existente
nombre_base_datos = 'canciones_copia.db'

# Verificar si la base de datos existe
if not os.path.exists(nombre_base_datos):
    print("La base de datos no existe.")
    exit()

# Conectarse a la base de datos
conexion = sqlite3.connect(nombre_base_datos)
cursor = conexion.cursor()

# Función para consultar la canción más antigua


def cancion_mas_antigua():
    cursor.execute('SELECT * FROM canciones ORDER BY año ASC LIMIT 1')
    cancion_antigua = cursor.fetchone()
    print("La canción más antigua de la lista es:")
    print(cancion_antigua)

# Función para consultar el artista más frecuente


def artista_mas_frecuente():
    cursor.execute('SELECT "Intérprete" FROM canciones')
    artistas = cursor.fetchall()

    # Crear un diccionario para contar las apariciones de cada artista
    conteo_artistas = {}
    for artista in artistas:
        interprete = artista[0]
        if interprete in conteo_artistas:
            conteo_artistas[interprete] += 1
        else:
            conteo_artistas[interprete] = 1

    # Encontrar el artista más frecuente
    artista_mas_frecuente, frecuencia = max(
        conteo_artistas.items(), key=lambda x: x[1])

    # Mostrar el resultado
    print(
        f"El artista que aparece más veces en la lista es: {artista_mas_frecuente}, con {frecuencia} apariciones.")


def pais_con_mas_artistas():
    cursor.execute('SELECT País, COUNT(DISTINCT ?) AS cantidad_artistas FROM canciones GROUP BY País ORDER BY cantidad_artistas DESC LIMIT 1',
                   (remover_tildes("Intérprete"),))
    pais_mas_artistas = cursor.fetchone()
    print("El país que tiene más artistas en la lista es:")
    print(pais_mas_artistas)

# Función para consultar el número de canciones por idioma


def canciones_por_idioma():
    cursor.execute(
        'SELECT Idioma, COUNT(DISTINCT Canción) AS cantidad_canciones FROM canciones GROUP BY Idioma')
    canciones_por_idioma = cursor.fetchall()
    print("El número de canciones distintas por cada idioma es:")
    print(tabulate(canciones_por_idioma, headers=[
          "Idioma", "Cantidad"], tablefmt="grid"))

# Función para consultar el continente con más apariciones


def continente_con_mas_apariciones():
    cursor.execute(
        'SELECT Continente, COUNT(*) AS cantidad_apariciones FROM canciones GROUP BY Continente ORDER BY cantidad_apariciones DESC LIMIT 1')
    continente_mas_apariciones = cursor.fetchone()
    print("El continente con más apariciones en la lista es:")
    print(continente_mas_apariciones)

# Función para consultar la canción que ha estado más % de tiempo al año como número 1


def cancion_mas_tiempo_numero_1():
    cursor.execute('SELECT Canción, (MAX(Semanas) * 100 / 52) AS porcentaje_tiempo_numero_1 FROM canciones WHERE Semanas = (SELECT MAX(Semanas) FROM canciones) GROUP BY Canción')
    canciones_mas_tiempo_numero_1 = cursor.fetchall()
    print("La(s) canción(es) que ha(n) estado más % de tiempo al año como número 1 es(són):")
    print(tabulate(canciones_mas_tiempo_numero_1, headers=[
          "Canción", "Porcentaje de tiempo como número 1"], tablefmt="grid"))


# Menú de interacción con el usuario
while True:
    print("\nMENU:")
    print("1. Consultar la canción más antigua de la lista")
    print("2. Consultar el artista que aparece más veces en la lista")
    print("3. Consultar el país que tiene más artistas en la lista")
    print("4. Consultar el número de canciones distintas por cada idioma")
    print("5. Consultar el continente con más apariciones en la lista")
    print("6. Consultar la canción que ha estado más % de tiempo al año como número 1")
    print("7. Salir")

    opcion = input("Ingrese el número de la opción que desea: ")

    if opcion == "1":
        cancion_mas_antigua()
    elif opcion == "2":
        artista_mas_frecuente()
    elif opcion == "3":
        pais_con_mas_artistas()
    elif opcion == "4":
        canciones_por_idioma()
    elif opcion == "5":
        continente_con_mas_apariciones()
    elif opcion == "6":
        cancion_mas_tiempo_numero_1()
    elif opcion == "7":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")

# Cerrar la conexión con la base de datos
conexion.close()

# Nombre de la base de datos existente
nombre_base_datos = 'canciones_copia.db'

# Verificar si la base de datos existe
if not os.path.exists(nombre_base_datos):
    print("La base de datos no existe.")
    exit()

# Conectarse a la base de datos
conexion = sqlite3.connect(nombre_base_datos)
cursor = conexion.cursor()

# Función para consultar la canción más antigua


def cancion_mas_antigua():
    cursor.execute('SELECT * FROM canciones ORDER BY año ASC LIMIT 1')
    cancion_antigua = cursor.fetchone()
    print("La canción más antigua de la lista es:")
    print(cancion_antigua)

# Función para consultar el artista más frecuente


def artista_mas_frecuente():
    cursor.execute(
        'SELECT "Intérprete", COUNT(*) AS cantidad FROM canciones GROUP BY unaccent("Intérprete") ORDER BY cantidad DESC LIMIT 1')
    artista_frecuente = cursor.fetchone()
    print("El artista que aparece más veces en la lista es:")
    print(artista_frecuente)

# Función para consultar el país con más artistas


def pais_con_mas_artistas():
    cursor.execute(
        'SELECT País, COUNT(DISTINCT unaccent("Intérprete")) AS cantidad_artistas FROM canciones GROUP BY País ORDER BY cantidad_artistas DESC LIMIT 1')
    pais_mas_artistas = cursor.fetchone()
    print("El país que tiene más artistas en la lista es:")
    print(pais_mas_artistas)


def canciones_por_idioma():
    cursor.execute(
        'SELECT Idioma, COUNT(DISTINCT Canción) AS cantidad_canciones FROM canciones GROUP BY Idioma')
    canciones_por_idioma = cursor.fetchall()
    print("El número de canciones distintas por cada idioma es:")
    print(tabulate(canciones_por_idioma, headers=[
          "Idioma", "Cantidad"], tablefmt="grid"))

# Función para consultar el continente con más apariciones


def continente_con_mas_apariciones():
    cursor.execute(
        'SELECT Continente, COUNT(*) AS cantidad_apariciones FROM canciones GROUP BY Continente ORDER BY cantidad_apariciones DESC LIMIT 1')
    continente_mas_apariciones = cursor.fetchone()
    print("El continente con más apariciones en la lista es:")
    print(continente_mas_apariciones)

# Función para consultar la canción que ha estado más % de tiempo al año como número 1


def cancion_mas_tiempo_numero_1():
    cursor.execute('SELECT Canción, (MAX(Semanas) * 100 / 52) AS porcentaje_tiempo_numero_1 FROM canciones WHERE Semanas = (SELECT MAX(Semanas) FROM canciones) GROUP BY Canción')
    canciones_mas_tiempo_numero_1 = cursor.fetchall()
    print("La(s) canción(es) que ha(n) estado más % de tiempo al año como número 1 es(són):")
    print(tabulate(canciones_mas_tiempo_numero_1, headers=[
          "Canción", "Porcentaje de tiempo como número 1"], tablefmt="grid"))


# Menú de interacción con el usuario
while True:
    print("\nMENU:")
    print("1. Consultar la canción más antigua de la lista")
    print("2. Consultar el artista que aparece más veces en la lista")
    print("3. Consultar el país que tiene más artistas en la lista")
    print("4. Consultar el número de canciones distintas por cada idioma")
    print("5. Consultar el continente con más apariciones en la lista")
    print("6. Consultar la canción que ha estado más % de tiempo al año como número 1")
    print("7. Salir")

    opcion = input("Ingrese el número de la opción que desea: ")

    if opcion == "1":
        cancion_mas_antigua()
    elif opcion == "2":
        artista_mas_frecuente()
    elif opcion == "3":
        pais_con_mas_artistas()
    elif opcion == "4":
        canciones_por_idioma()
    elif opcion == "5":
        continente_con_mas_apariciones()
    elif opcion == "6":
        cancion_mas_tiempo_numero_1()
    elif opcion == "7":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número válido.")

# Cerrar la conexión con la base de datos
conexion.close()
