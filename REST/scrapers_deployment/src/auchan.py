from bs4 import BeautifulSoup as BS
import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from unidecode import unidecode

data = []


def getProdutos(link):
    s = requests.Session()
    xml = s.get(link).text
    soup = BS(xml, features='lxml')
    tags = soup.find_all("url")

    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for produto in tags:
            productWebsite = produto.find("loc").text
            threads.append(executor.submit(getProductInfo, productWebsite))


def getProductInfo(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html, features='html.parser')
    try:
        tagJson = soup.find("script", type="application/ld+json").text
        jsonDic = json.loads(tagJson)
        if nome := jsonDic["name"]:
            nome = unidecode(jsonDic["name"].lower().replace('-', ' '))
        preco = jsonDic["offers"]["price"]
        if soup.find("span", class_="strike-through value") != None:
            tagOldPrice = soup.find("span", class_="strike-through value")
            preco = tagOldPrice["content"]
            promo = jsonDic["offers"]["price"]
        else:
            promo = None

        ean = soup.find("span", class_="product-ean").text
        if soup.find("span", class_="auc-measures--price-per-unit") != None:
            ppu = soup.find("span", class_="auc-measures--price-per-unit").text
        else:
            ppu = preco
        qnt = None
        try:
            brandTag = soup.find("script", type="application/ld+json").text
            brandJson = json.loads(brandTag)
            if brand := brandJson["brand"]["name"]:
                brand = unidecode(
                    brandJson["brand"]["name"].lower().replace('-', ' '))

        except KeyError:
            brand = None

        if soup.find("h3", class_="attribute-name auc-pdp-attribute-title") != None and 'Quantidade Liquida' in soup.find("h3", class_="attribute-name auc-pdp-attribute-title").text:
            qnt = soup.find(
                "li", class_="attribute-values auc-pdp-regular").text.strip()
        else:
            if x := re.search(r'((\d+)\.)?\d+((L|ML|KG|G)| ?(ml|ML|CL))|KG|(\d+)?UN', nome):
                qnt = x.group()
                qnt = qnt.upper()
                if qnt == 'KG':
                    qnt = '1 KG'
                elif qnt == 'LT':
                    qnt == '1 LT'
                elif qnt == 'UN':
                    qnt == '1 UN'

        objProduto = {"Nome": nome, "Marca": brand, "Quantidade": qnt, unidecode(
            "Preço Primário"): preco, unidecode("Preço Por Unidade"): ppu, "Promo": promo, "EAN": ean}
        if not objProduto in data:
            data.append(objProduto)

    except AttributeError:
        print(f"\nproduto removido do site, LINK para confirmar -> {link} \n")


def getInfoProdutos():
    # print("Starting..")
    # getProdutos('https://www.auchan.pt/sitemap_0-product.xml')
    # print("Finished first sitemap..")
    # getProdutos('https://www.auchan.pt/sitemap_1-product.xml')
    # print("Finished second sitemap...")

    data = [
        {
            "Nome": "x storck toffifee 125g",
            "Marca": "storck",
            "Quantidade": "0.125 KG",
            "Preco Primario": "3.85",
            "Preco Por Unidade": "24 €/Kg",
            "Promo": "3.00",
            "EAN": "4014200400007"
        },
        {
            "Nome": "x pescanova pescada do cabo 400g",
            "Marca": "pescanova",
            "Quantidade": "0.4 KG",
            "Preco Primario": "4.99",
            "Preco Por Unidade": "12.48 €/Kg",
            "Promo": None,
            "EAN": "8420063034515"
        },
        {
            "Nome": "x branco faisao 1l",
            "Marca": "faisao",
            "Quantidade": None,
            "Preco Primario": "2.19",
            "Preco Por Unidade": "2.19 €/Lt",
            "Promo": None,
            "EAN": "5621239329747"
        },
        {
            "Nome": "x pescanova pescada no5 para cozer 800g",
            "Marca": "hey im working",
            "Quantidade": "0.8 KG",
            "Preco Primario": "13.99",
            "Preco Por Unidade": "17.49 €/Kg",
            "Promo": None,
            "EAN": "8410963005232"
        }
    ]

    print('auchan doing request...')
    response = requests.post("http://api:8080/api/v1/auchan/products",
                             json=data, timeout=30)
    print('response status to auchan:')
    print(response.status_code)


def main():
    getInfoProdutos()


if __name__ == "__main__":
    main()
