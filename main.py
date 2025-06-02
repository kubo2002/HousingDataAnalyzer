from analysis.Analysis import Analysis
from scrapper.RawData import RawData

if __name__ == '__main__':
    scrapper = RawData("https://www.nehnutelnosti.sk/vysledky")
    scrapper.scrape()
    scrapper.save_to_csv("data/raw_data.csv")

    analyzer =Analysis("data/raw_data.csv")
    #analyzer.avg_price_by_type()
    #analyzer.number_of_sales_by_cities()
    analyzer.avg_price_by_type()
