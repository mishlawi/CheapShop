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
    rows = set()

    # CSV BUILD
    campos = ['Nome', 'Marca', 'Quantidade',
              'Preço Primário', 'Preço Por Unidade', 'Promo']
    file = 'csvProdutos/ProdutosContinente.csv'
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    html = requests.get(link).text
    soup = BS(html, "html.parser")

    categorycolumn = soup.find(["ul"], class_="dropdown-menu item-shadow").find([
        'div'], class_="container-dropdown-first-column")
    categorieslist = categorycolumn.find_all(
        ['li'], class_="dropdown-item dropdown", recursive=False)
    labelelem = {}
    categorylinks = {}
    for elem in categorieslist:
        categorylink = elem.find(['a'])["href"]
        label = elem.find(['ul'])["aria-label"]
        if not "-marcas" in label:
            categorylinks[categorylink] = label
            labelelem[label] = elem

    i = 0
    keys = list(categorylinks.keys())
    while i < len(keys):
        categorylink = keys[i]
        i = i+1
        print(categorylinks[categorylink])
        html = requests.get(categorylink).text
        soup = BS(html, "html.parser")
        totalproducts = 0
        if soup.find(['div'], class_="row product-grid no-gutters gtm-list"):
            totalproducts = soup.find(
                ['span'], class_="product-count pull-right").text.strip().split(' ')[0]
        else:
            currentelem = labelelem[categorylinks[categorylink]]
            linkTag2 = currentelem.find(
                ['ul'], class_="dropdown-menu item-shadow")
            subcategorieslist = linkTag2.find_all(
                ['li'], class_="dropdown-item dropdown", recursive=False)
            if not subcategorieslist:
                subcategorieslist = linkTag2.find_all(lambda tag: tag.name == 'li' and
                                                      tag.get('class') == ['dropdown-item'], recursive=False)
                for subcategoryelem in subcategorieslist:
                    subcategorylink2 = subcategoryelem.find(['a'])["href"]
                    # print(subcategorylink2)
                    categorylinks[subcategorylink2] = categorylinks[categorylink] + \
                        '-' + subcategorylink2.split('/')[-2].split('-')[0]
                    #print('added', list(categorylinks.keys())[-1])
            else:
                for subcategoryelem in subcategorieslist:
                    subcategorylink2 = subcategoryelem.find(['a'])["href"]
                    label2 = subcategoryelem.find(['ul'])["aria-label"]
                    # print(subcategorylink2)
                    if not "-marcas" in label2:
                        categorylinks[subcategorylink2] = label2
                        #print('added', list(categorylinks.keys())[-1])
                        labelelem[label2] = subcategoryelem
            keys = list(categorylinks.keys())
            continue

        # print(totalproducts)

        for j in range(0, int(totalproducts), 2000):
            if (int(totalproducts) <= 36):
                searchlink = categorylink
            else:
                searchlink = f"https://www.continente.pt/on/demandware.store/Sites-continente-Site/default/Search-UpdateGrid?cgid={categorylinks[categorylink]}&pmin=0.01&start={j}&sz=2000"

            html = requests.get(searchlink).text
            soup = BS(html, "html.parser")

            products = soup.find_all(
                ['div'], class_="col-12 col-sm-3 col-lg-2 productTile")

            #print('total', len(products))
            for product in products:

                try:
                    name = product.find(
                        ['a'], class_="ct-tile--description").text.strip()
                except:
                    continue
                productbrand = product.find(['p'], class_="ct-tile--brand").text.strip(
                ) if product.find(['p'], class_="ct-tile--brand") else None
                productquantity = product.find(
                    ['p'], class_="ct-tile--quantity").text.strip() if product.find(['p'], class_="ct-tile--quantity") else None

                productquantity = sub(r'^emb\. ?', '', productquantity)
                productquantity = sub(r',', '.', productquantity)
                productquantity = sub(r'\(.+?\)', '', productquantity)
                productquantity = sub(r'(g|G)arrafa ', '', productquantity)
                productquantity = sub(r'lata ', '', productquantity)
                productquantity = sub(r'gr', 'g', productquantity)
                productquantity = sub(r'\d+ rolos = ', '', productquantity)
                productquantity = sub(r'NULL ', '', productquantity)
                productquantity = sub(r'Várias quantidades', '', productquantity)
                productquantity = sub(r'Bag im Box ', '', productquantity)
                productquantity = sub(r'barril ', '', productquantity)

                if match(r'Quant\. Mínima ?=', productquantity):
                    productquantity = None  


                pp = product.find(
                    ['span'], class_="sales ct-tile--price-primary")
                sp = product.find(['div'], class_="ct-tile--price-secondary")

                promo = None
                price = None
                if product.find('span', class_='value ct-tile--price-value'):
                    price = product.find(
                        'span', class_='value ct-tile--price-value')['content']
                    promo = pp.find(['span'], class_="value")['content']
                else:
                    price = pp.find(['span'], class_="value")['content']

                if sp:
                    spu = sp.find(['span'], class_="ct-price-value").text.strip() + \
                        sp.find(['span'], class_="ct-m-unit").text.strip()
                    spu = sub(r',', '.', spu)
                else:
                    spu = None

                rows.add((name, productbrand, productquantity, price, spu, promo))

    csvwriter.writerows(rows)


getProdutosPagina('https://www.continente.pt')
