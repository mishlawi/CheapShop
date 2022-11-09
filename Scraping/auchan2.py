from bs4 import BeautifulSoup as BS
import requests
import re
import math

# sites = ['produtos-frescos','alimentacao','bebidas-e-garrafeira','limpeza-da-casa-e-roupa','beleza-e-higiene','o-mundo-do-bebe','biologicos-e-escolhas-alimentares','tecnologia-e-eletrodomesticos','saude-e-bem-estar','animais','tecnologia-e-eletrodomesticos','brinquedos-papelaria-e-livraria','casa-e-jardim','bricolage-e-renovacoes','automovel-desporto-e-outdoor','produtos-locais','loja-gourmet']
sites = [
    'produtos-frescos',
    'alimentacao',
    "limpeza-da-casa-e-roupa",
    "beleza-e-higiene",
    "o-mundo-do-bebe",
    "biologicos-e-escolhas-alimentares",
    "saude-e-bem-estar",
    "animais",
    "tecnologia-e-eletrodomesticos",
    "brinquedos-papelaria-e-livraria",
    "bricolage-e-renovacoes",
    "automovel-desporto-e-outdoor",
    "produtos-locais",
    "loja-gourmet",
]


#* "animais", "mundo do bebe","beleza e higiene" é especifico
#? "limpeza da casa", "biologicos" , "brinquedos papelaria e livraria", "bricolage e renovacoes", "automovel", "produtos locais", "gourmet" é generico
#! restantes divididos em subcategorias, alimentacao tem pelo menos uma subcategoria que é especifica


def getPaginas():
    for site in sites:
        link = "https://www.auchan.pt/pt/" + site + "/"
        getCategorias(link)


def getCategorias(website):
    s = requests.Session()
    html = s.get(website).text
    soup = BS(html, "html.parser")
    try: 
        categorias = soup.find("ul", class_="sub-categories__container")
        links = [elem["href"] for elem in categorias.find_all("a")] 
        print("ºººººººººººººººººººººººº CATEGORIA ºººººººººººººººººººººººººº")       
        print("\n------>" ,website)
        print("\n------------------------------------------------------------")
        print("\n.................... SUBCATEGORIAS ...........................\n")
        for link in links: # categorias com subcategorias #? 'produtos-frescos','alimentacao', 'bebidas', 'tecnologia', 'saude', 'casa & jardim'
            subCategoriesInfo(link) 
        print("\nFIM DAS SUBCATEGORIAS DO SITE", website,'\n')
    
    except AttributeError: # categorias sem subcategorias -> #? "limpeza da casa", "biologicos" , "brinquedos papelaria e livraria", "bricolage e renovacoes", "automovel", "produtos locais", "gourmet" é generico
        # consegues ter todas as categorias numa pagina
        try:
            subCategoriesInfo(website)
            
        except AttributeError:
            print("[!] DIFERENTE [!]", website,'\n')
 
def subCategoriesInfo(link):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(link)
    print("\n")
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html, "html.parser")
    try:
        cgidRaw = soup.find("meta", property="og:url")["content"]
    except TypeError:
        print("página",link, "não carrega\n")
    else:
        cgid = re.split("cgid=", cgidRaw)[1]
        numberRaw = soup.find("div", class_="auc-search-results auc-js-search-results-count").text
        number = re.split("de", numberRaw)[1]
        number = re.split(" ", number.lstrip())[0]  # numero de produtos de cada categoria
        products = []
        if "," in number:
            number = number.replace(",", "")
        if int(number) > 25 and int(number) < 2000:
            products = dynamic(cgid)
            print("CATEGORIA OU SUBCATEGORIA COM MENOS DE 2000 Produtos\n")
            print("Numero de produtos sacados: ", len(products))
            print("Número de produtos existentes no site: ", number)
            if (len(products)!=int(number)):
                print("\n!!!!!!!!!!!!!!!")
            print() 
        elif int(number) > 2000:  # if subcategory has more than 2 thousand products, it doesnt load in the same page
            x = 0
            aux = math.ceil(int(number) / 2000)
            while x < aux:
                products.extend(dynamicHuge(cgid, x * 2000))
                x += 1
            print("CATEGORIA OU SUBCATEGORIA COM MAIS DE 2000 Produtos\n")
            print("Numero de produtos sacados: ", len(products))
            print("Número de produtos existentes no site: ", number)
            if (len(products)!=int(number)):
                print("!!!!!!!!!!!!!!!")
            
            print()

        else:  #
            print("CATEGORIA/SUBCATEGORIA COM MENOS DE 24 PRODUTOS\n")
            products = normal(link)

# O SITE:
# Para ir buscar os produtos utilizo uma chamada que o website faz ao carregar os produtos por lazy loading, vi na tab do network na consola
# Alterando o parâmetro cgid= , o start= e o sz= consegues definir a categoria/subcategoria, o inicio da lista e o tamanho da lista (ate 2000 produtos) que queres carregar


# * seems to be working for every case
def dynamic(cgid):
    s = requests.Session()
    html = s.get(f"https://www.auchan.pt/on/demandware.store/Sites-AuchanPT-Site/pt_PT/Search-UpdateGrid?cgid={cgid}&prefn1=soldInStores&prefv1=000&start=0&sz=2000&next=true").text
    soup = BS(html, "html.parser")
    information = []
    produtosTag = soup.find_all("div", class_="auc-product")

    for produtoTag in produtosTag:
        nomeProduto = produtoTag.find("a", class_="link").text

        try:
            preco = produtoTag.find("span", class_="value").text

            precoAntes = ""
            if "from" in preco:  # promocao esta no formato price reduced FROM X TO Y
                preco = re.split("from", preco)[1].strip()
                preco = preco.replace("\n", "")
                precoAntes = re.split("to", preco)[0].strip()
            preco = preco.replace("\n", "")
            preco = preco.replace("to",'')
            precoUnidade = produtoTag.find("span", class_="auc-measures--price-per-unit").text.strip()
            value = (nomeProduto, preco, precoUnidade, precoAntes)
            if value not in information:
                information.append(value)
        except AttributeError:
            if (nomeProduto, "", "", "") not in information:
                information.append((nomeProduto, "", "", ""))
    return information


# ? works but gathers more than the total number, there is the need to normalize the final list
def dynamicHuge(cgid, start):
    s = requests.Session()
    html = s.get( 
         f"https://www.auchan.pt/on/demandware.store/Sites-AuchanPT-Site/pt_PT/Search-UpdateGrid?cgid={cgid}&prefn1=soldInStores&start={start}&sz=2000"
    ).text
    soup = BS(html, "html.parser")
    information = []
    produtosTag = soup.find_all("div", class_="auc-product")

    for produtoTag in produtosTag:
        nomeProduto = produtoTag.find("a", class_="link").text
        try:
            preco = produtoTag.find("span", class_="value").text
            precoAntes = ""
            if "from" in preco:  # promocao esta no formato price reduced FROM X TO Y
                preco = re.split("from", preco)[1].strip()
                preco = preco.replace("\n", "")
                preco = preco.replace("to",'')
                precoAntes = re.split("to", preco)[0].strip()
            preco = preco.replace("\n", "")
            precoUnidade = produtoTag.find(
                "span", class_="auc-measures--price-per-unit"
            ).text.strip()
            value = (nomeProduto, preco, precoUnidade, precoAntes)
            if value not in information:
                information.append(value)
        except AttributeError:
            if (nomeProduto, "", "", "") not in information:
                information.append((nomeProduto, "", "", ""))
    return information

# uma funcao para testar diretamente um determinado link em vez de correres o programa todo, exatamente igual à funcao @dynamic
def teste(link):
    html = requests.get(link).text
    soup = BS(html, "html.parser")
    information = []
    produtosTag = soup.find_all("div", class_="auc-product")

    for produtoTag in produtosTag:
        nomeProduto = produtoTag.find("a", class_="link").text
        try:
            preco = produtoTag.find("span", class_="value").text
            precoAntes = ""
            if "from" in preco:  # promocao esta no formato price reduced FROM X TO Y
                preco = re.split("from", preco)[1].strip()
                preco = preco.replace("\n", "")
                preco = preco.replace("to",'')
                precoAntes = re.split("to", preco)[0].strip()  # ha alguma coisa que faz apanhar o "to" também
            preco = preco.replace("\n", "")
            precoUnidade = produtoTag.find(
                "span", class_="auc-measures--price-per-unit"
            ).text.strip()
            information.append((nomeProduto, preco, precoUnidade, precoAntes))
        except AttributeError:
            information.append((nomeProduto, "", "", ""))
    print(information)
    print(len(information))
    return information


# if page is not loaded with lazy loading ~
# isto acontece por exemplo na subcategoria ovos, em que a pagina so tem 21 elementos e se fores ao html  como nas restantes paginas, aparecem lá produtos de outras categorias
def normal(link):
    s = requests.Session()
    html = s.get(link).text
    soup = BS(html, "html.parser")
    groupTag = soup.find_all("div", class_="tile-body auc-product-tile__body")
    information = []
    for elem in groupTag:
        nomeProduto = elem.find("a", class_="link").text
        preco = elem.find("span", class_="value").text.strip()
        precoUnidade = elem.find(
            "span", class_="auc-measures--price-per-unit"
        ).text.strip()
        information.append(
            (nomeProduto, preco, precoUnidade, "")
        )  #TODO apanhar descontos

getPaginas()