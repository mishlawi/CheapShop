from bs4 import BeautifulSoup as BS
import requests
import re
import csv
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# options= Options()
# options.add_argument('--headless')
# s= Service('./chromedriver.exe')

# driver = webdriver.Chrome(service=s, options=options)
# driver.get("https://www.auchan.pt/")
#time.sleep(10000)

# sites = ['produtos-frescos','alimentacao','bebidas-e-garrafeira','limpeza-da-casa-e-roupa','beleza-e-higiene','o-mundo-do-bebe','biologicos-e-escolhas-alimentares','tecnologia-e-eletrodomesticos','saude-e-bem-estar','animais','tecnologia-e-eletrodomesticos','brinquedos-papelaria-e-livraria','casa-e-jardim','bricolage-e-renovacoes','automovel-desporto-e-outdoor','produtos-locais','loja-gourmet']

count=0

def getProdutos(link):
    s= requests.Session()
    xml = s.get(link).text
    soup = BS(xml,features='lxml')
    tags = soup.find_all("url")
    infoProdutos = []
    for produto in tags:
        infoProdutos.append(getProductInfo(produto.find("loc").text))
    
    return infoProdutos


def getProductInfo(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html,features='html.parser')
    try:
        tagJson = soup.find("script",type="application/ld+json").text
        jsonDic = json.loads(tagJson)
        nome = jsonDic["name"]
        preco = jsonDic["offers"]["price"] + '€'
        
        print(nome,preco)
        return nome,preco
    except:
        print(f"\nproduto removido do site, LINK para confirmar -> {link} \n")

def getInfoProdutos():
    #https://www.auchan.pt/sitemap_0-product.xml
    #https://www.auchan.pt/sitemap_1-product.xml
    produtos =[]
    links = getProdutos("https://www.auchan.pt/sitemap_1-product.xml") #! takes >1h

    


getInfoProdutos()