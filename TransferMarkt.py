# librerías a usar
from collections import defaultdict
import math
import re
import requests
import os
import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ini = time.time()
ua = UserAgent()
# declaramos cabeceras aleatorias con User-Agent
headers = {'user-agent': ua.random}

nombres_competiciones = []

# en esta lista irán todos los dicts de los jugadores.
datos_totales = []

# en este dict guardamos los datos que obtenemos por cada jugador
datos = {}

# recorremos las ligas

""" urls_continentes = [""" "https://www.transfermarkt.es/wettbewerbe/europa", "https://www.transfermarkt.es/wettbewerbe/afrika",
"https://www.transfermarkt.es/wettbewerbe/asien",  """"https://www.transfermarkt.es/wettbewerbe/amerika"]

# recorremos las URLs de los continentes y obtenemos las URLs de las ligas de cada uno
max_page_num = 18  # por ejemplo, límite de páginas a recorrer
urls_ligas = ['https://www.transfermarkt.es' + link['href'] for url_continente in urls_continentes for page_num in range(1, max_page_num+1)
              for link in BeautifulSoup(requests.get(url_continente + f'?page={page_num}', headers=headers).content, 'html.parser')
              .find_all('a', href=lambda href: href and '/wettbewerb/' in href)[1::2]]

# recorremos las URLs de las ligas
print(len(urls_ligas))

print(urls_ligas) """
urls_ligas = [
    "https://www.transfermarkt.es/premier-league/startseite/wettbewerb/GB1"]

urls_equipos = list({f'https://www.transfermarkt.es{link["href"]}'
                     for url_liga in urls_ligas
                     for td in BeautifulSoup(requests.get(url_liga, headers=headers).content, 'html.parser').find_all('td', class_='hauptlink')
                     for link in td.find_all('a', href=lambda href: href and '/startseite/verein/' in href)})

urls_jugadores = list(dict.fromkeys(f"https://www.transfermarkt.es{link['href']}" for url_equipo in urls_equipos for link in BeautifulSoup(
    requests.get(url_equipo, headers=headers).content, 'html.parser').find_all('a', href=lambda href: href and 'profil/spieler/' in href)))


for url_jugador in urls_jugadores:
    soup = BeautifulSoup(requests.get(
        url_jugador, headers=headers).content, 'html.parser')

    jugador = {}

    # Buscar información de detalles
    detalles = soup.find('div', {'class': 'info-table--right-space'})

    # Buscar información del idjugador

    id_jugador = url_jugador.split('/')[-1]
    if id_jugador is not None:
        jugador['Id_Jugador'] = id_jugador

    # Buscar información del nombre jugador

    nombre = ' '.join([texto.strip() if isinstance(texto, str) else texto.text.strip()
                       for texto in soup.find('h1', class_='data-header__headline-wrapper').contents if texto.name != 'span'])
    if nombre is not None:
        jugador['Nombre_jugador'] = nombre

    # Buscar información de nombre completo

    nombre_completo = detalles.find(
        'span', {'class': 'info-table__label'}, text='Nombre completo:')
    if nombre_completo is not None:
        nombre_completo = ' '.join([texto.strip() if isinstance(texto, str) else texto.text.strip()
                                    for texto in nombre_completo.contents if texto.name != 'span'])
        jugador['Nombre_completo'] = nombre_completo

    # Buscar información de nombre pais origen

    nombre_pais_origen = detalles.find(
        'span', {'class': 'info-table__label'}, text='Nombre completo:')
    if nombre_pais_origen is not None:
        nombre_pais_origen = ' '.join([texto.strip() if isinstance(texto, str) else texto.text.strip()
                                       for texto in nombre_pais_origen.contents if texto.name != 'span'])
        jugador['Nombre_en_pais_origen'] = nombre_pais_origen

    # Buscar información de fecha de nacimiento
    fecha_nacimiento = detalles.find(
        'span', {'class': 'info-table__label'}, text='Fecha de nacimiento')
    if fecha_nacimiento is not None:
        jugador['Fecha_nacimiento'] = fecha_nacimiento.find_next(
            'span', {'class': 'info-table__content'}).text.strip()

    # Buscar información de lugar de nacimiento
    lugar_nacimiento = detalles.find(
        'span', {'class': 'info-table__label'}, text='Lugar de nacimiento')
    if lugar_nacimiento is not None:
        img = lugar_nacimiento.find_next(
            'span', {'class': 'info-table__content'}).find_all('img')
        jugador['Lugar_nacimiento'] = img.get('title')

    # Buscar información de agente
    agente = detalles.find('span', {
                           'class': 'info-table__content info-table__content--regular'}, text='Agente:')
    if agente is not None:
        siguiente_etiqueta = agente.find_next()
        if siguiente_etiqueta.name == 'a':
            jugador['Agente'] = siguiente_etiqueta.text.strip()
        else:
            jugador['Agente'] = siguiente_etiqueta.find_next(
                'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información de edad
    edad = detalles.find(
        'span', {'class': 'info-table__label'}, text='Edad:')
    if edad is not None:
        jugador['Edad'] = edad.find_next(
            'span', {'class': 'info-table__content'}).text.strip()

    # Buscar información de altura
    altura = detalles.find(
        'span', {'class': 'info-table__label'}, text='Altura:')
    if altura is not None:
        jugador['Altura'] = altura.find_next(
            'span', {'class': 'info-table__content'}).text.strip()

    # Buscar información de posición
    posicion = detalles.find(
        'span', {'class': 'info-table__label'}, text='Posición:')
    if posicion is not None:
        jugador['Posicion'] = posicion.find_next(
            'span', {'class': 'info-table__content'}).text.strip()

    # Buscar información de pie
    pie = detalles.find('span', {
        'class': 'info-table__content info-table__content--regular'}, text='Pie:')
    if pie is not None:
        jugador['Pie'] = pie.find_next(
            'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información del club actual
    club_actual = soup.find(
        'span', {'class': 'data-header__club'}).find('a').text.strip()
    if club_actual is not None:
        jugador['Club_actual'] = club_actual

    # Buscar información de fichado
    fichado = detalles.find('span', {
        'class': 'info-table__content info-table__content--regular'}, text='Fichado:')
    if fichado is not None:
        jugador['Fichado'] = fichado.find_next(
            'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información de contrato hasta
    contrato_hasta = detalles.find('span', {
                                   'class': 'info-table__content info-table__content--regular'}, text='Contrato hasta:')
    if contrato_hasta is not None:
        jugador['Fin contrato'] = contrato_hasta.find_next(
            'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información de última renovación
    ultima_renovacion = detalles.find('span', {
                                      'class': 'info-table__content info-table__content--regular'}, text='Última renovación:')
    if ultima_renovacion is not None:
        jugador['Ultima_renovacion'] = ultima_renovacion.find_next(
            'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información de proveedor
    proveedor = detalles.find('span', {
                              'class': 'info-table__content info-table__content--regular'}, text='Proveedor:')
    if proveedor is not None:
        jugador['Proveedor'] = proveedor.find_next(
            'span', {'class': 'info-table__content info-table__content--bold'}).text.strip()

    # Buscar información de valor mercado

    valor_mercado = soup.find('div', {
        'class': 'tm-player-market-value-development__current-value'}).text.strip()

    if valor_mercado is not None:
        jugador['Valor mercado'] = valor_mercado

    datos_totales.append(jugador)
    print(datos_totales)
pd.DataFrame(datos_totales)
