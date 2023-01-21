import subprocess
import schedule

import Scraping.auchan
import Scraping.pingodoce


def runscrapers():
    print("starting scrapers...")
    Scraping.auchan.main()
    Scraping.pingodoce.main()

    print("uploading json files to db...")
    subprocess.run(['npm', 'i', 'mysql2'])
    subprocess.run(['node', 'Database/uploadJSON.js'])


def main():
    runscrapers()
    schedule.every().day.at("00:00").do(runscrapers)

    while True:
        schedule.run_pending()


main()
