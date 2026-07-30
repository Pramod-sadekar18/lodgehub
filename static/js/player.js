async function getPlayers() {

    try {

        const response = await fetch(
            "http://127.0.0.1:114/api/players/"
        );

        const players = await response.json();

        let html = "";

        let totalRuns = 0;
        let totalWickets = 0;

        players.forEach(player => {

            totalRuns += player.total_runs;
            totalWickets += player.wickets;

            html += `
                <div class="player-card">

                    <img
                        src="${player.image}"
                        class="player-image"
                    >

                    <div class="player-body">

                        <div class="player-name">
                            ${player.name}
                        </div>

                        <div class="player-team">
                            ${player.team_name}
                        </div>

                        <span class="player-role">
                            ${player.position}
                        </span>

                        <div class="stats-row">

                            <div class="stat">
                                <h3>${player.matches_played}</h3>
                                <p>Matches</p>
                            </div>

                            <div class="stat">
                                <h3>${player.total_runs}</h3>
                                <p>Runs</p>
                            </div>

                            <div class="stat">
                                <h3>${player.wickets}</h3>
                                <p>Wickets</p>
                            </div>

                        </div>

                    </div>

                </div>
            `;
        });

        document.getElementById("playersContainer")
            .innerHTML = html;

        document.getElementById("totalPlayers")
            .innerText = players.length;

        document.getElementById("totalRuns")
            .innerText = totalRuns;

        document.getElementById("totalWickets")
            .innerText = totalWickets;

    }
    catch(error){

        console.log(error);

    }
}

getPlayers();