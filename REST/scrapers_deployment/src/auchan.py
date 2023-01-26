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

        if img := jsonDic["image"]:
            img = jsonDic["image"][0]

        objProduto = {"Nome": nome, "Marca": brand, "Quantidade": qnt, unidecode(
            "Preço Primário"): preco, unidecode("Preço Por Unidade"): ppu, "Promo": promo, "EAN": ean, "Link Imagem": img, "Link Produto": link}
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
            "Nome": "bolacha bahlsen waffer waffeleten 100g",
            "Marca": "bahlsen",
            "Quantidade": "0.1 KG",
            "Preco Primario": "2.49",
            "Preco Por Unidade": "24.9 \u20ac/Kg",
            "Promo": None,
            "EAN": "4017100219900",
            "Link Imagem": "https://www.auchan.pt/on/demandware.static/-/Sites-auchan-pt-master-catalog/default/dw0c614f5f/images/hi-res/000000105.jpg",
            "Link Produto": "https://www.auchan.pt/pt/alimentacao/mercearia/bolachas-e-bolos/bolachas-recheadas-e-waffers/bolacha-bahlsen-waffer-waffeleten-100g/105.html"
        },
        {
            "Nome": "flocos salutem centeio integral 375g",
            "Marca": "salutem",
            "Quantidade": "0.375 KG",
            "Preco Primario": "1.09",
            "Preco Por Unidade": "2.91 \u20ac/Kg",
            "Promo": None,
            "EAN": "5601557003138",
            "Link Imagem": "https://www.auchan.pt/on/demandware.static/-/Sites-auchan-pt-master-catalog/default/dw44af3d89/images/hi-res/000001006.jpg",
            "Link Produto": "https://www.auchan.pt/pt/alimentacao/dietetica/mercearia-dietetica/cereais-flocos-e-granolas/flocos-salutem-centeio-integral-375g/1006.html"
        },
        {
            "Nome": "soja salutem nacos 400g",
            "Marca": "salutem",
            "Quantidade": "0.4 KG",
            "Preco Primario": "1.89",
            "Preco Por Unidade": "4.73 \u20ac/Kg",
            "Promo": None,
            "EAN": "5601557005095",
            "Link Imagem": "https://www.auchan.pt/on/demandware.static/-/Sites-auchan-pt-master-catalog/default/dw1b5e7a21/images/hi-res/000001043.jpg",
            "Link Produto": "https://www.auchan.pt/pt/biologicos-e-escolhas-alimentares/alimentacao-vegetariana/soja-salutem-nacos-400g/1043.html"
        }
    ]

    # f = open('auchan.json', 'w')
    # f.write(json.dumps(data))

    print('auchan doing request...')
    response = requests.post("http://api:8080/api/v1/auchan/products",
                             json=data, timeout=30)
    print('response status to auchan:')
    print(response.status_code)


def main():
    getInfoProdutos()


if __name__ == "__main__":
    main()
