'''
This scraper is optimized with threads
Each store is processed by one thread and each thread processes only one store,
making the processing of each store parallel, and, consequently, faster
'''


from bs4 import BeautifulSoup as BS
from threading import Thread
import threading
import unidecode
import requests
import csv
import re
import time
import json


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


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def getProdutosPagina(link):
    s = requests.Session()

    html = s.get(link,headers=headers).text
    soup = BS(html, "html.parser")
    lojaselems = soup.find_all('div', class_='menu_ativo')
    linkslojas = [link]
    for lojaelem in lojaselems:
        linkslojas.append(lojaelem['onclick'].split(
            '(')[1].split(',')[0].replace('\'', '') + '/')

    # print(linkslojas)

    for lojalink in linkslojas:
        thread = Thread(target=processStore, args=(
            lojalink,), name=lojalink.split('/')[-2])
        thread.start()


def processStore(lojalink):
    print(threading.current_thread().name, 'started')
    storeregex = r'.*(?<=hipermercado-)(.*)\/|.*(?<=e\.leclerc-)(.*)\/'
    localstore = re.match(storeregex, lojalink)[1]
    if not localstore:
        localstore = re.match(storeregex, lojalink)[2]

    #print('loja: ',localstore)

    # CSV BUILD
    #rows = set()
    # campos = ['Nome', 'Marca', 'Quantidade',
    #           'Preço Primário', 'Preço Por Unidade', 'Promo']
    # file = f"csvProdutos/ProdutosEleclerc/ProdutosEleclerc_{localstore}.csv"
    # csvo = open(file, 'w')
    # csvwriter = csv.writer(csvo)
    # csvwriter.writerow(campos)

    data = []
    
    s = requests.Session()
    html = s.get(lojalink).text
    soup = BS(html, "html.parser")

    html = s.get(lojalink,headers=headers).text
    soup = BS(html, "html.parser")
    print(html)
    categoriesdiv = soup.find('div', class_='categorias').find(
        'div', class_='opcoes')
    categoriesnames = categoriesdiv.find_all('a', recursive=False)

    categorieslinks = []
    for categoryname in categoriesnames:
        categoryid = unidecode.unidecode(
            categoryname.text.strip().lower().replace(' ', '-'))
        categorieslinks.append(lojalink + categoryid + '/')

    # print(categorieslinks)

    for categorylink in categorieslinks:
        # for row in processCategory(categorylink):
        #     rows.add(row)
        data += processCategory(categorylink)

    #csvwriter.writerows(rows)
    json_file = open(f"csvProdutos/ProdutosEleclerc/ProdutosEleclerc_{localstore}.json",'w',encoding='utf-8')
    json.dump(data,json_file,ensure_ascii=False)


def processCategory(categorylink):
    print(threading.current_thread().name, 'started')
    local_rows = set()
    local_data = []
    categorytotal = 0

    s = requests.Session()
    html = s.get(categorylink,headers=headers).text
    soup = BS(html, "html.parser")

    productselems = soup.find_all('div', class_='produtos_coluna')
    while not productselems:
        print(productselems, ' productselems')
        
        s = requests.Session()
        html = s.get(categorylink,headers=headers).text
        soup = BS(html, "html.parser")
        productselems = soup.find_all('div', class_='produtos_coluna')

    print('    products on', threading.current_thread().name,
          'page:', len(productselems))
    for productelem in productselems:
        name = productelem.find('div', class_='produtos_nome').text.strip()
        brand = productelem.find('div', class_='produtos_marca_texto')
        if brand:
            brand = brand.text.strip()
        else:
            brand = None
        emb = productelem.find('div', class_='produtos_emb')
        if emb:
            emb = emb.text.strip()
        else:
            emb = None
        price = productelem.find('div', class_='div_preco')
        if price:
            price = price.text.strip()
            price = float(price.replace(',', '.')[:price.find('€')])
        else:
            price = None

        ppu = productelem.find('div', class_='div_preco_peq')
        if ppu:
            ppu = ppu.text.strip()
        else:
            ppu = None

        categorytotal += 1
        local_rows.add((name, brand, emb, price, ppu, None))
        objProduto = {"Nome":name, "Marca":brand, "Quantidade":emb, "Preço Primário":price,
                    "Preço Por Unidade":ppu, "Promo":None}
        if objProduto in local_data:
            continue
        
        local_data.append(objProduto)

    print('    products added for', categorylink.split(
        '/')[-2], ':', categorytotal)
    #return local_rows
    return local_data


getProdutosPagina('https://online.e-leclerc.pt/hipermercado-braga/')
