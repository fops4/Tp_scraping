from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Add this import
import pandas as pd
import time
import os
import logging

class HockeyScraper:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

        # Configuration des options de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans affichage
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Spécifiez le chemin de votre WebDriver
        self.driver = webdriver.Chrome(service=Service("D:/cour/B3/semestre1/python/tp/tp_final/test/chromedriver.exe"), options=chrome_options)
        self.base_url = "https://www.scrapethissite.com/pages/forms/"
        self.dataset_filename = "dataset.csv"

    def dataset_exists(self):
        """Vérifie si dataset.csv existe déjà"""
        return os.path.exists(self.dataset_filename)

    def get_all_teams_data(self):
        """Scrape all pages by directly modifying the URL to increment the page number"""
        if self.dataset_exists():
            logging.info(f"Le fichier '{self.dataset_filename}' existe déjà. Le scraping sera sauté.")
            return  # Skip scraping if the dataset already exists

        page_num = 1  # Start from the first page
        all_data = []

        while True:
            logging.info(f"Scraping des données de la page {page_num}...")

            # Build the URL with the current page number
            page_url = f"{self.base_url}?page_num={page_num}&per_page=100"
            self.driver.get(page_url)
            time.sleep(2)  # Wait for the page to load

            # Get the team rows
            teams = self.driver.find_elements(By.CSS_SELECTOR, "tr.team")
            if not teams:
                logging.warning(f"Aucune équipe trouvée sur la page {page_num}. Fin du scraping.")
                break

            # Extract the data for each team
            for team in teams:
                columns = team.find_elements(By.TAG_NAME, "td")
                if len(columns) < 8:
                    continue  # Ignore if the data is incomplete

                all_data.append({
                    "Nom": columns[0].text.strip(),
                    "Année": columns[1].text.strip(),
                    "Victoires": columns[2].text.strip(),
                    "Défaites": columns[3].text.strip(),
                    "OT Losses": columns[4].text.strip(),
                    "Win %": columns[5].text.strip(),
                    "Goals For": columns[6].text.strip(),
                    "Goals Against": columns[7].text.strip()
                })

            # Increment the page number for the next iteration
            page_num += 1


            # Save the data to a CSV file
            if all_data:
                self.save_to_csv(all_data)
            else:
                logging.warning("Aucune donnée exploitable trouvée.")


    def save_to_csv(self, data):
        """Enregistre les données dans dataset.csv"""
        df = pd.DataFrame(data)
        df.to_csv(self.dataset_filename, index=False, encoding="utf-8")
        logging.info(f"Données sauvegardées dans {self.dataset_filename}")

    def close(self):
        """Ferme le navigateur"""
        self.driver.quit()
        logging.info("Navigateur fermé.")

if __name__ == "__main__":
    scraper = HockeyScraper()
    scraper.get_all_teams_data()
    scraper.close()
