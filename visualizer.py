import matplotlib
matplotlib.use('Agg')  # Utilisation d'un backend non interactif

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Importation de seaborn
import os
import random

class HockeyVisualizer:
    def __init__(self, team_name):
        """Initialisation avec le fichier CSV spécifique à une équipe."""
        self.team_name = team_name
        self.file_path = f"static/hockey_stats_{team_name.replace(' ', '_').lower()}.csv"
        self.dataset_df = self.load_data()
        self.graphs_dir = "static/graphs/"
        os.makedirs(self.graphs_dir, exist_ok=True)  # Création du dossier pour les images

    def load_data(self):
        """Charge le dataset depuis un fichier CSV."""
        if not os.path.exists(self.file_path):
            print(f"❌ Fichier introuvable : {self.file_path}")
            return None
        return pd.read_csv(self.file_path)

    def save_plot(self, fig, filename):
        """Sauvegarde un graphique."""
        filepath = os.path.join(self.graphs_dir, filename)
        fig.savefig(filepath)
        plt.close(fig)  # Fermer la figure pour éviter les conflits
        return filepath

    def plot_team_wins_over_years(self):
        """Trace et sauvegarde l'évolution des victoires d'une équipe sur plusieurs années."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        self.dataset_df = self.dataset_df.sort_values("Année")

        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(self.dataset_df["Année"], self.dataset_df["Victoires"], marker='o', linestyle='-', label=self.team_name)
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de Victoires")
        ax.set_title(f"📊 Évolution des Victoires de {self.team_name}")
        ax.legend()
        ax.grid()

        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_wins.png")

    def plot_goals_histogram(self):
        """Trace et sauvegarde un histogramme du nombre de buts marqués par année."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        # Regroupement des données par année et calcul du total des buts marqués
        goals_by_year = self.dataset_df.groupby("Année")["Goals For"].sum()

        # Tracer l'histogramme avec les années sur l'axe des abscisses
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.bar(goals_by_year.index, goals_by_year.values, color='skyblue', edgecolor='black')

        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de buts marqués")
        ax.set_title(f"📊 Histogramme des buts marqués par {self.team_name} par année")
        ax.grid(axis='y', alpha=0.75)

        # Sauvegarder le graphique
        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_goals.png")

    def plot_wins_boxplot(self):
        """Boxplot des victoires par équipe."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        fig, ax = plt.subplots(figsize=(15, 5))
        sns.boxplot(x='Année', y='Victoires', data=self.dataset_df, palette="Set2", ax=ax)
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de Victoires")
        ax.set_title(f"📊 Boxplot des Victoires de {self.team_name} par Année")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.grid(axis='y', alpha=0.75)

        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_wins_boxplot.png")

    def plot_performance_heatmap(self):
        """Heatmap des performances moyennes par année."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        # Calcul des performances moyennes par année
        performance_matrix = self.dataset_df.groupby("Année")[["Victoires", "Goals For"]].mean()

        fig, ax = plt.subplots(figsize=(15, 5))
        sns.heatmap(performance_matrix.T, annot=True, cmap="YlGnBu", cbar=True, fmt=".1f", ax=ax)
        ax.set_title(f"📊 Heatmap des Performances Moyennes de {self.team_name} par Année")

        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_performance_heatmap.png")

    def plot_goals_vs_wins_scatter(self):
        """Scatter plot entre le nombre de buts marqués et le pourcentage de victoires."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        # Calcul du nombre total de matchs
        self.dataset_df['Total Matches'] = self.dataset_df['Victoires'] + self.dataset_df['Défaites'] + self.dataset_df['OT Losses']
        
        # Calcul du pourcentage de victoires
        self.dataset_df['Pourcentage de Victoires'] = (self.dataset_df["Victoires"] / self.dataset_df["Total Matches"]) * 100

        fig, ax = plt.subplots(figsize=(15, 5))
        sns.scatterplot(x='Goals For', y='Pourcentage de Victoires', data=self.dataset_df, color='blue', ax=ax)
        ax.set_xlabel("Nombre de Buts Marqués")
        ax.set_ylabel("Pourcentage de Victoires")
        ax.set_title(f"📊 Scatter Plot entre Buts Marqués et Pourcentage de Victoires de {self.team_name}")
        ax.grid(True)

        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_goals_vs_wins_scatter.png")


    def plot_performance_distribution(self):
        """Distribution des performances pour une année donnée."""
        if self.dataset_df is None or self.dataset_df.empty:
            print(f"⚠️ Aucune donnée disponible pour {self.team_name}.")
            return None

        year = random.randint(1990, 2011)

        # Filtrer les données pour l'année spécifiée
        data_for_year = self.dataset_df[self.dataset_df["Année"] == year]

        fig, ax = plt.subplots(figsize=(15, 5))
        sns.histplot(data_for_year['Victoires'], kde=True, color='purple', ax=ax)
        ax.set_xlabel("Nombre de Victoires")
        ax.set_ylabel("Fréquence")
        ax.set_title(f"📊 Distribution des Performances de {self.team_name} en {year}")
        ax.grid(True)

        return self.save_plot(fig, f"{self.team_name.replace(' ', '_').lower()}_performance_distribution.png")
