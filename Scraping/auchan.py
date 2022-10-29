from bs4 import BeautifulSoup as BS
import requests
import re
import csv
import os
import json


# sites = ['produtos-frescos','alimentacao','bebidas-e-garrafeira','limpeza-da-casa-e-roupa','beleza-e-higiene','o-mundo-do-bebe','biologicos-e-escolhas-alimentares','tecnologia-e-eletrodomesticos','saude-e-bem-estar','animais','tecnologia-e-eletrodomesticos','brinquedos-papelaria-e-livraria','casa-e-jardim','bricolage-e-renovacoes','automovel-desporto-e-outdoor','produtos-locais','loja-gourmet']


# def getPaginas():
    
#     for site in sites:
#         link = 'https://www.auchan.pt/pt/' + site +'/'
#         print("\n**********************")
#         print(link)
        


# def getWithCategories(link):
    
#     html = requests.get(link).text
#     soup = BS(html,"html.parser")
#     categorias = soup.find("ul",class_="sub-categories__container")
#     links = [elem["href"] for elem in categorias.find_all("a")]
#     print(links)    

#getWithCategories("https://www.auchan.pt/pt/produtos-frescos/")





def getProdutos(link):
    xml = requests.get(link).text
    soup = BS(xml,features='lxml')
    tags = soup.find_all("url")
    infoProdutos = [getProductInfo(produto.find("loc").text) for produto in tags]
    
    return infoProdutos


def getProductInfo(link):
    html = requests.get(link).text
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