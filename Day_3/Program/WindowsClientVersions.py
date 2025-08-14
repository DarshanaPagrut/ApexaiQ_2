"""File for scraping Windows Server release tables from the Microsoft Wiki page."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time


class WindowsClientVersions:
    """Scraper class to extract Windows Server tables from the Microsoft Wiki page."""
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.tables_data = {}
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)

    def _setup_driver(self):
        """Initialize and configure the Selenium WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--log-level=3")

        # Automatically install and use correct ChromeDriver
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_website(self, url):
        """Opens the given website URL."""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        time.sleep(1)

    def scrape_tables(self):
        """Scrape all tables from the opened page and combine into a single DataFrame."""
        tables = self.driver.find_elements(By.XPATH, "//table")
        all_dfs = []

        for idx, table in enumerate(tables, start=1):
            # Extract headers
            headers = [th.text.strip() for th in table.find_elements(By.XPATH, ".//th")]

            # Extract rows
            rows_data = []
            row_elements = table.find_elements(By.XPATH, ".//tr[position()>1]")
            for row in row_elements:
                cells = row.find_elements(By.XPATH, ".//td")
                row_text = [cell.text.strip() for cell in cells]
                if row_text:
                    rows_data.append(row_text)

            if headers and rows_data:
                df = pd.DataFrame(rows_data, columns=headers)
                all_dfs.append(df)

        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True).fillna("")
            return combined_df
        else:
            return pd.DataFrame()

    def save_to_csv(self, df, filename="combined_windows_tables.csv"):
        """Save the DataFrame to CSV."""
        output_path = os.path.join(self.output_folder, filename)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Data saved to: {output_path}")

    def close(self):
        """Close the browser."""
        self.driver.quit()

# Usage
scraper = WindowsClientVersions(headless=True)
scraper.open_website("https://learn.microsoft.com/en-us/windows/release-health/supported-versions-windows-client")
df = scraper.scrape_tables()
scraper.save_to_csv(df)
scraper.close()
