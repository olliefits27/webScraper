from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import re

chrome_options = Options()
driver = webdriver.Chrome()

query = input("Enter query to search for: ")
url = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={query}&_sacat=0&rt=nc&LH_PrefLoc=1"

driver.get(url)
page_source = driver.page_source
content = BeautifulSoup(page_source, "html.parser")

no_pages = content.find_all("a", attrs={"class":"pagination__item"})
no_pages = max([int(i.text) for i in no_pages])

listing_list = []
price_list = []

for i in range(no_pages):
    listings = content.find_all("div", attrs={"class":"s-item__title"})
    for listing in listings:
        listing_list.append(' '.join(re.findall(r"[a-zA-Z0-9]+", listing.text)))

    prices = content.find_all("span", attrs={"class":"s-item__price"})
    for price in prices:
        price_list.append(float(''.join(re.findall(r"[a-zA-Z0-9]+", price.text)))/100)

    button = driver.find_element(By.CLASS_NAME, "pagination__next").click()

listing_list = listing_list[1:]
price_list = price_list[1:]

ebay_dict = {"listing_name": listing_list,
             "price": price_list}

df = pd.DataFrame(ebay_dict)

df.to_csv(f"ebay_listings_for_{query}.csv", index=False)