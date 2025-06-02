from scrapper.RawData import RawData

if __name__ == '__main__':
    scrapper = RawData("https://www.nehnutelnosti.sk/vysledky")
    scrapper.scrape()
    scrapper.save_to_csv("data/raw_data.csv")

