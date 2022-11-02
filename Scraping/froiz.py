from bs4 import BeautifulSoup as BS
import requests
import csv
import re

rows = []

def getProdutosPagina(link):
    total = 0
        
    # CSV BUILD
    campos = ['Nome', 'Marca', 'Unidade', 'Preço', 'Preço anterior', 'Preço por unidade']
    file = 'ProdutosFroiz.csv'
    csvo = open(file,'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    html = requests.get(link).text
    soup = BS(html,"html.parser")

    categoriesmenu = soup.find('li', class_='dropdown dropdown-megamenu').find('ul')
    categoriescolumns = categoriesmenu.find_all('div',class_='span3')
    categoriesids = []

    for column in categoriescolumns:
        if listpercolumn := column.find('ul'):
            categories = listpercolumn.find_all('li')
            for category in categories:
                categoryid = category.find('a')['href']
                categoriesids.append(categoryid)
    
    print(categoriesids)

    subcategorylinks = {}
    for categoryid in categoriesids:
        htmlcategory = requests.get(link+categoryid).text
        soupcategory = BS(htmlcategory,"html.parser")
        
        subcategorieselems = soupcategory.find('div',class_='row popup-products').find_all('div',class_='span3')
        for subcategoryelem in subcategorieselems:
            subcategories = subcategoryelem.find_all('li')
            for subcategory in subcategories:
                subcategoryid = subcategory.find('a')['href']
                subcategoryname = subcategory.find('a').text.strip()
                subcategorylinks[link + subcategoryid] = subcategoryname

    #print(len(subcategorylinks))
    for subcategorylink in subcategorylinks:
        print(subcategorylinks[subcategorylink])
        htmlsubcategory = requests.get(subcategorylink).text
        soupsubcategory = BS(htmlsubcategory,"html.parser")

        subcategorytotal = re.search('\(([^)]+)', soupsubcategory.find('section',class_='span10').find('div',class_='span5').find('span',class_='light').text.strip().split(' ')[-1]).group(1)
        total = total + int(subcategorytotal)

        productelems = soupsubcategory.find_all('div',class_='row-fluid popup-products')
        for productelem in productelems:
            productname = productelem.find('p',class_='push-down-10 isotope--title dproducto').text.strip()
            productpricestrike = ''
            if productelem.find('h4',class_='title').find_all('span'):
                productprice = productelem.find('h4',class_='title').find('span',class_='red-clr').text.strip()
                productpricestrike = productelem.find('h4',class_='title').find('span',class_='striked').text.strip()
            else:
                productprice = productelem.find('h4',class_='title').text.strip()
            productpriceperunit = productelem.find('div',class_='row-fluid hidden-line').find('div',class_='span8').text.strip()

            rows.append([productname,'','',productprice,productpricestrike,productpriceperunit])

    csvwriter.writerows(rows)
    print(total)






getProdutosPagina('https://www.froiz.com/shop/')
