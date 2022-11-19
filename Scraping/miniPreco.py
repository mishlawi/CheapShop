from bs4 import BeautifulSoup as BS
import requests

import csv
import os

rows = []

def getProdutosPagina(link):
       
    html = requests.get(link).text
    soup = BS(html,"html.parser")
    titulo = soup.find(["meta"],property="og:description")["content"]
    
    tags = soup.find(["div"],class_="product-list--row")
    produtos = tags.find_all(["a"])
    
    ## CSV BUILD
            
    campos = ['NAME','BRAND','QUANTITY','PRICE','PPU','OLDPRICE','OLDPPU','EAN']     # PpU = PRICE PER UNIT

    if not os.path.exists("csvProdutos/ProdutosMP"):
        os.makedirs("csvProdutos/ProdutosMP")
    file = 'csvProdutos/ProdutosMP/'+ titulo.replace(" ","").lower()+'.csv'
    csvo = open(file,'w')
    csvwriter= csv.writer(csvo)
    csvwriter.writerow(campos)

    
    for elem in produtos:
        
        nomeProduto = elem.find(["span"],class_="details").text.strip()         # as a reminder:
        tagPrecosGeral = elem.find(["div"],class_="price_container") # tag com a tag com o preço e a tag com o preço/kg
        tagPrecos = tagPrecosGeral.find(["p"],class_="price") # tag com o preço
        tagPrecosKg = tagPrecosGeral.find(["p"],class_="pricePerKilogram") # tag com o preço por kilo/preço por unidade

        oldPrice = ''
        if old := tagPrecos.find(["s"]):      #! significa que sofreu uma promoção
            oldPrice = old.text.strip()               
            old.string = ''
        precoProduto = tagPrecos.text.strip()  
        if tagPrecos.text!="\n":
            
            oldPriceKg = ''
            if old := tagPrecosKg.find(["s"]):     #! significa que sofreu uma promoção
                oldPriceKg = old.text.strip()[1:-2]
                old.string = ''
            precoKg = tagPrecosKg.text.strip()[1:-2]
            

            rows.append([nomeProduto,'','',precoProduto,precoKg,oldPrice,oldPriceKg,''])
        else:
            pass                    #data-productCode
         
    nextpage = soup.find(["li"], class_ ="next").find(["a"])["href"]
    if nextpage == '#':
        csvwriter.writerows(rows)
        rows.clear()
    else:     
        getProdutosPagina("https://www.minipreco.pt" + nextpage)


def getPaginas(link):
    html = requests.get(link).text
    soup = BS(html,"html.parser")
    paginasTag = soup.find(["ul"],class_="nav-submenu")
    paginas = paginasTag.find_all(["div"],class_="category-link")

    links = []
    for pagina in paginas:
        linkIncomplete = pagina.find(["a"])["href"]
        categoria = pagina.find(["a"]).text.strip().split('-')[0]
        link = "https://www.minipreco.pt" + str(linkIncomplete)
        links.append((categoria,link))

    for elem in links:
        getProdutosPagina(elem[1])
        print("---->" + elem[0] + "     FEITO")
   

def main():
    getPaginas("https://www.minipreco.pt")

if __name__ == "__main__":
    main()


