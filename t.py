boston_bruins_goals
boston_bruins_goals_vs_wins_scatter
boston_bruins_performance_distribution_1996
boston_bruins_performance_heatmap
boston_bruins_wins
boston_bruins_wins_boxplot

import pandas as pd
import numpy as np
import glob
import os

class HockeyAnalyzer:
    def __init__(self, team_name):
        self.team_name = team_name
        self.file_path = self.get_latest_file()
        if self.file_path:
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = None
            print(f"Aucun fichier trouvé pour l'équipe {team_name}.")

    def get_latest_file(self):
        """Récupère le dernier fichier CSV disponible pour l'équipe spécifiée."""
        base_filename = f"static/hockey_stats_{self.team_name.replace(' ', '_').lower()}_*.csv"
        files = glob.glob(base_filename)

        if not files:
            return None
        
        latest_file = max(files, key=os.path.getctime)
        print(f"📂 Chargement des données depuis : {latest_file}")
        return latest_file

    def show_basic_stats(self):
        """Affiche les statistiques descriptives."""
        if self.df is None:
            return "Aucune donnée disponible."

        return self.df.describe()

    def calculate_correlation(self):
        """Calcule la corrélation entre le nombre de victoires et les buts marqués."""
        if self.df is None:
            return "Aucune donnée disponible."

        self.df = self.df.astype({"Victoires": float, "Goals For": float, "Win %": float, "Goals Against": float})

        correlation_matrix = {
            "Victoires-GF": np.corrcoef(self.df["Victoires"], self.df["Goals For"])[0, 1],
            "Win%-GA": np.corrcoef(self.df["Win %"], self.df["Goals Against"])[0, 1],
        }

        return correlation_matrix

    def get_best_year(self):
        """Trouver la meilleure année en fonction du pourcentage de victoires."""
        if self.df is None:
            return "Aucune donnée disponible."

        best_year = self.df.loc[self.df["Win %"].astype(float).idxmax()]
        return best_year[["Année", "Win %"]]

    def team_performance_trend(self):
        """Analyse de l'évolution des performances."""
        if self.df is None:
            return "Aucune donnée disponible."

        return self.df.sort_values("Année")[["Année", "Win %"]]

    def best_teams_over_years(self, top_n=5):
        """Trouver les équipes avec le meilleur ratio de victoires."""
        if self.df is None:
            return "Aucune donnée disponible."

        avg_win_rate = self.df.groupby("Nom")["Win %"].mean().sort_values(ascending=False)
        return avg_win_rate.head(top_n)

    def compare_teams_performance(self, team_list):
        """Comparer les performances de plusieurs équipes."""
        if self.df is None:
            return "Aucune donnée disponible."

        return self.df[self.df["Nom"].isin(team_list)][["Nom", "Année", "Win %"]].sort_values(["Nom", "Année"])


















import subprocess
from flask import Flask, render_template, request, jsonify
from scraper import HockeyScraper
from analyzer import HockeyAnalyzer

class HockeyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.scraper = HockeyScraper()
        self.setup_routes()

        # 🔹 Appel du script de scraping
        self.run_scraper()

    def run_scraper(self):
        """Exécute scrape_all_pages.py"""
        print("📡 Lancement du script de scraping...")
        subprocess.run(["python", "scrape_all_teams.py"], check=True)

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/search', methods=['POST'])
        def search():
            team_name = request.form.get('team_name')

            # Scraping des données spécifiques à une équipe
            data = self.scraper.get_team_data(team_name)

            if not data:
                return jsonify({"error": "Aucune donnée trouvée pour cette équipe."}), 404

            # Analyse des données
            analyzer = HockeyAnalyzer(team_name)

            if analyzer.df is None:
                return jsonify({"error": "Données analysables non disponibles."}), 500

            # Récupération des résultats d'analyse
            stats = analyzer.show_basic_stats().to_dict()
            best_year = analyzer.get_best_year().to_dict()
            correlation = analyzer.calculate_correlation()
            trend = analyzer.team_performance_trend().to_dict(orient="records")
            best_teams = analyzer.best_teams_over_years().to_dict()
            comparison = analyzer.compare_teams_performance([team_name]).to_dict(orient="records")

            return jsonify({
                "message": f"Données récupérées et analysées pour {team_name}",
                "data": data,
                "statistiques": stats,
                "meilleure_année": best_year,
                "corrélation": correlation,
                "évolution_performance": trend,
                "meilleures_equipes": best_teams,
                "comparaison_équipes": comparison
            })

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    HockeyApp().run()




document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let teamName = document.getElementById("teamName").value;

    fetch("/search", {
        method: "POST",
        body: new URLSearchParams({ "team_name": teamName }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("result");

        if (data.error) {
            resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
        } else {
            let html = `<h2>Résultats pour ${teamName}</h2>`;
            html += "<h3>Performances :</h3><ul>";

            data.data.forEach(team => {
                html += `<li>${team.Nom} (${team.Année}) - Victoires: ${team.Victoires}, Défaites: ${team.Défaites}</li>`;
            });

            html += "</ul>";

            // Ajout des statistiques
            html += "<h3>📊 Statistiques :</h3><pre>" + JSON.stringify(data.statistiques, null, 2) + "</pre>";

            // Ajout de la meilleure année
            html += "<h3>🏆 Meilleure Année :</h3><pre>" + JSON.stringify(data.meilleure_année, null, 2) + "</pre>";

            // Ajout de la corrélation
            html += "<h3>📈 Corrélation :</h3><pre>" + JSON.stringify(data.corrélation, null, 2) + "</pre>";

            // Ajout de l'évolution des performances
            html += "<h3>🔄 Évolution des Performances :</h3><ul>";
            data.évolution_performance.forEach(entry => {
                html += `<li>Année: ${entry.Année} - Win %: ${entry["Win %"]}</li>`;
            });
            html += "</ul>";

            // Ajout du classement des meilleures équipes
            html += "<h3>🥇 Meilleures Équipes :</h3><pre>" + JSON.stringify(data.meilleures_equipes, null, 2) + "</pre>";

            // Ajout de la comparaison des équipes
            html += "<h3>🔄 Comparaison avec d'autres équipes :</h3><ul>";
            data.comparaison_équipes.forEach(entry => {
                html += `<li>${entry.Nom} - Année: ${entry.Année} - Win %: ${entry["Win %"]}</li>`;
            });
            html += "</ul>";

            resultDiv.innerHTML = html;
        }
    })
    .catch(error => console.error("Erreur:", error));
});














