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
import re


class PaloAltoScraper:
    """Scraper for Palo Alto hardware End-of-Life product data using XPath only."""

    def __init__(self, headless=True):
        """Initialize scraper with WebDriver and default settings."""
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 15)
        self.data = []
        self.vendor = "Palo Alto"

    def _setup_driver(self):
        """Configure and return Chrome WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        """Open the target website and wait for table data to load."""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//tbody//tr")))

    def _format_date(self, date_str):
        """Convert date to yyyy-mm-dd format (handles short/full month names and ordinals)."""
        if not date_str:
            return ""

        # Remove ordinal suffixes (st, nd, rd, th)
        clean_date = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str.strip())

        # Try parsing with both short and full month formats
        for fmt in ("%B %d, %Y", "%b %d, %Y"):  # January vs Jan
            try:
                return datetime.strptime(clean_date, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str

    def extract_table_headers(self):
        """Extract column names from table header (th tags) using XPath."""
        headers = self.driver.find_elements(By.XPATH, "//thead//tr/th")
        return [h.text.strip() for h in headers]

    def extract_data(self):
        """Extract all product rows and store as dictionaries using XPath only."""
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")

        for row in rows:
            tds = row.find_elements(By.XPATH, "./td")
            if len(tds) < 6:   # Skip rows without enough columns
                continue

            # Product names (replace <br> with commas)
            product_html = tds[0].get_attribute("innerHTML")
            product_name = " ".join(product_html.replace("<br>", "\n").split()).strip('", ')

            # EOL date
            eol_date = self._format_date(tds[2].text.strip())

            # Resource link
            resource_link = (
                tds[3].find_element(By.XPATH, ".//a").get_attribute("href")
                if tds[3].find_elements(By.XPATH, ".//a") else ""
            )

            # Recommended replacement (replace <br> with commas)
            replacement_html = tds[5].get_attribute("innerHTML")
            replacement = " ".join(replacement_html.replace("<br>", "\n ").split()).strip()

            # One row per original <tr>
            record = {
                "vendor": self.vendor,
                "productName": product_name,
                "EOL Date": eol_date,
                "resource": resource_link,
                "Recommended replacement": replacement
            }
            self.data.append(record)


    def to_dataframe(self):
        """Convert collected data to pandas DataFrame and format dates."""
        df = pd.DataFrame(self.data)
        if "EOL Date" in df.columns:
            df["EOL Date"] = df["EOL Date"].apply(self._format_date)
        return df

    def save_to_csv(self, filename="palo_alto_eol5.csv"):
        """Save extracted data to CSV with formatted dates."""
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        return filename

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()


scraper = PaloAltoScraper(headless=True)
scraper.open_website("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates")
scraper.extract_data()
df = scraper.to_dataframe()
scraper.save_to_csv("palo_alto_eol5.csv")
scraper.close()
