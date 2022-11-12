from bs4 import BeautifulSoup as BS
from threading import Thread
import requests
import csv


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
    campos = ['Nome', 'Marca', 'Unidade', 'Preço Primário', 'Preço Secundário']
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
                price = pricediv.find('p', class_='').text.strip()
                ppu = pricediv.find('p', class_=None).text.strip()

                rows.add((name, brand, quantity, price, ppu))
        else:
            s.close()
            break
        s.close()

    csvwriter.writerows(rows)


getProdutosPagina('https://www.intermarche.pt/lojas/?q=online')
