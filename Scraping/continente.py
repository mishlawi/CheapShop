from bs4 import BeautifulSoup as BS
import requests
import re
import csv
import os


def getPaginas(link):
    html = requests.get(link).text
    soup = BS(html,"html.parser")

    paginasTag = soup.find_all(["li"],class_="dropdown-item see-all",role="presentation")
    links = []
    for elem in paginasTag:
        link = elem.find(["a"])["href"]
        #if elem.text.strip()=='Ver todos':
        if elem.text.strip()=='Ver todos' and re.match(r'^https\:\/\/www\.continente\.pt\/\w+(\-\w+)*\/$',link):
            links.append(link)

    return links





getPaginas("https://www.continente.pt")