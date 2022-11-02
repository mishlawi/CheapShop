from bs4 import BeautifulSoup as BS
import requests
import csv

rows = []

def getProdutosPagina(link):
    
    # CSV BUILD
    campos = ['Nome', 'Marca', 'Unidade', 'Preço Primário', 'Preço Secundário']
    file = 'ProdutosContinente.csv'
    csvo = open(file,'w')
    csvwriter = csv.writer(csvo)
    csvwriter.writerow(campos)

    html = requests.get(link).text
    soup = BS(html,"html.parser")

    categorycolumn = soup.find(["ul"],class_="dropdown-menu item-shadow").find(['div'],class_="container-dropdown-first-column")
    categorieslist = categorycolumn.find_all(['li'],class_="dropdown-item dropdown",recursive=False)
    labelelem = {}
    links = {}
    for elem in categorieslist:
        link = elem.find(['a'])["href"]
        label = elem.find(['ul'])["aria-label"]
        if not "-marcas" in label:
            links[link] = label
            labelelem[label] = elem

    i = 0
    keys = list(links.keys())
    while i < len(keys):
        link = keys[i]
        i = i+1
        print(links[link])
        html = requests.get(link).text
        soup = BS(html,"html.parser")
        totalproducts = 0
        if soup.find(['div'],class_="row product-grid no-gutters gtm-list"):
            totalproducts = soup.find(['span'],class_="product-count pull-right").text.strip().split(' ')[0]
        else:
            currentelem = labelelem[links[link]]
            linkTag2 = currentelem.find(['ul'],class_="dropdown-menu item-shadow")
            subcategorieslist = linkTag2.find_all(['li'],class_="dropdown-item dropdown",recursive=False)
            if not subcategorieslist:
                subcategorieslist = linkTag2.find_all(lambda tag: tag.name == 'li' and 
                                                        tag.get('class') == ['dropdown-item'],recursive=False)
                for subcategoryelem in subcategorieslist:
                    link2 = subcategoryelem.find(['a'])["href"]
                    print(link2)
                    links[link2] = links[link] + '-' + link2.split('/')[-2].split('-')[0]
                    print('added', list(links.keys())[-1])
            else:
                for subcategoryelem in subcategorieslist:
                    link2 = subcategoryelem.find(['a'])["href"]
                    label2 = subcategoryelem.find(['ul'])["aria-label"]
                    print(link2)
                    if not "-marcas" in label2:
                        links[link2] = label2
                        print('added', list(links.keys())[-1])
                        labelelem[label2] = subcategoryelem
            keys = list(links.keys())
            continue

        print(totalproducts)

        for j in range(0,int(totalproducts),2000):
            if(int(totalproducts)<=36):
                searchlink = link
            else:
                searchlink = f"https://www.continente.pt/on/demandware.store/Sites-continente-Site/default/Search-UpdateGrid?cgid={links[link]}&pmin=0.01&start={j}&sz=2000"
            
            html = requests.get(searchlink).text
            soup = BS(html,"html.parser")

            products = soup.find_all(['div'],class_="col-12 col-sm-3 col-lg-2 productTile")
            rows = []
            print('total',len(products))
            for product in products:
                
                name = product.find(['a'],class_="ct-tile--description").text.strip()
                productbrand = product.find(['p'],class_="ct-tile--brand").text.strip() if product.find(['p'],class_="ct-tile--brand") else None
                productquantity = product.find(['p'],class_="ct-tile--quantity").text.strip()
                
                pp = product.find(['span'],class_="sales ct-tile--price-primary")
                sp = product.find(['div'],class_="ct-tile--price-secondary")

                ppu = pp.find(['span'],class_="ct-price-formatted").text.strip() + pp.find(['span'],class_="ct-m-unit").text.strip()
                if sp:
                    spu = sp.find(['span'],class_="ct-price-value").text.strip() + sp.find(['span'],class_="ct-m-unit").text.strip()
                else:
                    spu = None

                rows.append([name,productbrand,productquantity,ppu,spu])
                # print(name)
                # print(ppu)
                # print(spu)

            csvwriter.writerows(rows)



getProdutosPagina('https://www.continente.pt')


