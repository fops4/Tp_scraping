"# Tp_scraping" 
Projet Final PYTHON : Analyse des Performances des Équipes de Projet Final PYTHON : Analyse des Performances des Équipes de
 Hockey [B3 soir] 

 Synopsis 
    Dans ce projet, nous allons créer une application web interactive application web interactive permettant de récupérer et d’analyser des données historiques sur les performances des équipes de
    hockey. Nous utiliserons le web scraping le web scraping pour extraire les informations depuis le site Scrape This Site, et exploiterons des bibliothèques Python telles que NumPy, NumPy,
    Pandas, Matplotlib et Seaborn Pandas, Matplotlib et Seaborn pour analyser et visualiser ces données. L'application sera construite avec Flask ou FastAPI Flask ou FastAPI pour permettre une interaction simple via
    une interface web.

 Objectifs pédagogiques Objectifs pédagogiques
    1. Comprendre et mettre en œuvre le web scraping Comprendre et mettre en œuvre le web scraping pour extraire des données dynamiques d'un site web.
    2. Utiliser Pandas et NumPy Utiliser Pandas et NumPy pour manipuler et analyser des données tabulaires.
    3. Appliquer des concepts statistiques Appliquer des concepts statistiques comme la corrélation, la moyenne, l’écart-type et la distribution des données.
    4. Créer des visualisations pertinentes Créer des visualisations pertinentes avec Matplotlib et Seaborn.
    5. Développer une interface web légère Développer une interface web légère permettant aux utilisateurs de rechercher des données spécifiques et d'afficher les résultats sous forme graphique.

 Étapes du projet Étapes du projet
    1. Création de l’interface utilisateur 1. Création de l’interface utilisateur
    Développer une petite page web avec un champ de saisie pour entrer le nom d’une équipe nom d’une équipe.
    Ajouter un bouton pour déclencher la recherche et afficher les résultats.

    2. Extraction des données via Web Scraping 2. Extraction des données via Web Scraping
    Utiliser la bibliothèque BeautifulSoup et requests pour extraire les informations du site.
    Construire une URL dynamique pour rechercher une équipe spécifique : https://www.scrapethissite.com/pages/forms/?q={nom_equipe}.
    Extraire les informations suivantes :
    Nom de l'équipe Nom de l'équipe
    Année Année
    Victoires Victoires
    Défaites Défaites
    OT Losses OT Losses
    Win % Win %
    Goals For (GF) Goals For (GF)
    Goals Against (GA) Goals Against (GA)
    Sauvegarder les données scrappées dans un fichier CSV unique avec un nom spécifique.

    3. Analyse et exploration des données avec Pandas et NumPy 3. Analyse et exploration des données avec Pandas et NumPy
        Charger le fichier CSV et effectuer des calculs statistiques calculs statistiques sur les performances des équipes.
        Calculer les statistiques descriptives statistiques descriptives : moyenne, médiane, mode, écart-type.
        Calculer la corrélation corrélation entre différentes variables, notamment :
            Corrélation entre le nombre de victoires et le nombre de buts marqués.
            Corrélation entre le pourcentage de victoires et les buts encaissés.
        Utiliser la formule de corrélation de Pearson formule de corrélation de Pearson 
    Répondre à quelques questions analytiques questions analytiques, par exemple :

        1. Quelle est la meilleure année de performance d’une équipe donnée en fonction du pourcentage de victoires ?
        2. Quelle est l’évolution des performances d’une équipe sur plusieurs années ?
        3. Y a-t-il une corrélation entre le nombre de victoires et le nombre de buts marqués (GF) ?
        4. Quelles équipes ont le meilleur ratio de victoires sur plusieurs années ?
        5. Comparaison des performances entre plusieurs équipes sur une période donnée.

    4. Visualisation des données avec Matplotlib et Seaborn 4. Visualisation des données avec Matplotlib et Seaborn
    Créer 2 à 3 graphiques simples 2 à 3 graphiques simples avec Matplotlib :
        Évolution des victoires d’une équipe sur plusieurs années (courbe).
        Comparaison du nombre de buts marqués par année (histogramme).
    Générer 2 à 3 visualisations avancées 2 à 3 visualisations avancées avec Seaborn :
        Boxplot des victoires par équipe.
        Heatmap des performances moyennes par année.
        Scatter plot entre le nombre de buts marqués et le pourcentage de victoires.
        Graphique de distribution des performances des équipes pour une année donnée.
        
    5. Intégration des résultats sur l’interface web 5. Intégration des résultats sur l’interface web
        Afficher les résultats de l’analyse sur la page web après la recherche.
        Générer dynamiquement les visualisations et permettre le téléchargement des résultats en CSV.
        Explication des champs du dataset : Équipes de Hockey Explication des champs du dataset : Équipes de Hockey

Voici la description détaillée de chaque colonne du dataset que vous allez utiliser dans le projet :

    1. Team Name (Nom de l'équipe) :
        Team Name (Nom de l'équipe) :
        Désigne le nom officiel
        nom officiel de l’équipe de hockey.
        Chaque ligne du dataset correspond à une saison jouée par cette équipe.

    2. Year (Année) :
        Year (Année) :
        Indique l’année
        année de la saison concernée.
        Permet de suivre l’évolution des performances d’une équipe au fil du temps.

    3. Wins (Victoires) :
        Wins (Victoires) :
        Nombre total de matchs gagnés
        matchs gagnés par l’équipe au cours de la saison.
        Indicateur clé de la performance de l’équipe.

    4. Losses (Défaites) :
        Losses (Défaites) :
        Nombre total de matchs perdus
        matchs perdus par l’équipe.
        Un nombre élevé de défaites peut refléter une mauvaise saison.

    5. OT Losses (Défaites en prolongation) :
            Nombre de défaites concédées en prolongation
            défaites concédées en prolongation.
            Différent des défaites classiques, car l’équipe a réussi à pousser le match en prolongation avant de perdre.
            Dans certains championnats, ces défaites rapportent 1 point au classement
    6. Win % (Pourcentage de victoires) :
        Win % (Pourcentage de victoires) :
        Représente le ratio de victoires
        1 point au classement.
        ratio de victoires par rapport au nombre total de matchs joués.
        Une valeur proche de 1 (ou 100 %) indique une excellente saison

    7. Goals For (GF) - Buts marqués :
        Goals For (GF) - Buts marqués :
        Nombre total de buts marqués
        buts marqués par l’équipe durant la saison.
        Mesure la capacité offensive
        capacité offensive de l’équipe.

    8. Goals Against (GA) - Buts encaissés :
        Goals Against (GA) - Buts encaissés :
        Nombre total de buts concédés
        buts concédés par l’équipe.
        Mesure la solidité défensive
        solidité défensive : une équipe ayant encaissé peu de buts a généralement une bonne défense.


 Indicateurs d’analyse possibles avec ces données :
    Différence de buts (Goal Difference) : Un score positif indique une attaque efficace et une bonne défense.
    Ratio Victoires/Défaites :
    Ratio Victoires/Défaites : Permet de comparer la performance des équipes sans prendre en compte les prolongations.
    Corrélation entre les victoires et les buts marqués : Permet de voir si les équipes qui marquent le plus de buts sont aussi celles qui gagnent le plus de matchs.

 Technologies utilisées
    Web Scraping : 
        BeautifulSoup , 
        requests
    Manipulation des données : 
        Pandas , 
        NumPy
    Analyse statistique : Calculs de corrélation, distribution des données, écart-type
    Visualisation des données : 
        Matplotlib , Seaborn
    Développement web : 
        Flask ou
        FastAPI pour le back-end, 
        HTML/CSS pour l’interface
 
    Livrables attendus
    1. Code source Python complet
    2. Page web fonctionnelle permettant de rechercher des équipes et d’afficher les analyses
    3. Fichier CSV généré automatiquement après chaque recherche
    4. Rapport PDF contenant des captures d’écran des visualisations et une synthèse des analyses
    5. Documentation succincte expliquant le fonctionnement du projet
    6. Videos Demo

    **Delai : Jusqu'aaaaaa la derniere seances de cour!!!.