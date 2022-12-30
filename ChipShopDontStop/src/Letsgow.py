from Produto import Produto
import json


# se os dois tiverem qtd e encontrar um numero nos 2 e forem diferentes manda logo false,
# se os 2 numeros forem iguais ou nao encotrar numero num deles pesquisa palavras em comum
# barata mudou a função no cafe tropinha

def podeSerOMesmo(a, b):
    conta = 0
    pode = False

    baratata = a.getQuantidade().lower()
    baratata = baratata.replace(" ", "")

    baratata2 = b.getQuantidade().lower()
    baratata2 = baratata2.replace(" ", "")

    if not baratata == baratata2:
        return False

    auxB = b.getNome().split(" ")

    for aa in auxB:
        if aa in a.getNome().split(" ") and not aa == a.getMarca() and not aa == "DE" and not aa == "PARA" and not aa == "COM" and not aa == "SEM" and not aa == "A" and not aa == "E" and not aa == "I" and not aa == "O" and not aa == "U" and not aa == "OU":
            conta += 1

    graudecerteza = 0.5

    if conta > graudecerteza * len(auxB):
        pode = True

    return pode


def main():
    kappa = 0

    # 1oCSV TEM QUE TER EAN
    _1oJSON = 'ProdutosPingoDoce.json'
    _2oJSON = 'ProdutosFroiz.json'
    _2oCSV = 'ProdutosFroiz.csv'

    auchanMap = {}
    secondMap = {}

    auchanMapEAN = {}

    qts = 0
    i = 0
    j = 0

    try:
        path_1oJSON = "./"+_1oJSON
        myObj = open(path_1oJSON, 'r')
        data = json.load(myObj)

        for product in data:
            values = []
            for value in product.values():
                if value:
                    values.append(str(value))
                else:
                    values.append('')

            strToda = ','.join(values)
            copy = strToda.upper()

            p = Produto(copy, product['Nome'], product['Marca'], str(product['Quantidade']), str(product['Preço Primário']), str(product['Preço Por Unidade']), str(product['Promo']))
            p.setEANOriginal(product['EAN'])
            # marca e aux[1]

            if product['Marca'] in auchanMap.keys():
                lii = auchanMap.get(product['Marca'])
                lii.append(p)
                auchanMapEAN[product['EAN']] = p

            else:
                lii2 = []
                lii2.append(p)
                auchanMap[product['Marca']] = lii2
                auchanMapEAN[product['EAN']] = p

            qts += 1

    except Exception as e:
        print("An error occurred.")
        print(e)

    try:
        path_2oJSON = "./"+_2oJSON
        myObj2 = open(path_2oJSON, 'r')

        data2 = json.load(myObj2)

        for product2 in data2:
            values = []
            for value in product2.values():
                if value:
                    values.append(str(value))
                else:
                    values.append('')

            strToda = ','.join(values)
            copy2 = strToda.upper()

            # if len(aux2) > 6 or len(aux2) < 5:
            #     continue

            kappa = 0

            if product2['Nome'] == 'None' or product2['Marca'] == 'None' or product2['Quantidade'] == 'None':
                continue

            if product2['Promo'] == 'None':
                p = Produto(copy2, product2['Nome'], product2['Marca'], str(product2['Quantidade']), str(product2['Preço Primário']), str(product2['Preço Por Unidade']))
            else:
                p = Produto(copy2, product2['Nome'], product2['Marca'], str(product2['Quantidade']),str( product2['Preço Primário']), str(product2['Preço Por Unidade']), str(product2['Promo']))

            if product2['Marca'] in secondMap.keys():
                lii2 = secondMap.get(product2['Marca'])
                lii2.append(p)
            else:
                lii22 = []
                lii22.append(p)
                secondMap[product2['Marca']] = lii22

            qts += 1

    except Exception as e:
        print("An error occurred.")
        print(e)

    # associar or EANS do auchan ao 2o CSV
    for ma in auchanMap.keys():
        if ma in secondMap.keys():
            list_auchan = auchanMap.get(ma)
            list_2ndSUPER = secondMap.get(ma)

            for p1 in list_auchan:
                for p2 in list_2ndSUPER:
                    barata = podeSerOMesmo(p1, p2)
                    if barata:
                        # System.out.println("\n");
                        #System.out.println(p2.toString() + "\n pode ser igual a \n"+ p1.toString());
                        p2.addEANCopiado(p1.getEANOriginal())

    # Escrever para OUTPUT.csv os produtos com EANS encontrados
    try:
        nomeFileOutput = "OUTPUT"+_2oCSV
        file = open(nomeFileOutput, 'w')

        for ll in secondMap.values():
            for p in ll:
                num_eans = len(p.getEANCopiados())
                qual = 1

                file.write(p.getStrToda())
                file.write('[')
                for ean in p.getEANCopiados():
                    if qual == num_eans:
                        file.write(ean)
                    else:
                        file.write(ean)
                        file.write(",")
                        qual += 1
                file.write(']\n')
    except Exception as e:
        print("An error occurred.")
        print(e)

    kappa = 0


if __name__ == "__main__":
    main()
