import requests
from xml.dom import minidom
from re import *
import time
import csv
import json
from unidecode import unidecode
import os

SITEMAP = 'https://mercadao.pt/api/sitemap.xml'
APIIDS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/categories/slug/'
APIPRODUTOS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=["@catID@"]&from=@startPoint@&size=100&esPreference=0.6439211110152693'
FILENAME = 'csvProdutos/ProdutosPingoDoce.json'


def regra3simples(preco, quantidade, pretendido=1):
    return round(pretendido*float(preco)/float(quantidade), 2)


def getProdutosPagina():
    # CSV BUILD
    # campos = ['Nome', 'Marca', 'Quantidade',
    #           'Preço Primário', 'Preço Por Unidade', 'Promo', 'EAN']
    # file = f"csvProdutos/ProdutosPingoDoce.csv"
    # csvo = open(file, 'w')
    # csvwriter = csv.writer(csvo,delimiter=';')
    # csvwriter.writerow(campos)

    #rows = set()
    data = []

    s = requests.Session()
    print('getting sitemap...')
    sitemap = s.get(SITEMAP)

    xmlstr = minidom.parseString(sitemap.content).toprettyxml(indent="   ")
    with open("sitemap.xml", "w") as f:
        print('saving sitemap...')
        f.write(xmlstr)

    print('getting ids of categories...')
    categoriasTemp = findall(
        r'<loc>https://mercadao\.pt/store/pingo-doce/category/((\w|-)+)</loc>', xmlstr)
    categorias = []
    for elem in categoriasTemp:
        s = requests.Session()
        categorias.append((elem[0], s.get(APIIDS+elem[0]).json()['id']))

    #produtos = {}
    print('Starting getting products...')
    for categoria, categoriaId in categorias:
        link = sub(r'@catID@', categoriaId, APIPRODUTOS)
        thislink = sub(r'@startPoint@', '0', link)
        s = requests.Session()
        try:
            page = s.get(thislink).json()['sections']['null']
        except:
            print(thislink)
            # exit(-1)
            continue
        total = page['total']
        print(categoria + f' ({total})')
        i = 0
        while i < total:
            for product in page['products']:
                product = product['_source']
                for ean in product['eans']:
                    # if product['slug'] in produtos.keys():
                    #     continue
                    if name := product['firstName']:
                        name = unidecode(
                            product['firstName'].lower().replace('-', ' '))
                    if brand := product['brand']['name']:
                        brand = unidecode(
                            product['brand']['name'].lower().replace('-', ' '))
                    price = round(float(product['regularPrice']), 2)
                    if price != product['buyingPrice']:
                        promo = round(float(product['buyingPrice']), 2)
                    else:
                        promo = None
                    quantity = product['capacity']
                    quantity = sub('L', 'lt', quantity)
                    quantity = sub('metros', 'mt', quantity)
                    quantity = unidecode(quantity.lower())

                    ppu = regra3simples(
                        product['buyingPrice'], product['netContent'])

                    #rows.add((name, brand, quantity, price, ppu, promo, ean))
                    objProduto = {"Nome": name, "Marca": brand, "Quantidade": quantity,
                                  unidecode("Preço Primário"): price, unidecode("Preço Por Unidade"): ppu, "Promo": promo, "EAN": ean}
                    if objProduto in data:
                        continue
                    data.append(objProduto)
                # produtos[product['slug']] = objProduct
            i += 100
            thislink = sub(r'@startPoint@', str(i), link)
            try:
                page = s.get(thislink).json()['sections']['null']
            except:
                print(f'ERROR::: got {len(data)} products')
                time.sleep(60)

    # csvwriter.writerows(rows)

    requests.post("http://localhost:8080/api/v1/pingodoce/products", json=data)

    # if not os.path.exists("csvProdutos"):
    #    os.makedirs("csvProdutos")
    # json_file = open(FILENAME,
    #                 'w')
    #json.dump(data, json_file)
    # print(f'getted {len(produtos)} products')

    # with open('pingo-doce-products.json', 'w') as f:
    #     print('saving...')
    #     for id in produtos.keys():
    #         f.write(f'{str(produtos[id])}\n')


def main():
    getProdutosPagina()
    return FILENAME


if __name__ == "__main__":
    main()
