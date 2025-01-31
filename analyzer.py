import pandas as pd
import numpy as np
import glob
import os
import random

class HockeyAnalyzer:
    def __init__(self, team_name):
        self.team_name = team_name
        self.file_path = self.get_latest_file()
        if self.file_path:
            self.df = pd.read_csv(self.file_path)
            self.dataset_df = pd.read_csv("dataset.csv")  # Charger le dataset complet pour la comparaison
        else:
            self.df = None
            print(f"Aucun fichier trouvé pour l'équipe {team_name}.")

    def get_latest_file(self):
        """Récupère le dernier fichier CSV disponible pour l'équipe spécifiée."""
        base_filename = f"static/hockey_stats_{self.team_name.replace(' ', '_').lower()}*"
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

    def best_teams_over_years(self):
        """Retourne les meilleures équipes sur plusieurs années en fonction de leur ratio de victoires."""
        if self.dataset_df is None:
            return "Aucune donnée disponible."

        # Calculer la moyenne des pourcentages de victoires par équipe
        avg_win_rate = self.dataset_df.groupby("Nom")["Win %"].mean().sort_values(ascending=False)

        # Retourner les 5 meilleures équipes
        return avg_win_rate.head(5)

    def get_teams_from_dataset(self):
        """Récupère la liste des équipes disponibles dans le dataset."""
        if self.dataset_df is None:
            return []

        teams = self.dataset_df["Nom"].unique()  # Liste des équipes sans doublons
        return teams

    def get_random_teams(self, num_teams=3):
        """Sélectionne un nombre donné d'équipes au hasard dans le dataset (en plus de l'équipe saisie)."""
        available_teams = self.get_teams_from_dataset()

        # Exclure l'équipe saisie
        available_teams = [team for team in available_teams if team != self.team_name]

        # Choisir des équipes au hasard parmi celles disponibles
        random_teams = random.sample(available_teams, min(num_teams, len(available_teams)))

        return random_teams

    def compare_all_teams_performance(self):
        """Compare les performances de toutes les équipes pour une année aléatoire entre 1990 et 2011."""
        if self.dataset_df is None:
            return "Aucune donnée disponible."

        # Choisir une année aléatoire entre 1990 et 2011
        random_year = random.randint(1990, 2011)
        print(f"Année choisie pour la comparaison : {random_year}")

        # Filtrer les données pour l'année sélectionnée
        filtered_df = self.dataset_df[self.dataset_df["Année"] == random_year]

        # Vérifier qu'on a bien des données pour cette année
        if filtered_df.empty:
            return f"Aucune donnée trouvée pour l'année {random_year}."

        print("DataFrame après filtrage des équipes pour l'année choisie :")
        print(filtered_df.head())

        # Trier les équipes par leur pourcentage de victoires
        performance = filtered_df[["Nom", "Win %", "Année"]].sort_values("Win %", ascending=False)

        # Convertir en liste de dictionnaires pour affichage
        performance_dict = performance.to_dict(orient="records")

        # Afficher les performances de toutes les équipes
        print("Performances des équipes comparées :")
        for team_performance in performance_dict:
            print(f"{team_performance['Nom']} - Année: {team_performance['Année']} - Win %: {team_performance['Win %']}")

        return performance_dict











