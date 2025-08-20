import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


class PaloAltoScraper:
    """Scraper for Palo Alto Software End-of-Life product tables using XPath only."""

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.data = []

    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='mainParsys parsys']")))

    def parse_date(self, date_str):
        """Convert to yyyy-mm-dd format, keep original if parsing fails."""
        if not date_str or date_str.strip() == "":
            return ""
        for fmt in ["%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except:
                continue
        return date_str.strip()

    def scrape_tables(self):
        """Scrape all software tables inside mainParsys."""
        tables = self.driver.find_elements(By.XPATH, "//div[@class='text baseComponent parbase section']//table")

        for t_index, table in enumerate(tables, start=1):
            # try software name from b-tag OR thead
            try:
                software_name = table.find_element(By.XPATH, ".//tbody/tr/td[@colspan='3']//b").text.strip()
            except:
                try:
                    software_name = table.find_element(By.XPATH, ".//thead").text.strip()
                except:
                    software_name = f"Unknown_Table_{t_index}"

            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            # Special handling for 2nd table (QRadar SaaS Products)
            if "QRadar SaaS" in software_name or t_index == 2:
                for row in rows:
                    cols = row.find_elements(By.XPATH, ".//td")
                    if len(cols) > 0:
                        for col in cols:
                            col_text = col.text.strip()
                            if col_text and col_text != "EOL Date":
                                self.data.append({
                                    "Software Name": col_text,
                                    "Version": "",
                                    "Release Date": "",
                                    "EOL Date": ""
                                })
                continue

            # Normal tables
            for row in rows:
                cols = row.find_elements(By.XPATH, ".//td")
                if len(cols) >= 3:
                    version = cols[0].text.strip()
                    release_date = self.parse_date(cols[1].text.strip())
                    eol_date = self.parse_date(cols[2].text.strip())

                    self.data.append({
                        "Software Name": software_name,
                        "Version": version,
                        "Release Date": release_date,
                        "EOL Date": eol_date
                    })

    def to_dataframe(self):
        return pd.DataFrame(self.data)

    def save_to_csv(self, filename="paloalto_software_eol.csv"):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        return filename

    def close(self):
        self.driver.quit()


scraper = PaloAltoScraper(headless=True)
scraper.open_website("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
scraper.scrape_tables()
df = scraper.to_dataframe()
print(df.head())   # preview
scraper.save_to_csv("paloalto_software_eol.csv")
scraper.close()
