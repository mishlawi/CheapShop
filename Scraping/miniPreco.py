from bs4 import BeautifulSoup as BS
import requests

import csv
import os
import re

rows = set()


def getProdutosPagina(link):

    html = requests.get(link).text
    soup = BS(html, "html.parser")
    titulo = soup.find(["meta"], property="og:description")["content"]

    tags = soup.find(["div"], class_="product-list--row")
    produtos = tags.find_all(["a"])

    # CSV BUILD

    campos = ['Nome', 'Preço', 'Preço Antigo', 'PpU',
              'PpU Antigo']     # PpU = Preço por Unidade
    ['Nome', 'Marca', 'Quantidade', 'Preço Primário', 'Preço Por Unidade', 'Promo']

    if not os.path.exists("ProdutosMP"):
        os.makedirs("ProdutosMP")
    file = 'ProdutosMP/' + titulo.replace(" ", "").lower()+'.csv'
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    for elem in produtos:

        # as a reminder:
        nomeProduto = elem.find(["span"], class_="details").text.strip()

        marcaRegex = re.findall(r'[A-Z]{2,}', nomeProduto)
        marca = None
        for regex in marcaRegex:
            marca += regex + ' '
        marca = marca.rstrip()
        # tag com a tag com o preço e a tag com o preço/kg
        tagPrecosGeral = elem.find(["div"], class_="price_container")
        tagPrecos = tagPrecosGeral.find(
            ["p"], class_="price")  # tag com o preço
        # tag com o preço por kilo/preço por unidade
        tagPrecosKg = tagPrecosGeral.find(["p"], class_="pricePerKilogram")

        quantity = None

        oldPrice = ''
        if old := tagPrecos.find(["s"]):  # ! significa que sofreu uma promoção
            oldPrice = old.text.strip()
            old.string = ''
        promo = tagPrecos.text.strip()
        if tagPrecos.text != "\n":

            oldPriceKg = ''
            # ! significa que sofreu uma promoção
            if old := tagPrecosKg.find(["s"]):
                oldPriceKg = old.text.strip()[1:-2]
                old.string = ''
            # not existent on other supermarkets so we're not adding this to the csv
            precopromoKg = tagPrecosKg.text.strip()[1:-2]

            #! Ha um codigo de produto (penso que seja só interno)
            # adding old price and old price per unit and then the promo price, if no promo, field stays blank
            rows.add((nomeProduto, marca, quantity,
                     oldPrice, oldPriceKg, promo))
        else:
            pass  # data-productCode

    nextpage = soup.find(["li"], class_="next").find(["a"])["href"]
    if nextpage == '#':
        csvwriter.writerows(rows)
        rows.clear()
    else:
        getProdutosPagina("https://www.minipreco.pt" + nextpage)


def getPaginas(link):
    html = requests.get(link).text
    soup = BS(html, "html.parser")
    paginasTag = soup.find(["ul"], class_="nav-submenu")
    paginas = paginasTag.find_all(["div"], class_="category-link")

    links = []
    for pagina in paginas:
        linkIncomplete = pagina.find(["a"])["href"]
        categoria = pagina.find(["a"]).text.strip().split('-')[0]
        link = "https://www.minipreco.pt" + str(linkIncomplete)
        links.append((categoria, link))

    for elem in links:
        getProdutosPagina(elem[1])
        print("---->" + elem[0] + "     FEITO")


getPaginas("https://www.minipreco.pt")
