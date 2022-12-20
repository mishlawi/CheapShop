from bs4 import BeautifulSoup as BS
import requests

import csv
import os
import re

rows = set()


def getProdutosPagina(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html, "html.parser")
    titulo = soup.find(["meta"], property="og:description")["content"]

    tags = soup.find(["div"], class_="product-list--row")
    produtos = tags.find_all(["a"])


    for elem in produtos:

        # as a reminder:
        nomeProduto = elem.find(["span"], class_="details").text.strip()
        quantity = None

        marca = None
        if match := re.match(r'\b[A-ZÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ+\'-_:! ]+[^ I]\b', nomeProduto):
            marca = match[0].strip()
            nomeProduto = nomeProduto.replace(marca, '').strip()

        # marcaRegex = re.findall(r'[A-ZÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]{2,}', nomeProduto)
        # marca = ' '
        # for regex in marcaRegex:
        #     marca += regex + ' '
        # marca = marca.strip()

        if quantity := re.search(r'(\(\d+[^()]+?\)|\d+((x|,|\.)\d+)?([^0-9()a-zA-Z]+)?(\w{,3}|unidades))$', nomeProduto):
            quantity = quantity.group(0)
            nomeProduto = nomeProduto.replace(quantity, '').strip()

        # tag com a tag com o preço e a tag com o preço/kg
        tagPrecosGeral = elem.find(["div"], class_="price_container")
        tagPrecos = tagPrecosGeral.find(
            ["p"], class_="price")  # tag com o preço
        # tag com o preço por kilo/preço por unidade
        tagPrecosKg = tagPrecosGeral.find(["p"], class_="pricePerKilogram")

        oldPrice = None
        oldPriceKg = None
        promo = None

        if old := tagPrecos.find(["s"]):  # ! significa que sofreu uma promoção
            oldPrice = float(old.text.strip().replace(',', '.')[:-1])
            old.string = ''
            promo = float(tagPrecos.text.strip().replace(',', '.')[:-1])
        else:
            if tagPrecos.text.strip():
                oldPrice = float(tagPrecos.text.strip().replace(',', '.')[:-1])
            else:
                oldPrice = 'Indisponível'

        if tagPrecosKg:
            # ! significa que sofreu uma promoção
            if old := tagPrecosKg.find(["s"]):
                oldPriceKg = tagPrecosKg.text.strip()
                oldPriceKg = oldPriceKg[oldPriceKg.find(
                    "(")+1:oldPriceKg.find(")")].replace('.', '')
                old.string = ''
            else:
                oldPriceKg = tagPrecosKg.text.strip()
                oldPriceKg = oldPriceKg[oldPriceKg.find(
                    "(")+1:oldPriceKg.find(")")].replace('.', '')
        else:
            pass  # data-productCode

        #! Ha um codigo de produto (penso que seja só interno)
        # adding old price and old price per unit and then the promo price, if no promo, field stays blank
        rows.add((nomeProduto, marca, quantity,
                  oldPrice, oldPriceKg, promo))

    nextpage = soup.find(["li"], class_="next").find(["a"])["href"]
    if not nextpage == '#':
        getProdutosPagina("https://www.minipreco.pt" + nextpage)


def getPaginas(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html, "html.parser")
    paginasTag = soup.find(["ul"], class_="nav-submenu")
    paginas = paginasTag.find_all(["div"], class_="category-link")


    # CSV BUILD

    campos = ['Nome', 'Marca', 'Quantidade',
              'Preço Primário', 'Preço Por Unidade', 'Promo']

    if not os.path.exists("csvProdutos"):
        os.makedirs("csvProdutos")
    file = 'csvProdutos/ProdutosMP.csv'
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    links = []
    for pagina in paginas:
        linkIncomplete = pagina.find(["a"])["href"]
        categoria = pagina.find(["a"]).text.strip().split('-')[0]
        link = "https://www.minipreco.pt" + str(linkIncomplete)
        links.append((categoria, link))

    for elem in links:
        getProdutosPagina(elem[1])
        print("---->" + elem[0] + "     FEITO")

    csvwriter.writerows(rows)

getPaginas("https://www.minipreco.pt")
