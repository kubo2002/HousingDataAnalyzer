import pandas as pd
import matplotlib.pyplot as pl

class Analysis:

    def __init__(self, path: str):
        self.data = pd.read_csv(path)

    def avg_price_by_type(self):
        avg_price = self.data.groupby("listing_type")["price"].mean()

        avg_price.plot(kind="bar", color=["green", "orange"])
        pl.title("Average price by listing type")
        pl.xlabel("Typ inzerátu")
        pl.ylabel("Priemerná cena (€)")
        pl.grid(True)
        pl.savefig("graph_price_by_type.png")


    def number_of_sales_by_cities(self):
        city_counts = self.data["city"].value_counts()

        city_counts.plot(kind="bar", color="skyblue")
        pl.title("Počet inzerátov podľa mesta")
        pl.xlabel("Mesto")
        pl.ylabel("Počet inzerátov")
        pl.xticks(rotation=45)
        pl.tight_layout()
        pl.grid(axis="y")
        pl.savefig("graph_of_sales_by_cities.png")

    def avg_price_by_type(self):
        df_sale = self.data[self.data['listing_type'] == 'sale']

        avg_price_by_type = df_sale.groupby('type')['price'].mean()

        avg_price_by_type.plot(kind='barh', color='green')
        pl.title('Average price by type (sale only)')
        pl.xlabel('Cena (€)')
        pl.ylabel('Typ bytu')
        pl.grid(True)
        pl.tight_layout()
        pl.savefig("graph_avg_price_by_type.png")

