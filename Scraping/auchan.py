from bs4 import BeautifulSoup as BS
import requests
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

products = set()

def getProdutos(link):
    #xml = open("site.xml").read()
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
        tagJson = soup.find("script",type="application/ld+json").text
        jsonDic = json.loads(tagJson)
        nome = jsonDic["name"]
        preco = jsonDic["offers"]["price"] + '€'        
        if soup.find("span",class_="strike-through value")!=None:
            tagOldPrice = soup.find("span",class_="strike-through value")
            preco = tagOldPrice["content"] + '€'
            promo = jsonDic["offers"]["price"] + '€'        
        else:
            promo = 'None'        
        
        ean = soup.find("span",class_="product-ean").text
        if soup.find("span",class_="auc-measures--price-per-unit")!=None: 
            ppu = soup.find("span",class_="auc-measures--price-per-unit").text
        else:
            ppu = preco
        qnt = 'None'
        try:
            brandTag = soup.find("script",type="application/ld+json").text
            brandJson = json.loads(brandTag)
            brand = brandJson["brand"]["name"]
        
        except KeyError:
            brand = 'None'
        
        if soup.find("h3",class_="attribute-name auc-pdp-attribute-title") != None and 'Quantidade Liquida' in soup.find("h3",class_="attribute-name auc-pdp-attribute-title").text:
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

        products.add((nome,brand,qnt,preco,ppu,promo,ean))


    except AttributeError:
       print(f"\nproduto removido do site, LINK para confirmar -> {link} \n")



#https://www.auchan.pt/sitemap_0-product.xml
#https://www.auchan.pt/sitemap_1-product.xml
    
def getInfoProdutos():
    print("Starting..")
    getProdutos('https://www.auchan.pt/sitemap_0-product.xml')
    print("Finished first sitemap..")
    getProdutos('https://www.auchan.pt/sitemap_1-product.xml')
    print("Finished second sitemap...")
    
    print("Writing in csv")
    fields = ['Nome', 'Marca', 'Quantidade',
              'Preço Primário', 'Preço Por Unidade', 'Promo','EAN']
    #print(products)
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