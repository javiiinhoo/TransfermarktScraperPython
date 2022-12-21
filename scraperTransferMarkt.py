# importamos todas las librerías necesarias para el programa
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# TransferMarkt tiene antiscraper por lo que declaramos una cabecera html con un user agent
headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# declaramos todos los arrays necesarios para el posterior dataframe
todos_datos = []
nombres_sin_truncar = []
nombres_jugadores = []
pais_jugadores = []
equipos_jugadores = []
precios_jugadores = []
alineaciones_jugadores = []
edad_jugadores = []
goles_jugadores = []
goles_propia_jugadores = []
asistencias_jugadores = []
amarillas_jugadores = []
segundas_amarillas_jugadores = []
rojas_jugadores = []
entran_cambio_jugadores = []
salen_cambio_jugadores = []


# bucle principal de consultas y de lectura de los datos de la página
for pagenum in range(1, 21):
    page = "https://www.transfermarkt.es/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=0&kontinent_id=0&plus=1&page=" + \
        str(pagenum)
    response = requests.get(page, headers=headers)
    html = BeautifulSoup(response.content, 'html.parser')
    # consultas html
    jugadores = html.find_all('td', {"class":"hauptlink"})
    precios = html.find_all("td", {"class": "rechts"})
    datos = html.find_all("td", {"class": "zentriert"})
    banderas = html.find_all("img", {"class": "flaggenrahmen"}, {"title": True})
    # bucle de generación de los subarrays
    for p in range(0, 25):
        while ("" in todos_datos):
            todos_datos.remove("")
        edad_jugadores.append(datos[1 + (13*p)].text)
        alineaciones_jugadores.append(datos[4 + (13*p)].text)
        goles_jugadores.append(datos[5 + (13*p)].text)
        goles_propia_jugadores.append(datos[6 + (13*p)].text)
        asistencias_jugadores.append(datos[7 + (13*p)].text)
        amarillas_jugadores.append(datos[8 + (13*p)].text)
        segundas_amarillas_jugadores.append(datos[9 + (13*p)].text)
        rojas_jugadores.append(datos[10 + (13*p)].text)
        salen_cambio_jugadores.append(datos[11 + (13*p)].text)
        entran_cambio_jugadores.append(datos[12 + (13*p)].text)

    for bandera in banderas:
        pais_jugadores.append(bandera.text)

    # bucles de llenado de arrays
    for jugador in jugadores:
        # empleamos un array auxiliar puesto que la consulta html realizada devuelve una dupla de datos (hay 2 etiquetas a por fila)
        nombres_sin_truncar.append(jugador.text)
    nombres_jugadores=nombres_sin_truncar[::2]

    for precio in precios:
        texto_precio = precio.text
        # reemplazamos los caracteres que quedan de vacío
        texto_precio = texto_precio.replace("\xa0", "")
        precios_jugadores.append(texto_precio)

    for i in datos:
        imagen_pais = i.find(
            "img", {"class": "flaggenrahmen"}, {"title": True})
        if (imagen_pais != None):  # si no tiene una imagen inexistente guardamos el title de la misma (nombre del país)
            pais_jugadores.append(imagen_pais['title'])
        while ("" in pais_jugadores):
            pais_jugadores.remove("")

    for j in datos:
        equipo_jugador = j.find(
            "a", {"title": True})
        if (equipo_jugador != None):  # si el jugador tiene equipo añadiremos el nombre del mismo
            equipos_jugadores.append(equipo_jugador['title'])

df = pd.DataFrame({'Jugador': nombres_jugadores,
                   'Edad': edad_jugadores,
                   'Nacionalidad': pais_jugadores,
                   'Club': equipos_jugadores,
                   'Valor de mercado': precios_jugadores,
                   'Alineaciones': alineaciones_jugadores,
                   'Goles anotados': goles_jugadores,
                   'Goles en propia puerta': goles_propia_jugadores,
                   'Asistencias': goles_propia_jugadores,
                   'Tarjetas amarillas': goles_propia_jugadores,
                   'Segundas amarillas': goles_propia_jugadores,
                   'Tarjetas rojas': goles_propia_jugadores,
                   'Veces cambiado': salen_cambio_jugadores,
                   'Entra de suplente': entran_cambio_jugadores
                   })
df.index = df.index + 1 #el index por defecto empieza en 0 pero queremos que sea el 1 al comienzo 
print(df) #imprimimos el dataframe

# exportamos el dataframe a un .xlsx en el escritorio del usuario
df.to_csv(os.path.expanduser('~/Desktop\\') + r' data.csv',
          index=False, header=True)