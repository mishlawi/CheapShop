'''
This scraper is optimized with threads
Each category is processed by one thread and each thread processes only one category,
making the processing of category products parallel, and, consequently, faster
'''

from bs4 import BeautifulSoup as BS
from threading import Thread
import requests
import json
import csv
import re


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
    file = 'csvProdutos/ProdutosElCorteIngles.csv'
    csvo = open(file, 'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
               "Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(link, headers=headers).text
    soup = BS(html, "html.parser")

    navbar = soup.find('nav', class_='top_menu')
    categorieselem = navbar.find_all(lambda tag: tag.name == 'a' and tag.get(
        'class') == ['top_menu-item'], recursive=False)

    categorieslinks = []
    for elem in categorieselem:
        categorieslinks.append(link + elem['href'].split('/')[-2])

    # print(categorieslinks)

    scrappingWorkers = []
    for categorylink in categorieslinks:
        scrappingWorker = ThreadWithReturnValue(target=processCategory, args=(
            categorylink,), name=categorylink.split('/')[-1])
        scrappingWorkers.append(scrappingWorker)
        scrappingWorker.start()

    for scrappingWorker in scrappingWorkers:
        for row in scrappingWorker.join():
            rows.add(row)

    csvwriter.writerows(rows)


def processCategory(categoryLink):
    local_rows = set()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
               "Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(categoryLink, headers=headers).text
    soup = BS(html, "html.parser")

    totalcategoryproducts = int(soup.find(
        'div', class_='c12 c4-xl-up tc').find('h2').text.strip().split(' ')[0].replace('.', ''))
    print('# total products', totalcategoryproducts,
          categoryLink.split('/')[-1])

    paginationdiv = soup.find('div', class_='pagination c12 js-pagination')

    while not paginationdiv:
        html = requests.get(categoryLink, headers=headers).text
        soup = BS(html, "html.parser")
        paginationdiv = soup.find('div', class_='pagination c12 js-pagination')

    paginationcontrols = paginationdiv.find(
        'div', class_='pagination-controls c12')
    totalpages = paginationcontrols.find(
        'li', id='pagination-current').text.strip().split(' ')[-1]
    # print('# pages',int(totalpages))

    for _ in range(int(totalpages)):
        paginationdiv = soup.find('div', class_='pagination c12 js-pagination')
        paginationcontrols = paginationdiv.find(
            'div', class_='pagination-controls c12')
        newpage = paginationcontrols.find('li', id='pagination-next').find('a')

        productsgrid = soup.find('div', class_='c12 js-grid-container')
        # 'grid-item product_tile _retro _supermarket _nostock dataholder js-product' --apanhar produtos sem stock?
        productselems = productsgrid.find_all('div', class_=re.compile(
            'grid-item product_tile _retro _supermarket'))

        # print('# of product elements got from page',len(productselems))
        for productelem in productselems:
            name = productelem['data-product-description']
            pricediv = productelem.find(
                'div', class_='product_tile-price_holder')
            promo = None
            price = None
            if json.loads(productelem["data-json"])['discount'] == True:
                promo = json.loads(productelem["data-json"])['price']['final']
                price = json.loads(
                    productelem["data-json"])['price']['original']
            else:
                price = json.loads(productelem["data-json"])['price']['final']
            # if pricediv.find('div','prices-price _before'):
            #     promo = pricediv.find('div','prices-price _before').text.strip()
            # else:
            #     promo = None
            # if pricediv.find('div',class_=re.compile('prices-price [_offer|_offer _no_pum|_current|current_no_pum]')):
            #     price = pricediv.find('div',class_=re.compile('prices-price [_offer|_offer _no_pum|_current|current_no_pum]')).text.strip()
            # else:
            #     price = None
            if pricediv.find('div', class_='prices-price _pum'):
                ppu = pricediv.find(
                    'div', class_='prices-price _pum').text.strip()
            else:
                ppu = None
            if 'brand' in json.loads(productelem["data-json"]):
                brand = json.loads(productelem["data-json"])['brand']
            else:
                brand = None
            quantity = None
            if quantity := re.search(r'(\(\d+[^()]+?\)|\d+((x|,|\.)\d+)?([^0-9()a-zA-Z]+)?(\w{,3}|unidades))$', name):
                quantity = quantity.group(0)
                name = name.replace(quantity, '').strip()
                name = name.replace('embalagem', '').strip()
            local_rows.add((name, brand, quantity, price, ppu, promo))

        if newpage:
            nextpagelink = categoryLink + '/' + newpage['href'].split('/')[-2]
            # print('next',nextpagelink)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Accept-Language": "en-US,en;q=0.5"}
            html = requests.get(nextpagelink, headers=headers).text
            soup = BS(html, "html.parser")
            paginationdiv = soup.find(
                'div', class_='pagination c12 js-pagination')

            while not paginationdiv:
                html = requests.get(categoryLink, headers=headers).text
                soup = BS(html, "html.parser")
                paginationdiv = soup.find(
                    'div', class_='pagination c12 js-pagination')

            paginationcontrols = paginationdiv.find(
                'div', class_='pagination-controls c12')

        else:
            break

    print('category: ', categoryLink.split('/')[-1])
    return local_rows


getProdutosPagina('https://www.elcorteingles.pt/supermercado/')
