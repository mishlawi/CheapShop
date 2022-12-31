from Produto import Produto
import json
import re


def main():
    _1oJSON = 'ProdutosPingoDoce.json'
    _1super = re.match(r'.+?(?<=Produtos)(.+)\.json', _1oJSON)[1]
    _2oJSON = 'ProdutosAuchan.json'
    _2super = re.match(r'.+?(?<=Produtos)(.+)\.json', _2oJSON)[1]

    try:
        path_1oJSON = "./"+_1oJSON
        path_2oJSON = "./"+_2oJSON
        _1ofile = open(path_1oJSON, 'r')
        _2ofile = open(path_2oJSON, 'r')
        data1file = json.load(_1ofile)
        data2file = json.load(_2ofile)

        productCompared = {}

        for _1product in data1file:
            got_a_match = False
            for _2product in data2file:
                if _1product['EAN'] == _2product['EAN'] and _1product['EAN'] not in productCompared.keys():
                    got_a_match = True
                    newObjProduct = {
                        "Nome": _1product['Nome'],
                        "Marca": _1product['Marca'],
                        "Quantidade": _1product['Quantidade'],
                        f"Preço {_1super}": _1product['Preço Primário'],
                        f"Preço {_2super}": _2product['Preço Primário'],
                        f"Preço Por Unidade {_1super}": _1product['Preço Por Unidade'],
                        f"Preço Por Unidade {_2super}": _2product['Preço Por Unidade'],
                        f"Promo {_1super}": _1product['Promo'],
                        f"Promo {_2super}": _2product['Promo']
                    }

                    productCompared[_1product['EAN']] = newObjProduct
            
            if not got_a_match:
                _1ObjProduct = {
                    "Nome": _1product['Nome'],
                    "Marca": _1product['Marca'],
                    "Quantidade": _1product['Quantidade'],
                    f"Preço {_1super}": _1product['Preço Primário'],
                    f"Preço Por Unidade {_1super}": _1product['Preço Por Unidade'],
                    f"Promo {_1super}": _1product['Promo'],
                }

                productCompared[_1product['EAN']] = _1ObjProduct
        
        for _2product in data2file:
            if _2product['EAN'] not in productCompared.keys():
                _2ObjProduct = {
                    "Nome": _2product['Nome'],
                    "Marca": _2product['Marca'],
                    "Quantidade": _2product['Quantidade'],
                    f"Preço {_2super}": _2product['Preço Primário'],
                    f"Preço Por Unidade {_2super}": _2product['Preço Por Unidade'],
                    f"Promo {_2super}": _2product['Promo'],
                }

                productCompared[_2product['EAN']] = _2ObjProduct

        json_file = open('./output.json', 'w', encoding='utf-8')
        json.dump(productCompared, json_file, ensure_ascii=False)
    except Exception as e:
        print('An error occured!')
        print(e)


if __name__ == "__main__":
    main()