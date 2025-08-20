import re
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class PaloAltoScraper:
    """Scraper for Palo Alto Software End-of-Life tables using XPath only."""

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 20)
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

    def format_date(self, date_str):
        """Convert many date formats to yyyy-mm-dd."""
        if not date_str or date_str.strip() == "":
            return ""
        date_str = date_str.strip()

        # Try multiple formats
        fmts = ["%m/%d/%Y", "%m/%d/%y", "%B %d, %Y", "%b %d, %Y", "%Y-%m-%d"]
        for fmt in fmts:
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except:
                continue
        return date_str  # return as-is if parsing fails

    def scrape_tables(self):
        """Scrape software tables with regex-based column detection."""

        tables = self.driver.find_elements(By.XPATH, "//div[@class='text baseComponent parbase section']//table")
        prev_software_name = ""

        for t_index, table in enumerate(tables, start=1):
            # --- Software Name ---
            try:
                software_name = table.find_element(By.XPATH, ".//tbody/tr[2]/td/p/b").text.strip()
            except:
                try:
                    software_name = table.find_element(By.XPATH, ".//thead/tr[2]/th/p/b").text.strip()
                except:
                    software_name = ""

            if not software_name:
                software_name = prev_software_name if prev_software_name else f"Unknown_Table_{t_index}"

            prev_software_name = software_name

            # --- Column Headings ---
            col_map = {"version": None, "release": None, "eol": None}
            headings = table.find_elements(By.XPATH, ".//tbody/tr[3]/td/b")
            for idx, h in enumerate(headings):
                h_text = h.text.strip().lower()
                if re.search(r"version", h_text):
                    col_map["version"] = idx
                elif re.search(r"release", h_text):
                    col_map["release"] = idx
                elif re.search(r"end[\s-]?of[\s-]?life", h_text) or re.search(r"eol", h_text):
                    col_map["eol"] = idx

            # --- Data Rows ---
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            for row in rows:
                cols = row.find_elements(By.XPATH, ".//td")
                if not cols:
                    continue

                # skip heading row
                if any(c.find_elements(By.XPATH, ".//b") for c in cols):
                    continue

                def safe_get(col_key):
                    idx = col_map.get(col_key)
                    if idx is not None and idx < len(cols):
                        return cols[idx].text.strip()
                    return ""

                version = safe_get("version")
                release_date = safe_get("release")
                eol_date = safe_get("eol")

                # format dates
                release_date = self.format_date(release_date)
                eol_date = self.format_date(eol_date)

                if not any([version, release_date, eol_date]):
                    continue  # skip empty rows

                self.data.append({
                    "Software Name": software_name,
                    "Version": version,
                    "Release Date": release_date,
                    "EOL Date": eol_date
                })

    def to_dataframe(self):
        return pd.DataFrame(self.data, columns=["Software Name", "Version", "Release Date", "EOL Date"])

    def save_to_csv(self, filename="paloalto_software_eol3.csv"):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        return filename

    def close(self):
        self.driver.quit()


scraper = PaloAltoScraper(headless=True)
scraper.open_website("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
scraper.scrape_tables()
df = scraper.to_dataframe()
print(df.head(20))   # preview
scraper.save_to_csv("paloalto_software_eol3.csv")
scraper.close()
