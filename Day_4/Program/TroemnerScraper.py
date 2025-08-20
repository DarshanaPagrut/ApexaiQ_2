"""Scraper for Troemner calibration weights product data using XPath only.

This script uses Selenium to scrape product information from the Troemner
OIML Calibration Weight Sets listing page. It extracts the following fields:

- vendor (fixed as "Troemner")
- productName
- model
- description
- productURL
- cost

The results are stored in a pandas DataFrame and exported to CSV.
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TroemnerScraper:
    """Scraper for Troemner product listings."""

    def __init__(self, headless=True):
        """Initialize scraper and WebDriver."""
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.data = []
        self.vendor = "Troemner"

    def _setup_driver(self):
        """Set up Chrome WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        """Open the website and wait for products."""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h3[@class='title text-left hover-highlight header-padding headerGtmEvent']"))
        )

    def scroll_and_load(self):
        """Scroll to load all products."""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrape_products(self):
        """Scrape product data from listing page."""
        products = self.driver.find_elements(
            By.XPATH, "//h3[@class='title text-left hover-highlight header-padding headerGtmEvent']"
        )
        print(f"Found {len(products)} products")

        for product in products:
            try:
                link_elem = product.find_element(By.XPATH, ".//a")
                product_name = link_elem.text.strip()
                product_url = link_elem.get_attribute("href")

                model_elem = product.find_element(By.XPATH, ".//span[@class='code hover-highlight hidden-xs']")
                model = model_elem.text.strip()

                desc_elem = product.find_element(By.XPATH, "../following-sibling::div//div[@class='description product-description']")
                description = desc_elem.text.strip()

                price_elem = product.find_element(By.XPATH, "../following-sibling::div//span[@class='priceValue']")
                cost = price_elem.text.strip()

                self.data.append({
                    "vendor": self.vendor,
                    "productName": product_name,
                    "model": model,
                    "description": description,
                    "productURL": product_url,
                    "cost": cost
                })
            except Exception as e:
                print("Error scraping one product:", e)

    def save_to_csv(self, filename="troemner_products.csv"):
        """Save scraped data to CSV."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} products to {filename}")
        return df

    def close(self):
        """Close WebDriver."""
        self.driver.quit()

# Usage
scraper = TroemnerScraper(headless=False)
scraper.open_website("https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944")
scraper.scroll_and_load()
scraper.scrape_products()
df = scraper.save_to_csv("troemner_products.csv")
scraper.close()

