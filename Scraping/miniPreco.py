from unicodedata import category
from bs4 import BeautifulSoup as BS
import requests
import re
import csv


rows = []

def getProdutosPagina(link):
       
    html = requests.get(link).text
    soup = BS(html,"html.parser")
    titulo = soup.find(["meta"],property="og:description")["content"]
    
    tags = soup.find(["div"],class_="product-list--row")
    produtos = tags.find_all(["a"])
    
    ## CSV BUILD
        
        #
        # PpU = Preço por Unidade
    
    campos = ['Nome', 'Preço','Preço Antigo', 'PpU', 'PpU Antigo']
    file = 'ProdutosMP/'+titulo.replace(" ","").lower()+'.csv'
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
        #print(tagPrecos.contents)
        if tagPrecos.text!="\n":
            
            oldPriceKg = ''
            if old := tagPrecosKg.find(["s"]):     #! significa que sofreu uma promoção
                oldPriceKg = old.text.strip()[1:-2]
                old.string = ''
            precoKg = tagPrecosKg.text.strip()[1:-2]
            
            #

            #print(oldPrice)
            #print(oldPriceKg)

            #

            # print(nomeProduto)        
            # print(precoProduto)
            # print(precoKg)

            #! Ha um codigo de produto (penso que seja só interno)
            rows.append([nomeProduto,precoProduto,oldPrice,precoKg,oldPriceKg])
        else:
            pass                    #data-productCode
         
    nextpage = soup.find(["li"], class_ ="next").find(["a"])["href"]
    #print(nextpage)
    if nextpage == '#':
        csvwriter.writerows(rows)
        rows.clear()
    else:     
        getProdutosPagina("https://www.minipreco.pt" + nextpage)

#getProdutosPagina("https://www.minipreco.pt/produtos/mercearia-doce/c/WEB.004.000.00000?q=%3Arelevance&page=12&disp=")





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
   
getPaginas("https://www.minipreco.pt")


