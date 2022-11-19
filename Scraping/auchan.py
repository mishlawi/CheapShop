from bs4 import BeautifulSoup as BS
import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

products = []
count = 0
def getProdutos(link):
    
    #xml = open('site.xml').read()
    s = requests.Session()
    xml = s.get(link).text
    soup = BS(xml,features='lxml')
    tags = soup.find_all("url")

    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for produto in tags:
            productWebsite = produto.find("loc").text
            threads.append(executor.submit(getProductInfo,productWebsite))


def getProductInfo(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html,features='html.parser')
    try:
        
        try:    #promotion
            tagPromocao = soup.find("span",class_="strike-through value")
            beforePrice = tagPromocao["content"] + '€'
        
        except TypeError:
            beforePrice = 'None'        
        
        tagJson = soup.find("script",type="application/ld+json").text
        jsonDic = json.loads(tagJson)
        nome = jsonDic["name"]
        preco = jsonDic["offers"]["price"] + '€'        
        ean = soup.find("span",class_="product-ean").text 
        ppu = soup.find("span",class_="auc-measures--price-per-unit").text
        qnt = 'None'
        if 'Quantidade Liquida' in soup.find("h3",class_="attribute-name auc-pdp-attribute-title").text:
            qnt = soup.find("li",class_="attribute-values auc-pdp-regular").text.strip()
        else: 
            if x:= re.search(r'((\d+)\.)?\d+((L|ML|KG|G)| ?(ml|ML|CL))|KG|(\d+)?UN',nome):
                qnt = x.group()
                qnt = qnt.upper()
                if qnt == 'KG':
                    qnt = '1 KG'
                elif qnt == 'LT':
                    qnt == '1 LT'
                elif qnt == 'UN':
                    qnt == '1 UN'

        products.append((nome,'None',qnt,preco,ppu,beforePrice,ean))


    except AttributeError:
       print(f"\nproduto removido do site, LINK para confirmar -> {link} \n")


    #https://www.auchan.pt/sitemap_0-product.xml
    #https://www.auchan.pt/sitemap_1-product.xml
    
def getInfoProdutos():
    getProdutos('https://www.auchan.pt/sitemap_0-product.xml')
    
    getProdutos('https://www.auchan.pt/sitemap_1-product.xml')
    
    fields = ['NAME','BRAND','QUANTITY','PRICE','PPU','OLDPRICE','EAN']
    print(products)
    with open('products.csv','w') as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for elem in products:
            csvwriter.writerow(elem)
   
    
#getProductInfo('https://www.auchan.pt/pt/beleza-e-higiene/maquilhagem-e-perfumes/perfumes-senhora/conjunto-sense-collection-calendario-advento-magical/3519949.html')
#getProductInfo('https://www.auchan.pt/pt/alimentacao/mercearia/bolachas-e-bolos/bolachas-recheadas-e-waffers/bolacha-bahlsen-waffer-waffeleten-100g/105.html')


def main():
    getInfoProdutos()

if __name__ == "__main__":
    main()