import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

class HockeyScraper:
    def __init__(self):
        self.base_url = "https://www.scrapethissite.com/pages/forms/?q="

    def get_team_data(self, team_name):
        url = f"{self.base_url}{team_name.replace(' ', '%20')}"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": f"Impossible de récupérer les données (Code {response.status_code})"}

        soup = BeautifulSoup(response.text, 'html.parser')
        teams = soup.find_all("tr", class_="team")

        if not teams:
            return {"message": "Aucune équipe trouvée"}

        data = []
        for team in teams:
            # Vérifier l'existence des balises pour éviter les erreurs
            name = team.find("td", class_="name")
            year = team.find("td", class_="year")
            wins = team.find("td", class_="wins")
            losses = team.find("td", class_="losses")
            ot_losses = team.find("td", class_="ot-losses")
            win_percentage = team.find("td", class_="pct")
            goals_for = team.find("td", class_="gf")
            goals_against = team.find("td", class_="ga")

            if None in (name, year, wins, losses, ot_losses, win_percentage, goals_for, goals_against):
                continue  # Passer cette ligne si une donnée est manquante

            data.append({
                "Nom": name.text.strip(),
                "Année": year.text.strip(),
                "Victoires": wins.text.strip(),
                "Défaites": losses.text.strip(),
                "OT Losses": ot_losses.text.strip(),
                "Win %": win_percentage.text.strip(),
                "Goals For": goals_for.text.strip(),
                "Goals Against": goals_against.text.strip()
            })

        if data:
            self.save_to_csv(data, team_name)
            return data
        else:
            return {"message": "Aucune donnée exploitable trouvée"}

    def save_to_csv(self, data, team_name):
        df = pd.DataFrame(data)

        # Normalisation du nom de fichier
        base_filename = f"static/hockey_stats_{team_name.replace(' ', '_').lower()}"

        filename = f"{base_filename}.csv"

        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Données sauvegardées dans {filename}")
