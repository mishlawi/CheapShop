import subprocess
import schedule

import Scraping.auchan
import Scraping.pingodoce


def runscrapers():
    print("starting scrapers...")
    auchanfilename = Scraping.auchan.main()
    pingofilename = Scraping.pingodoce.main()
    #auchanfilename = 'csvProdutos/ProdutosAuchan.json'
    #pingofilename = 'csvProdutos/ProdutosPingoDoce.json'

    print("uploading json files to db...")
    subprocess.run(['node', 'Database/uploadJSON.js',
                    auchanfilename, pingofilename])


def main():
    runscrapers()
    schedule.every().day.at("00:00").do(runscrapers)

    while True:
        schedule.run_pending()


main()
