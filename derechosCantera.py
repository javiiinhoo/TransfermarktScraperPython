import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
ini = time.time()
ua = UserAgent()
headers = {'user-agent': ua.random}
nombres_competiciones = []
datos_transfers = []
urls_jugadores = ['https://www.transfermarkt.es/hugo-novoa/profil/spieler/668276',
                  'https://www.transfermarkt.es/trilli/profil/spieler/668272',
                  'https://www.transfermarkt.es/noel-lopez/profil/spieler/926854',
                  'https://www.transfermarkt.es/lucas-taibo/profil/spieler/1062520',
                  'https://www.transfermarkt.es/jorge-oreiro/profil/spieler/1106258',
                  'https://www.transfermarkt.es/oscar-pinchi/profil/spieler/413502',
                  'https://www.transfermarkt.es/diego-gomez/profil/spieler/941104',
                  'https://www.transfermarkt.es/alvaro-fernandez/profil/spieler/811778',
                  'https://www.transfermarkt.es/cristian-canales/profil/spieler/821072']
urls_jugadores = [url.replace('profil', 'transfers')for url in urls_jugadores]


def obtenerSeasons():
    now = datetime.datetime.now()
    current_year = now.year
    seasons = [f"{str(current_year-2)[-2:]}/{str(current_year-1)[-2:]}",
               f"{str(current_year-3)[-2:]}/{str(current_year-2)[-2:]}"]
    return seasons


for url_jugador in urls_jugadores:
    jugador = {}
    soup = BeautifulSoup(requests.get(
        url_jugador, headers=headers).content, 'html.parser')

    detalles = soup.find('div', {'class': 'box viewport-tracking'})
    try:
        nombre = ' '.join([texto.strip()if isinstance(texto, str)else texto.text.strip()for texto in soup.find(
            'h1', class_='data-header__headline-wrapper').contents if texto.name != 'span'])
        if nombre is not None:
            jugador['Nombre Jugador'] = nombre.strip()
    except AttributeError:
        nombre = None
    jugador['Enlace TM'] = url_jugador

    historial_traspasos = soup.find_all(
        'div', class_='grid tm-player-transfer-history-grid')
    temporadas_previas = obtenerSeasons()

    for traspaso in historial_traspasos:
        season = traspaso.find(
            'div', class_='tm-player-transfer-history-grid__season').text.strip()
        if season in temporadas_previas:
            jugador_temp = jugador.copy()
            jugador_temp['Temporada'] = season
            fecha = traspaso.find(
                'div', class_='tm-player-transfer-history-grid__date').text.strip()
            jugador_temp['Fecha'] = fecha
            ultimo_club = traspaso.find(
                'div', class_='tm-player-transfer-history-grid__old-club').text.strip()
            jugador_temp['Último club'] = ultimo_club
            nuevo_club = traspaso.find(
                'div', class_='tm-player-transfer-history-grid__new-club').text.strip()
            jugador_temp['Nuevo club'] = nuevo_club
            valor_mercado = traspaso.find(
                'div', class_='tm-player-transfer-history-grid__market-value').text.strip()
            jugador_temp['Valor de mercado'] = valor_mercado
            coste = traspaso.find(
                'div', class_='tm-player-transfer-history-grid__fee').text.strip()
            jugador_temp['Coste'] = coste
            datos_transfers.append(jugador_temp)
    print(datos_transfers)
df = pd.DataFrame(datos_transfers)
df.to_csv(os.path.expanduser('~/Desktop\\') +
          'derechosCantera.csv', index=False, header=True)
fin = time.time()
m, s = divmod(fin-ini, 60)
print(f"Tiempo de ejecución: {m:.0f} minuto(s) y {s:.2f} segundo(s)")
