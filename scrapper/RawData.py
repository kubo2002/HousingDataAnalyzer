import requests
from bs4 import BeautifulSoup
import pandas as pd

class RawData:
    """
        A web scraper for collecting raw data of real estate listings from nehnutelnosti.sk

        It fetches offers from multiple pages, simply parses useful data,
        and exports the result into a CSV file.

        """
    def __init__(self, base_url):
        """
        Initializes the scraper with the base URL (without ?page=).

        :param base_url: The root URL of the listings page.
        """
        self.base_url = base_url
        self.data = []


    def fetch_page(self, url):
        """
        Sends a GET request to the given URL and returns parsed HTML.

        :param url: The URL to fetch.
        :return: BeautifulSoup object of the page content.
        """
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def get_total_number_of_pages(self):
        """
        Finds the total number of pages with listings by locating the
        last pagination button on the first page.

        :return: Total number of pages as an integer.
        """
        url = f"{self.base_url}?page={1}"
        print(f"Scraping {url} ...")
        soup = self.fetch_page(url)

        total_number_of_pages =  soup.find_all('button', class_='MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-sizeSmall MuiPaginationItem-text MuiPaginationItem-rounded MuiPaginationItem-colorPrimary MuiPaginationItem-textPrimary MuiPaginationItem-page mui-1sslsl5');

        return int(total_number_of_pages[-1].text.strip())

    def parse_listings(self, soup):
        """
        Extracts listings from a given page's HTML soup. For each offer,
        it collects the title, price, location, and property type.

        :param soup: Parsed HTML content (BeautifulSoup).
        """
        listings = soup.find_all('div', class_='MuiBox-root mui-0')
        for offer in listings:
            """Pre kazdu ponuku zo zoznamu najde popis, cenu, lokalitu"""

            price_tag = offer.find('p', class_='MuiTypography-root MuiTypography-h5 mui-7e5awq')
            location_tag = offer.find('p', class_='MuiTypography-root MuiTypography-body2 MuiTypography-noWrap mui-3vjwr4')
            type_tag = offer.find('p', class_='MuiTypography-root MuiTypography-body2 MuiTypography-noWrap mui-1hwpzcb')


            price = price_tag.text.strip() if price_tag else 'N'
            location = location_tag.text.strip() if location_tag else 'N'
            type = type_tag.text.strip() if type_tag else 'N'

            if self.check_candidate({
                'price': price,
                'location': location,
                'type' : type
            }):
                self.data.append({
                    'price': price,
                    'location': location,
                    'type' : type
                })

    def scrape(self):
        """
        Loops through all pages and collects listing data.
        """
        pages = self.get_total_number_of_pages()
        for i in range(1, pages + 1):
            url = f"{self.base_url}?page={i}"
            print(f"Scraping {url} ...")
            soup = self.fetch_page(url)
            self.parse_listings(soup)

    def check_candidate(self, data):
        """
        Checks if all fields in the listing are valid (i.e. not 'N').

        :param data: A dictionary with listing details.
        :return: True if all values are valid, otherwise False.
        """
        count = 0
        index = 0
        for key in data:
            index += 1
            if data[key] != 'N':
                count += 1

        if count == index:
            return True
        else:
            return False

    def save_to_csv(self, filename):
        """
        Saves the collected listings to a CSV file.

        :param filename: Name of the CSV output file.
        """
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    scraper = RawData("https://www.reality.sk/zilinsky-kraj/virtualne-prehliadky/")

    scraper.scrape()

    """subory ulozi do """
    scraper.save_to_csv("raw_data.csv")