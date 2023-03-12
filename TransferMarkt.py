import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ini = time.time()
ua = UserAgent()
headers = {'user-agent': ua.random}
nombres_competiciones = []

datos_jugadores = []
datos_transfers = []
datos_equipos = []
datos_lesiones = []

urls_continentes = ['https://www.transfermarkt.es/wettbewerbe/europa',
                    'https://www.transfermarkt.es/wettbewerbe/afrikahttps://www.transfermarkt.es/wettbewerbe/asien', 'https://www.transfermarkt.es/wettbewerbe/amerika']
urls_ligas = [
    'https://www.transfermarkt.es/premier-league/startseite/wettbewerb/GB1']
urls_equipos = list({f"https://www.transfermarkt.es{link['href']}"for url_liga in urls_ligas for td in BeautifulSoup(requests.get(
    url_liga, headers=headers).content, 'html.parser').find_all('td', class_='hauptlink')for link in td.find_all('a', href=lambda href: href and '/startseite/verein/' in href)})
urls_jugadores = list(dict.fromkeys((f"https://www.transfermarkt.es{link['href']}"for url_equipo in urls_equipos for link in BeautifulSoup(
    requests.get(url_equipo, headers=headers).content, 'html.parser').find_all('a', href=lambda href: href and 'profil/spieler/' in href))))
for url_jugador in urls_jugadores:
    soup = BeautifulSoup(requests.get(
        url_jugador, headers=headers).content, 'html.parser')
    jugador = {}
    transfer = {}
    lesiones = {}
    equipos = {}
    detalles = soup.find('div', {'class': 'info-table--right-space'})
    id_jugador = url_jugador.split('/')[-1]
    if id_jugador is not None:
        jugador['Id_Jugador'] = id_jugador
    try:
        nombre = ' '.join([texto.strip()if isinstance(texto, str)else texto.text.strip()for texto in soup.find(
            'h1', class_='data-header__headline-wrapper').contents if texto.name != 'span'])
        if nombre is not None:
            jugador['Nombre_jugador'] = nombre.strip()

    except AttributeError:
        nombre = None
    
    try:
        nombre_completo = detalles.find('span', {
                                        'class': 'info-table__content info-table__content--regular'}, text='Nombre completo:')
        if nombre_completo is not None:
            jugador['Nombre_completo'] = nombre_completo.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Nombre_completo'] = None
    try:
        nombre_pais_origen = detalles.find('span', {
                                           'class': 'info-table__content info-table__content--regular'}, text='Nombre en país de origen:')
        if nombre_pais_origen:
            jugador['Nombre_en_pais_origen'] = nombre_pais_origen.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
        else:
            jugador['Nombre_en_pais_origen'] = None
    except AttributeError:
        jugador['Nombre_en_pais_origen'] = None
    try:
        fecha_nacimiento = detalles.find('span', {
                                         'class': 'info-table__content info-table__content--regular'}, text='Fecha de nacimiento:')
        if fecha_nacimiento is not None:
            siguiente_etiqueta = fecha_nacimiento.find_next()
            if siguiente_etiqueta.name == 'a':
                jugador['Fecha_nacimiento'] = siguiente_etiqueta.text.strip()
            elif siguiente_etiqueta.name == 'span':
                fecha_texto = siguiente_etiqueta.text.strip()
                if fecha_texto:
                    jugador['Fecha_nacimiento'] = fecha_texto
                else:
                    jugador['Fecha_nacimiento'] = None
            else:
                jugador['Fecha_nacimiento'] = None
    except AttributeError:
        jugador['Fecha_nacimiento'] = None
    try:
        lugar_nacimiento = detalles.find('span', {
            'class': 'info-table__content info-table__content--regular'}, text='Lugar de nacimiento:')
        if lugar_nacimiento is not None:
            img_tags = lugar_nacimiento.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).find_all('img')
            if len(img_tags) > 0:
                jugador['Lugar_nacimiento'] = img_tags[0].get('title')
            else:
                jugador['Lugar_nacimiento'] = None
    except AttributeError:
        jugador['Lugar_nacimiento'] = None

    try:
        edad = detalles.find('span', {
                             'class': 'info-table__content info-table__content--regular'}, text='Edad:')
        if edad is not None:
            jugador['Edad'] = edad.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Edad'] = None
    try:
        altura = detalles.find('span', {
                               'class': 'info-table__content info-table__content--regular'}, text='Altura:')
        if altura is not None:
            jugador['Altura'] = altura.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Altura'] = None
    try:
        posicion = detalles.find('span', {
                                 'class': 'info-table__content info-table__content--regular'}, text='Posición:')
        if posicion is not None:
            jugador['Posicion'] = posicion.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Posicion'] = None
    try:
        pie = detalles.find(
            'span', {'class': 'info-table__content info-table__content--regular'}, text='Pie:')
        if pie is not None:
            jugador['Pie'] = pie.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Pie'] = None
    try:
        agente = detalles.find('span', {
                               'class': 'info-table__content info-table__content--regular'}, text='Agente:')
        if agente is not None:
            siguiente_etiqueta = agente.find_next()
            if siguiente_etiqueta.name == 'a':
                jugador['Agente'] = siguiente_etiqueta.text.strip()
            elif siguiente_etiqueta.name == 'span':
                agente_texto = siguiente_etiqueta.text.strip()
                if agente_texto:
                    jugador['Agente'] = agente_texto
                else:
                    jugador['Agente'] = None
            else:
                jugador['Agente'] = None
    except AttributeError:
        jugador['Agente'] = None
    try:
        club_actual = soup.find(
            'span', {'class': 'data-header__club'}).find('a').text.strip()
        if club_actual is not None:
            jugador['Club_actual'] = club_actual
    except AttributeError:
        jugador['Club_actual'] = None
    try:
        fichado = detalles.find('span', {
                                'class': 'info-table__content info-table__content--regular'}, text='Fichado:')
        if fichado is not None:
            jugador['Fichado'] = fichado.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Fichado'] = None
    try:
        contrato_hasta = detalles.find('span', {
                                       'class': 'info-table__content info-table__content--regular'}, text='Contrato hasta:')
        if contrato_hasta is not None:
            jugador['Fin contrato'] = contrato_hasta.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Fin contrato'] = None
    try:
        ultima_renovacion = detalles.find('span', {
                                          'class': 'info-table__content info-table__content--regular'}, text='Última renovación:')
        if ultima_renovacion is not None:
            jugador['Ultima_renovacion'] = ultima_renovacion.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Ultima_renovacion'] = None
    try:
        proveedor = detalles.find('span', {
                                  'class': 'info-table__content info-table__content--regular'}, text='Proveedor:')
        if proveedor is not None:
            jugador['Proveedor'] = proveedor.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()
    except AttributeError:
        jugador['Proveedor'] = None
    try:
        valor_mercado = soup.find(
            'div', {'class': 'tm-player-market-value-development__current-value'}).text.strip()
        if valor_mercado is not None:
            jugador['Valor mercado'] = valor_mercado
    except AttributeError:
        valor_mercado = None
    datos_jugadores.append(jugador)
df = pd.DataFrame(datos_jugadores)
df = df.sort_values(by=['Club_actual']).reindex(columns=['Id_Jugador', 'Nombre_jugador', 'Nombre_completo', 'Nombre_en_pais_origen', 'Fecha_nacimiento',
                                                         'Lugar_nacimiento', 'Agente', 'Edad', 'Altura', 'Posicion', 'Pie', 'Club_actual', 'Fichado',
                                                         'Fin contrato', 'Ultima_renovacion', 'Proveedor', 'Valor mercado'])
df.to_csv(os.path.expanduser('~/Desktop\\') +
          'transfer_players.csv', index=False, header=True)
fin = time.time()
m, s = divmod(fin-ini, 60)
print(f"Tiempo de ejecución: {m:.0f} minuto(s) y {s:.2f} segundo(s)")
