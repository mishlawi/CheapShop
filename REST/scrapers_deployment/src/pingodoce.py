import requests
from xml.dom import minidom
from re import *
from unidecode import unidecode

SITEMAP = 'https://mercadao.pt/api/sitemap.xml'
APIIDS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/categories/slug/'
APIPRODUTOS = 'https://mercadao.pt/api/catalogues/6107d28d72939a003ff6bf51/products/search?mainCategoriesIds=["@catID@"]&from=@startPoint@&size=100&esPreference=0.6439211110152693'
IMAGELINK = 'https://res.cloudinary.com/fonte-online/image/upload/v1/PDO_PROD/'
PRODUCTLINK = 'https://mercadao.pt/store/pingo-doce/product/'


def regra3simples(preco, quantidade, pretendido=1):
    return round(pretendido*float(preco)/float(quantidade), 2)


def getProdutosPagina():

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

                    imagelink = IMAGELINK + \
                        product['sku']+'_'+str(product['imagesNumber'])

                    productlink = PRODUCTLINK + product['slug']

                    objProduto = {"Nome": name, "Marca": brand, "Quantidade": quantity,
                                  unidecode("Preço Primário"): price, unidecode("Preço Por Unidade"): ppu, "Promo": promo, "EAN": ean, "Link Imagem": imagelink, "Link Produto": productlink}
                    if objProduto in data:
                        continue
                    data.append(objProduto)
            i += 100
            thislink = sub(r'@startPoint@', str(i), link)
            try:
                page = s.get(thislink).json()['sections']['null']
            except:
                print(f'ERROR::: got {len(data)} products')

    # data = [
    #     {
    #         "Nome": "fosforos home 7   pack 4",
    #         "Marca": "home 7",
    #         "Quantidade": "4x100 un",
    #         "Preco Primario": 0.69,
    #         "Preco Por Unidade": 0.17,
    #         "Promo": None,
    #         "EAN": "2000003210862",
    #         "Link Imagem": "https://res.cloudinary.com/fonte-online/image/upload/v1/PDO_PROD/862257_1",
    #         "Link Produto": "https://mercadao.pt/store/pingo-doce/product/fosforos-home-7-pack-4-4x100-un"
    #     },
    #     {
    #         "Nome": "fosforos home 7   pack 4",
    #         "Marca": "home 7",
    #         "Quantidade": "4x100 un",
    #         "Preco Primario": 0.69,
    #         "Preco Por Unidade": 0.17,
    #         "Promo": None,
    #         "EAN": "5601009967759",
    #         "Link Imagem": "https://res.cloudinary.com/fonte-online/image/upload/v1/PDO_PROD/862257_1",
    #         "Link Produto": "https://mercadao.pt/store/pingo-doce/product/fosforos-home-7-pack-4-4x100-un"
    #     },
    #     {
    #         "Nome": "castanha pingo doce congelada",
    #         "Marca": "pingo doce",
    #         "Quantidade": "1 kg",
    #         "Preco Primario": 9.99,
    #         "Preco Por Unidade": 9.99,
    #         "Promo": None,
    #         "EAN": "5601009920594",
    #         "Link Imagem": "https://res.cloudinary.com/fonte-online/image/upload/v1/PDO_PROD/614838_1",
    #         "Link Produto": "https://mercadao.pt/store/pingo-doce/product/castanha-pingo-doce-congelada-1-kg"
    #     }
    # ]
    # f = open('pingo.json','w')
    # f.write(json.dumps(data))

    print('pingo doing request...')
    response = requests.post(
        "http://api:8080/api/v1/pingodoce/products", json=data, timeout=30)
    print('response status to pingo:')
    print(response.status_code)


def main():
    getProdutosPagina()


if __name__ == "__main__":
    main()
