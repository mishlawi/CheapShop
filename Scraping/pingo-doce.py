import requests
from xml.dom import minidom
from re import *
import time

SITEMAP = 'https://mercadao.pt/api/sitemap.xml'
APIIDS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/categories/slug/'
APIPRODUTOS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=["@catID@"]&from=@startPoint@&size=100&esPreference=0.6439211110152693'

print('getting sitemap...')
sitemap = requests.get(SITEMAP)

xmlstr = minidom.parseString(sitemap.content).toprettyxml(indent="   ")
with open("sitemap.xml", "w") as f:
    print('saving sitemap...')
    f.write(xmlstr)


print('getting ids of categories...')
categoriasTemp = findall(r'<loc>https://mercadao\.pt/store/pingo-doce/category/((\w|-)+)</loc>', xmlstr)
categorias = []
for elem in categoriasTemp:
    categorias.append((elem[0], requests.get(APIIDS+elem[0]).json()['id']))


produtos = {}
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
            if product['slug'] in produtos.keys():
                continue
            objProduct = {
                'Designação' : product['firstName'],
                'Marca' : product['brand']['name'],
                'Preco' : product['regularPrice'],
                'Preco_Promo' : product['campaignPrice'],
                'Quantidade' : product['capacity']
            }
            produtos[product['slug']] = objProduct
        i+=100
        thislink = sub(r'@startPoint@', str(i), link)
        try:
            page = s.get(thislink).json()['sections']['null']
        except:
            print(f'ERROR::: got {len(produtos)} products')
            time.sleep(60)

print(f'getted {len(produtos)} products')

with open('pingo-doce-products.json', 'w') as f:
    print('saving...')
    for id in produtos.keys():
        f.write(f'{str(produtos[id])}\n')