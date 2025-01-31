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

            // Performances sous forme de tableau
            html += `
                <h3>📊 Performances :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Année</th>
                            <th>Victoires</th>
                            <th>Défaites</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            data.data.forEach(team => {
                html += `
                    <tr>
                        <td>${team.Nom}</td>
                        <td>${team.Année}</td>
                        <td>${team.Victoires}</td>
                        <td>${team.Défaites}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;

            // Bouton de téléchargement CSV
            html += `<button id="downloadCSV" style="margin-top: 10px;">📥 Télécharger les Résultats (CSV)</button>`;

            // Statistiques générales
            html += `<h3>📊 Statistiques :</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>Statistique</th>
                        <th>Count</th>
                        <th>Mean</th>
                        <th>Min</th>
                        <th>25%</th>
                        <th>50%</th>
                        <th>75%</th>
                        <th>Max</th>
                        <th>Std</th>
                    </tr>
                </thead>
                <tbody>`;

            Object.entries(data.statistiques).forEach(([stat, values]) => {
                html += `
                    <tr>
                        <td>${stat}</td>
                        <td>${values.count || '-'}</td>
                        <td>${values.mean.toFixed(2)}</td>
                        <td>${values.min}</td>
                        <td>${values["25%"]}</td>
                        <td>${values["50%"]}</td>
                        <td>${values["75%"]}</td>
                        <td>${values.max}</td>
                        <td>${values.std.toFixed(2)}</td>
                    </tr>`;
            });

            html += `</tbody></table>`;


            // Meilleure année sous forme de tableau
            html += `
                <h3>🏆 Meilleure Année :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Année</th>
                            <th>Win %</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>${data.meilleure_année.Année}</td>
                            <td>${data.meilleure_année["Win %"].toFixed(3)}</td>
                        </tr>
                    </tbody>
                </table>
            `;

            // Corrélation sous forme de tableau
            html += `
                <h3>📈 Corrélation :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Relation</th>
                            <th>Valeur</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            Object.entries(data.corrélation).forEach(([relation, valeur]) => {
                html += `
                    <tr>
                        <td>${relation}</td>
                        <td>${valeur.toFixed(3)}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;

            // Évolution des performances sous forme de tableau
            html += `
                <h3>🔄 Évolution des Performances :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Année</th>
                            <th>Win %</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            data.évolution_performance.forEach(entry => {
                html += `
                    <tr>
                        <td>${entry.Année}</td>
                        <td>${entry["Win %"]}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;

            // Meilleures équipes sous forme de tableau
            html += `
                <h3>🥇 Meilleures Équipes :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Équipe</th>
                            <th>Win %</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            Object.entries(data.meilleures_equipes).forEach(([team, winRate]) => {
                html += `
                    <tr>
                        <td>${team}</td>
                        <td>${winRate.toFixed(3)}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;

            // Comparaison avec d'autres équipes sous forme de tableau
            html += `
                <h3>🔄 Comparaison avec d'autres équipes :</h3>
                <table border="1" cellspacing="0" cellpadding="5">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Année</th>
                            <th>Win %</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            data.comparaison_équipes.forEach(entry => {
                html += `
                    <tr>
                        <td>${entry.Nom}</td>
                        <td>${entry.Année}</td>
                        <td>${entry["Win %"]}</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;

            // Graphiques associés
            html += `<h3>📸 Graphiques :</h3>`;
            let imageBaseName = teamName.replace(/ /g, '_').toLowerCase();
            const images = [
                `${imageBaseName}_goals.png`,
                `${imageBaseName}_goals_vs_wins_scatter.png`,
                `${imageBaseName}_performance_distribution.png`,
                `${imageBaseName}_performance_heatmap.png`,
                `${imageBaseName}_wins.png`,
                `${imageBaseName}_wins_boxplot.png`
            ];

            images.forEach(image => {
                html += `<div><img src="graphs/${image}" alt="${image}"></div>`;
            });

            resultDiv.innerHTML = html;

            // Ajouter l'événement au bouton de téléchargement CSV
            document.getElementById("downloadCSV").addEventListener("click", function() {
                downloadCSV(data.data, teamName);
            });
        }
    })
    .catch(error => console.error("Erreur:", error));
});

// Fonction pour générer et télécharger le CSV
function downloadCSV(data, teamName) {
    let csvContent = "data:text/csv;charset=utf-8,Nom,Année,Victoires,Défaites\n";
    data.forEach(team => {
        csvContent += `${team.Nom},${team.Année},${team.Victoires},${team.Défaites}\n`;
    });

    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `hockey_stats_${teamName.replace(/\s+/g, '_').toLowerCase()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
