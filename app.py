from flask import Flask, render_template, request, jsonify, send_file
from scraper import HockeyScraper
from analyzer import HockeyAnalyzer
from visualizer import HockeyVisualizer
import os
import subprocess

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

            # 📡 Scraping automatique des données
            data = self.scraper.get_team_data(team_name)
            if not data:
                return jsonify({"error": "Aucune donnée trouvée pour cette équipe."}), 404

            # 📂 Vérification du fichier CSV existant
            csv_file = f"static/hockey_stats_{team_name.replace(' ', '_').lower()}.csv"
            if not os.path.exists(csv_file):
                return jsonify({"error": "Le fichier de données n'a pas été généré."}), 500

            # 📊 Analyse des données
            analyzer = HockeyAnalyzer(team_name)
            if analyzer.df is None:
                return jsonify({"error": "Données analysables non disponibles."}), 500

            stats = analyzer.show_basic_stats().to_dict()
            best_year = analyzer.get_best_year().to_dict()
            correlation = analyzer.calculate_correlation()
            trend = analyzer.team_performance_trend().to_dict(orient="records")
            best_teams = analyzer.best_teams_over_years().to_dict()
            comparison = analyzer.compare_all_teams_performance()

            # 🎨 Génération des graphiques
            visualizer = HockeyVisualizer(team_name)
            wins_plot = visualizer.plot_team_wins_over_years()  # ✅ Sauvegarde
            goals_plot = visualizer.plot_goals_histogram()      # ✅ Sauvegarde

            # Nouveau graphique 1 : Boxplot des victoires par équipe
            wins_boxplot = visualizer.plot_wins_boxplot()

            # Nouveau graphique 2 : Heatmap des performances moyennes par année
            heatmap_plot = visualizer.plot_performance_heatmap()

            # Nouveau graphique 3 : Scatter plot entre buts marqués et pourcentage de victoires
            scatter_plot = visualizer.plot_goals_vs_wins_scatter()  # 🛠️ Méthode corrigée

            # Nouveau graphique 4 : Graphe plot de perfomance
            performance_plot = visualizer.plot_performance_distribution()  # 🛠️ Méthode corrigée


            return jsonify({
                "message": f"Données récupérées et analysées pour {team_name}",
                "data": data,
                "statistiques": stats,
                "meilleure_année": best_year,
                "corrélation": correlation,
                "évolution_performance": trend,
                "meilleures_equipes": best_teams,
                "comparaison_équipes": comparison,
                "csv_file": csv_file,
                "graphs": {
                    "wins_plot": wins_plot,
                    "goals_plot": goals_plot,
                    "wins_boxplot": wins_boxplot,
                    "heatmap_plot": heatmap_plot,
                    "scatter_plot": scatter_plot,
                    "performance_plot": performance_plot
                }
            })

        @self.app.route('/graphs/<filename>')
        def get_graph(filename):
            """Route pour accéder aux graphiques sauvegardés."""
            graph_path = os.path.join('static', 'graphs', filename)
            if os.path.exists(graph_path):
                return send_file(graph_path)
            else:
                return jsonify({"error": "Graphique non trouvé."}), 404

    def run(self):
        """Lance l'application Flask."""
        self.app.run(debug=True)

if __name__ == '__main__':
    HockeyApp().run()
