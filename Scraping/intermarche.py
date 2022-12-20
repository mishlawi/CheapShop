from bs4 import BeautifulSoup as BS
from threading import Thread
import requests
import csv
from re import *


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def getProdutosPagina(link):
    html = requests.get(link).text
    soup = BS(html, "html.parser")

    districts = soup.find_all(lambda tag: tag.name ==
                              'div' and tag.get('class') == ['district'])
    stores = []
    for district in districts:
        storesdistrict = district.find_all(
            lambda tag: tag.name == 'a' and tag.get('data-es') == 'True')
        for storedistrict in storesdistrict:
            stores.append(storedistrict['href'])

    storelinks = []
    for store in stores:
        html = requests.get(store).text
        soup = BS(html, "html.parser")

        onlinelink = soup.find(lambda tag: tag.name == 'a' and tag.get(
            'data-ga-category') == "Ver Loja Online")
        if onlinelink:
            storelinks.append(onlinelink['href'])

    # print(storelinks)

    for storelink in storelinks:
        processStore((storelink))


def processStore(storelink):
    print(storelink)

    # CSV BUILD
    campos = ['Nome', 'Marca', 'Quantidade',
              'Preço Primário', 'Preço Por Unidade', 'Promo']
    file = f"csvProdutos/ProdutosIntermarche/ProdutosIntermarche_{storelink.split('/')[-1]}.csv"
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    rows = set()

    s = requests.Session()
    html = s.get(storelink).text
    soup = BS(html, "html.parser")

    categorieselems = soup.find_all(
        lambda tag: tag.name == 'li' and tag.get('class') == ['separateur'])
    categorylinks = []
    for categoryelem in categorieselems:
        linkstemp = categoryelem.find(
            'nav', class_='nav_sous-menu').find_all('a')
        for linktemp in linkstemp:
            categorylinks.append(linktemp['href'])

    for categorylink in categorylinks:
        # print(categorylink)

        baselink = 'https://lojaonline.intermarche.pt'

        s = requests.Session()
        html = s.get(baselink+categorylink).text
        soup = BS(html, "html.parser")

        productsgrid = soup.find(lambda tag: tag.name == 'div' and tag.get(
            'class') == ['content_vignettes', 'js-vignette_rayon'])
        if productsgrid:
            productslist = productsgrid.find(lambda tag: tag.name == 'ul' and tag.get('class') == ['vignettes_produit', 'js-source', 'js-vignettes_produit_slide']).find_all(
                lambda tag: tag.name == 'li' and tag.get('class') == ['vignette_produit_info', 'js-vignette_produit'])
            for product in productslist:
                infodiv = product.find('div', class_='vignette_info')
                pricediv = productsgrid.find(
                    'div', class_='vignette_picto_prix')
                brand = infodiv.find('p', class_='js-marque')
                if brand:
                    brand = brand.text.strip()
                else:
                    brand = None
                name = infodiv.find(lambda tag: tag.name == 'p' and tag.get(
                    'class') == None).text.strip()
                quantity = infodiv.find('span').text.strip()
                quantity = sub(r'Vendido.+', '', quantity)
                quantity = sub(r'Venda ao Kilo', '', quantity)
                quantity = sub(r'(\d+)Unidades', '\1 un', quantity)
                quantity = sub(r'^unidade$', '1 un', quantity)
                quantity = sub(r'(u|U)nidade(s?)', 'un', quantity)
                quantity = sub(r'Uma embalagem de ', '', quantity)
                quantity = sub(r'Uma embalagem com', '', quantity)
                quantity = sub(r'Uma embalagem - ', '', quantity)
                quantity = sub(r'embalagem', '', quantity)
                quantity = sub(r'Saqueta de ', '', quantity)
                quantity = sub(r'Pescado no mar', '', quantity)
                quantity = sub(r'pasta.+', '', quantity)
                quantity = sub(r'Pack Poupança de ', '', quantity)
                quantity = sub(r'pack familiar de ', '', quantity)
                quantity = sub(r'pack de ', '', quantity)
                quantity = sub(r'(L|l)ata de ', '', quantity)
                quantity = sub(r'(P|p)ack:? ', '', quantity)
                quantity = sub(r'(G|g)arrafão de ', '', quantity)
                quantity = sub(r'(G|g)arrafa de vidro ', '', quantity)
                quantity = sub(r'(G|g)arrafa de ', '', quantity)
                quantity = sub(r'(litro(s?))|L', 'l', quantity)
                quantity = sub(r' c/ Caixa de Madeira', '', quantity)
                quantity = sub(r'(\d+)L', '\1 l', quantity)
                quantity = sub(r'(\d+)(\w)', '\1 \2', quantity)
                quantity = sub(r'(F|f)rasco de ', '', quantity)
                quantity = sub(r'(F|f)rasco com ', '', quantity)
                quantity = sub(r'Embalagem:? ', '', quantity)
                quantity = sub(r'Embalagem sortida com ', '', quantity)
                quantity = sub(r'Embalagem ML', '', quantity)
                quantity = sub(r'Embalagem de', '', quantity)
                quantity = sub(r'\+ Oferta de 1 Copo', '', quantity)
                quantity = sub(r'\+-', '', quantity)
                quantity = sub(r'(E|e)mbalagem com rosca de ', '', quantity)
                quantity = sub(r'(E|e)mbalagem com ', '', quantity)
                quantity = sub(r'(E|e)mbalagem c/ ', '', quantity)
                quantity = sub(r'\.$', '', quantity)
                quantity = sub(r'cubos', 'un', quantity)
                quantity = sub(r'^T.+', '', quantity)
                quantity = sub(r'^Dim.+', '', quantity)
                quantity = sub(r'Conjunto.+', '', quantity)
                quantity = sub(r'^Congelada.+', '', quantity)
                quantity = sub(r'^(C|c).+', '', quantity)
                quantity = sub(r'Boião de ', '', quantity)
                quantity = sub(r'Bag-in-box de ', '', quantity)
                quantity = sub(r', 1 embalagem', '', quantity)
                quantity = sub(r',', '.', quantity)
                quantity = sub(r'Uma', '1', quantity)
                quantity = sub(r' embaladas individualmente', '', quantity)



                if pricediv.find('p', class_='red-text surligner'):
                    promo = price = pricediv.find(
                        'p', class_='red-text surligner').text.strip()
                    promo = float(promo.replace(',', '.')[:-1])
                else:
                    promo = None
                    price = pricediv.find('p', class_='').text.strip()
                    price = float(price.replace(',', '.')[:-1])
                ppu = pricediv.find('p', class_=None).text.strip()

                rows.add((name, brand, quantity, price, ppu, promo))
        else:
            s.close()
            break
        s.close()

    csvwriter.writerows(rows)


getProdutosPagina('https://www.intermarche.pt/lojas/?q=online')
