import requests
from xml.dom import minidom
from re import *
import time
import csv

SITEMAP = 'https://mercadao.pt/api/sitemap.xml'
APIIDS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/categories/slug/'
APIPRODUTOS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=["@catID@"]&from=@startPoint@&size=100&esPreference=0.6439211110152693'


def getProdutosPagina():
    # CSV BUILD
    campos = ['Nome', 'Marca', 'Quantidade',
              'Preço Primário', 'Preço Por Unidade', 'Promo']
    file = f"csvProdutos/ProdutosPingoDoce.csv"
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    rows = set()

    print('getting sitemap...')
    sitemap = requests.get(SITEMAP)

    xmlstr = minidom.parseString(sitemap.content).toprettyxml(indent="   ")
    with open("sitemap.xml", "w") as f:
        print('saving sitemap...')
        f.write(xmlstr)

    print('getting ids of categories...')
    categoriasTemp = findall(
        r'<loc>https://mercadao\.pt/store/pingo-doce/category/((\w|-)+)</loc>', xmlstr)
    categorias = []
    for elem in categoriasTemp:
        categorias.append((elem[0], requests.get(APIIDS+elem[0]).json()['id']))

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
            exit(-1)
        total = page['total']
        print(categoria + f' ({total})')
        i = 0
        while i < total:
            for product in page['products']:
                product = product['_source']
                # if product['slug'] in produtos.keys():
                #     continue
                name = product['firstName']
                brand = product['brand']['name']
                price = product['regularPrice']
                promo = product['campaignPrice']
                quantity = product['capacity']
                ppu = None

                rows.add((name, brand, quantity, price, ppu, promo))
                # produtos[product['slug']] = objProduct
            i += 100
            thislink = sub(r'@startPoint@', str(i), link)
            try:
                page = s.get(thislink).json()['sections']['null']
            except:
                #print(f'ERROR::: got {len(produtos)} products')
                time.sleep(60)

    csvwriter.writerows(rows)
    # print(f'getted {len(produtos)} products')

    # with open('pingo-doce-products.json', 'w') as f:
    #     print('saving...')
    #     for id in produtos.keys():
    #         f.write(f'{str(produtos[id])}\n')


getProdutosPagina()
