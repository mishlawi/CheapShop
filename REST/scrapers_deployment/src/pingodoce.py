import requests
from xml.dom import minidom
from re import *
from unidecode import unidecode

SITEMAP = 'https://mercadao.pt/api/sitemap.xml'
APIIDS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/categories/slug/'
APIPRODUTOS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=["@catID@"]&from=@startPoint@&size=100&esPreference=0.6439211110152693'


def regra3simples(preco, quantidade, pretendido=1):
    return round(pretendido*float(preco)/float(quantidade), 2)


def getProdutosPagina():

    # data = []

    # s = requests.Session()
    # print('getting sitemap...')
    # sitemap = s.get(SITEMAP)

    # xmlstr = minidom.parseString(sitemap.content).toprettyxml(indent="   ")
    # with open("sitemap.xml", "w") as f:
    #     print('saving sitemap...')
    #     f.write(xmlstr)

    # print('getting ids of categories...')
    # categoriasTemp = findall(
    #     r'<loc>https://mercadao\.pt/store/pingo-doce/category/((\w|-)+)</loc>', xmlstr)
    # categorias = []
    # for elem in categoriasTemp:
    #     s = requests.Session()
    #     categorias.append((elem[0], s.get(APIIDS+elem[0]).json()['id']))

    # print('Starting getting products...')
    # for categoria, categoriaId in categorias:
    #     link = sub(r'@catID@', categoriaId, APIPRODUTOS)
    #     thislink = sub(r'@startPoint@', '0', link)
    #     s = requests.Session()
    #     try:
    #         page = s.get(thislink).json()['sections']['null']
    #     except:
    #         print(thislink)
    #         # exit(-1)
    #         continue
    #     total = page['total']
    #     print(categoria + f' ({total})')
    #     i = 0
    #     while i < total:
    #         for product in page['products']:
    #             product = product['_source']
    #             for ean in product['eans']:
    #                 if name := product['firstName']:
    #                     name = unidecode(
    #                         product['firstName'].lower().replace('-', ' '))
    #                 if brand := product['brand']['name']:
    #                     brand = unidecode(
    #                         product['brand']['name'].lower().replace('-', ' '))
    #                 price = round(float(product['regularPrice']), 2)
    #                 if price != product['buyingPrice']:
    #                     promo = round(float(product['buyingPrice']), 2)
    #                 else:
    #                     promo = None
    #                 quantity = product['capacity']
    #                 quantity = sub('L', 'lt', quantity)
    #                 quantity = sub('metros', 'mt', quantity)
    #                 quantity = unidecode(quantity.lower())

    #                 ppu = regra3simples(
    #                     product['buyingPrice'], product['netContent'])

    #                 objProduto = {"Nome": name, "Marca": brand, "Quantidade": quantity,
    #                               unidecode("Preço Primário"): price, unidecode("Preço Por Unidade"): ppu, "Promo": promo, "EAN": ean}
    #                 if objProduto in data:
    #                     continue
    #                 data.append(objProduto)
    #         i += 100
    #         thislink = sub(r'@startPoint@', str(i), link)
    #         try:
    #             page = s.get(thislink).json()['sections']['null']
    #         except:
    #             print(f'ERROR::: got {len(data)} products')

    data = [
        {
            "Nome": "chocolate storck toffifee 125g",
            "Marca": "storck",
            "Quantidade": "0.125 KG",
            "Preco Primario": "3.85",
            "Preco Por Unidade": "24 €/Kg",
            "Promo": "3.00",
            "EAN": "4014400400007"
        },
        {
            "Nome": "filetes pescanova pescada do cabo 400g",
            "Marca": "pescanova",
            "Quantidade": "0.4 KG",
            "Preco Primario": "4.99",
            "Preco Por Unidade": "12.48 €/Kg",
            "Promo": None,
            "EAN": "8410063034515"
        },
        {
            "Nome": "vinho branco faisao 1l",
            "Marca": "faisao",
            "Quantidade": None,
            "Preco Primario": "2.19",
            "Preco Por Unidade": "2.19 €/Lt",
            "Promo": None,
            "EAN": "5601239329747"
        },
        {
            "Nome": "posta pescanova pescada no5 para cozer 800g",
            "Marca": "hey im working",
            "Quantidade": "0.8 KG",
            "Preco Primario": "13.99",
            "Preco Por Unidade": "17.49 €/Kg",
            "Promo": None,
            "EAN": "8410063005232"
        }
    ]

    print('pingo doing request...')
    response = requests.post(
        "http://api:8080/api/v1/pingodoce/products", json=data, timeout=30)
    print('response status to pingo:')
    print(response.status_code)


def main():
    getProdutosPagina()


if __name__ == "__main__":
    main()
