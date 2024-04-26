import sqlite3
from collections import Counter
from tabulate import tabulate

# Conectarse a la base de datos
conn = sqlite3.connect('canciones_copia.db')
c = conn.cursor()

# Consulta SQL para obtener los datos de la tabla de canciones
c.execute("SELECT * FROM canciones")

# Obtener todos los resultados de la consulta
rows = c.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Convertir los datos en una lista de diccionarios
encabezado = ['ID', 'Canción', 'Intérprete', 'Año',
              'Semanas', 'País', 'Idioma', 'Continente']
datos = [dict(zip(encabezado, row)) for row in rows]

# Contar la frecuencia de los intérpretes
interprete_counter = Counter(d["Intérprete"] for d in datos)

# Encontrar el intérprete más común
interprete_mas_comun = interprete_counter.most_common(1)[0]

print("El intérprete que más se repite es:",
      interprete_mas_comun[0], "con", interprete_mas_comun[1], "ocurrencias.")
