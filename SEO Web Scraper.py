from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

class scraper():

    def __init__(self, url):
        self.url = url

    def run_scraper(self):

        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(executable_path="C:\\Users\\Mukul\\PycharmProjects\\pythonProject\\SeleniumScripts\\chromedriver.exe", options=options)
        driver.get(self.url)
        src = driver.page_source
        soup = bs(src, features = "html.parser")

        # reading the head of the webpage

        head = soup.find('head')

        # extracting the title of the page
        self.page_title = head.find("title").get_text()

        # extracting the page description
        page_description = head.find(attrs = {"name": 'description'})
        self.page_description = page_description["content"]

        # extracting the meta keywords of the page
        meta_key = head.find('meta', attrs = {"name": "keywords"})
        self.meta_keywords = meta_key["content"]

        # extracting the page h1
        self.h1 = soup.find("h1").get_text()

        # extracting the page h2
        h2_list = soup.find_all("h2")
        self.h2 = [i.get_text().strip() for i in h2_list]

        # extracting the image alt tags of the page
        alt_tags_list = [key.get('alt') for key in soup.find_all("img")]

        # cleaning of alt tags list
        modified_alt_tags = []
        self.modified_alt_tags = modified_alt_tags

        for i in alt_tags_list:
            if i not in re.findall(".*svg$|.*png", str(i)):
                modified_alt_tags.append(i)
            else:
                pass

        # extracting the anchor text and links from the page
        internal_links = {}

        for link in soup.select("p, a"):
            if 'href' in link.attrs:
                anchors = link.get_text()
                internal_links[anchors] = link.attrs['href']
            else:
                continue

        self.internal_links_df = pd.DataFrame([internal_links.keys(), internal_links.values()], index = ["Anchors", "Links"]).T

    def check_h1(self):
        print("H1: {} \n Length: {}".format(self.h1, len(self.h1)))

    def check_title(self):
        print("Page Title: {} \n Length: {}".format(self.page_title, len(self.page_title)))

    def check_description(self):
        print("Page Description: {} \n Length: {}".format(self.page_description, len(self.page_description)))

    def check_keywords(self):
        print("Meta Keywords: {}".format(self.meta_keywords))

    def check_alt_tags(self):
        print(self.modified_alt_tags)

    def check_int_links(self):
        return self.internal_links_df

    def check_h2(self):
        print(self.h2)


scrape = scraper('https://www.healthkart.com')
scrape.run_scraper()
scrape.check_h1()
scrape.check_title()
scrape.check_description()
scrape.check_keywords()
scrape.check_alt_tags()
scrape.check_h2()
scrape.check_int_links()