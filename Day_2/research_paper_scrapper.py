"""File for scraping research papers from multiple public repositories."""
import os
import json
import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed


class ResearchPaperScraper:
    """Scraper to fetch research paper metadata from multiple sources."""

    def __init__(self, driver_path="./chromedriver.exe", headless=True):
        """Initialize the web driver and storage."""
        self.driver_path = os.path.abspath(driver_path)
        self.headless = headless
        self.output_folder = "output"
        os.makedirs(self.output_folder, exist_ok=True)
        self.all_results = []  # This is our collector

    def _setup_driver(self):
        """Configure Selenium WebDriver."""
        chrome_options = webdriver.ChromeOptions()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def scrape_arxiv(self, query, max_results=10):
        """Scrape research papers from arXiv."""
        driver = self._setup_driver()
        results = []
        try:
            search_url = f"https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&size={max_results}&order=-announced_date_first"
            driver.get(search_url)
            time.sleep(2)

            papers = driver.find_elements(By.CSS_SELECTOR, "li.arxiv-result")
            results = [
                {
                    "title": p.find_element(By.CSS_SELECTOR, "p.title").text.strip(),
                    "authors": p.find_element(By.CSS_SELECTOR, "p.authors").text.replace("Authors:", "").strip(),
                    "date": p.find_element(By.CSS_SELECTOR, "p.is-size-7 span").text.strip(),
                    "source": "arXiv",
                    "link": p.find_element(By.CSS_SELECTOR, "p.list-title a").get_attribute("href")
                }
                for p in papers
            ]
        except Exception as e:
            print(f"[ERROR] arXiv scraping failed: {e}")
        finally:
            driver.quit()
        return results

    def scrape_citeseerx(self, query, max_results=10):
        """Scrape research papers from CiteSeerX."""
        driver = self._setup_driver()
        results = []
        try:
            search_url = f"https://citeseerx.ist.psu.edu/search?q={query.replace(' ', '+')}&submit=Search&sort=rlv&t=doc"
            driver.get(search_url)
            time.sleep(2)

            papers = driver.find_elements(By.CSS_SELECTOR, "div.result")
            results = [
                {
                    "title": p.find_element(By.CSS_SELECTOR, "a.doc_details").text.strip(),
                    "authors": "Unknown",
                    "date": "Unknown",
                    "source": "CiteSeerX",
                    "link": p.find_element(By.CSS_SELECTOR, "a.doc_details").get_attribute("href")
                }
                for p in papers[:max_results]
            ]
        except Exception as e:
            print(f"[ERROR] CiteSeerX scraping failed: {e}")
        finally:
            driver.quit()
        return results

    def scrape_core(self, query, max_results=10):
        """Scrape research papers from CORE."""
        driver = self._setup_driver()
        results = []
        try:
            search_url = f"https://core.ac.uk/search?q={query.replace(' ', '+')}"
            driver.get(search_url)
            time.sleep(2)

            papers = driver.find_elements(By.CSS_SELECTOR, "div.result__body")
            results = [
                {
                    "title": p.find_element(By.CSS_SELECTOR, "a.result__title").text.strip(),
                    "authors": "Unknown",
                    "date": "Unknown",
                    "source": "CORE",
                    "link": p.find_element(By.CSS_SELECTOR, "a.result__title").get_attribute("href")
                }
                for p in papers[:max_results]
            ]
        except Exception as e:
            print(f"[ERROR] CORE scraping failed: {e}")
        finally:
            driver.quit()
        return results

    def collect_results(self, query, max_results=10):
        """Collector method to gather from multiple sources in parallel."""
        sources = [
            self.scrape_arxiv,
            self.scrape_citeseerx,
            self.scrape_core
        ]

        with ThreadPoolExecutor() as executor:
            future_to_source = {
                executor.submit(source, query, max_results): source.__name__
                for source in sources
            }
            for future in as_completed(future_to_source):
                source_name = future_to_source[future]
                try:
                    results = future.result()
                    print(f"[INFO] {source_name} returned {len(results)} results.")
                    self.all_results.extend(results)
                except Exception as e:
                    print(f"[ERROR] {source_name} failed: {e}")

    def save_data(self):
        """Save collected results to JSON and CSV."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(self.output_folder, f"papers_{timestamp}.json")
        csv_path = os.path.join(self.output_folder, f"papers_{timestamp}.csv")

        try:
            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(self.all_results, jf, ensure_ascii=False, indent=4)

            with open(csv_path, "w", encoding="utf-8", newline="") as cf:
                writer = csv.DictWriter(cf, fieldnames=self.all_results[0].keys())
                writer.writeheader()
                writer.writerows(self.all_results)

            print(f"[INFO] Data saved to {json_path} and {csv_path}")
        except Exception as e:
            print(f"[ERROR] Saving data failed: {e}")

    def generate_summary(self):
        """Generate summary statistics."""
        summary = {
            "total_papers": len(self.all_results),
            "sources_used": len(set(r["source"] for r in self.all_results)),
            "duplicates_removed": 0
        }
        summary_path = os.path.join(self.output_folder, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as sf:
            json.dump(summary, sf, indent=4)
        print(f"[INFO] Summary saved: {summary_path}")


# Example usage (no main method)
scraper = ResearchPaperScraper(headless=False)
scraper.collect_results("machine learning agriculture", max_results=5)
scraper.save_data()
scraper.generate_summary()
