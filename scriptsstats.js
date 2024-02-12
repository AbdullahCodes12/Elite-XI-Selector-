document.addEventListener('DOMContentLoaded', function() {
    const teams = ["Pakistan", "India", "Australia", "England", "South Africa", 
                   "Bangladesh", "New Zealand", "Srilanka", "Scotland", "Zimbabwe", 
                   "West Indies", "USA", "UAE", "Papa New Guinea", "Afghanistan", 
                   "Canada", "Hong Kong", "Ireland", "Kenya", "Namibia", "Nepal", 
                   "Netherlands", "Oman"];
    
    let statsType;
    let selectedTeam = "";
    let selectedHostOrOpponent = "";
    let isHost = false;
    let battingStatsDiv = document.getElementById('batting-stats');
    let bowlingStatsDiv = document.getElementById('bowling-stats');

    // Function to populate any dropdown
    function populateDropdown(dropdownId, options) {
        let dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = ''; // Clear existing options
    
        options.forEach(optionText => {
            let option = document.createElement('li');
            let link = document.createElement('a');
            link.href = "#";
            link.textContent = optionText;
            link.addEventListener('click', function() {
                dropdown.parentNode.querySelector('.dropdown-toggle').textContent = optionText;
    
                // Update selected values based on dropdown ID
                if (dropdownId === 'teamDropdown') {
                    selectedTeam = optionText;
                } else if (dropdownId === 'hostOrOpponentDropdown') {
                    selectedHostOrOpponent = optionText === 'None' ? '' : optionText;
                    isHost = (optionText.toLowerCase() === 'host');
                    populateDropdown('hostoroppselectionDropdown', teams); // Repopulate the host/opponent selection dropdown
                } else if (dropdownId === 'hostoroppselectionDropdown') {
                    // Handle host or opponent selection
                }
            });
            option.appendChild(link);
            dropdown.appendChild(option);
        });
    }
    // Initial population of dropdowns
    populateDropdown('statsTypeDropdown', ['Batting', 'Bowling']);
    populateDropdown('teamDropdown', teams);
    populateDropdown('hostOrOpponentDropdown', ['Host', 'Opponent']);

    // Function to fetch and display stats
    // Function to fetch and display stats
// Function to fetch and display stats
function fetchAndDisplayStats() {
    let statsType = document.getElementById('statsTypeDropdown').parentNode.querySelector('.dropdown-toggle').textContent.trim();
    let selectedHostOrOpponentTeam = document.getElementById('hostoroppselectionDropdown').parentNode.querySelector('.dropdown-toggle').textContent.trim();

    // Send an empty string or a special value for 'None' selection
    if (selectedHostOrOpponentTeam === 'None') {
        selectedHostOrOpponentTeam = ''; // or 'none'
    }

    let data = {
        choice: statsType.toLowerCase(),
        team: selectedTeam,
        opponent_or_host: selectedHostOrOpponentTeam,
        is_host: isHost
    };

    fetch('/get_player_stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Check if the received data is an array
        if (Array.isArray(data)) {
            // Show and populate the appropriate table based on statsType
            if (statsType === 'batting') {
                battingStatsDiv.style.display = 'block'; // Show batting stats table
                populateStatsTable(data, battingStatsTableBody, 'batting', statSuffix);
            } else if (statsType === 'bowling') {
                bowlingStatsDiv.style.display = 'block'; // Show bowling stats table
                populateStatsTable(data, bowlingStatsTableBody, 'bowling', statSuffix);
            }

            // Parse the data and display stats
            displayPlayerStats(data, statsType.toLowerCase(), selectedHostOrOpponentTeam);
        } else {
            console.error('Error: Received data is not an array', data);
        }
    })
    .catch(error => console.error('Error:', error));
}


        // Function to display player stats
    function displayPlayerStats(data, statsType, selectedHostOrOpponent) {
        // Get references to both tables and their bodies
        let battingStatsTableBody = document.getElementById('stats-table-body'); // Update this line
        let bowlingStatsTableBody = document.getElementById('bowling-stats-table-body');

        let battingStatsDiv = document.getElementById('batting-stats');
        let bowlingStatsDiv = document.getElementById('bowling-stats');
        console.log("Displaying stats for type:", statsType); // Log the stats type being displayed
        // ... existing code ...
    
        // Clear previous results and hide both tables
        clearAndHideStatsTables();
    
        // Determine stat suffix based on user choice
        let statSuffix = '';
            if (selectedHostOrOpponent && selectedHostOrOpponent !== 'None') {
                statSuffix = isHost ? `_in_${selectedHostOrOpponent}` : `_vs_${selectedHostOrOpponent}`;
            }

            // Show and populate the appropriate table based on statsType
            if (statsType === 'batting') {
                battingStatsDiv.style.display = 'block'; // Show batting stats table
                populateStatsTable(data, battingStatsTableBody, 'batting', statSuffix);
            } else if (statsType === 'bowling') {
                bowlingStatsDiv.style.display = 'block'; // Show bowling stats table
                populateStatsTable(data, bowlingStatsTableBody, 'bowling', statSuffix);
            }
        
    }
    function clearAndHideStatsTables() {
        const battingBody = document.getElementById('batting-stats-table-body');
        const bowlingBody = document.getElementById('bowling-stats-table-body');
        if (battingBody) battingBody.innerHTML = '';
        if (bowlingBody) bowlingBody.innerHTML = '';
        document.getElementById('batting-stats').style.display = 'none';
        document.getElementById('bowling-stats').style.display = 'none';
    }
        // Function to populate stats table
        function populateStatsTable(data, tableBody, statsType, statSuffix) {
            console.log(`Populating table for ${statsType} with suffix ${statSuffix}`); // Log the operation
            tableBody.innerHTML = ''; // Clear existing rows
            console.log("Data to populate:", data); // Log the data to be populated
        
            data.forEach(player => {
                let row = tableBody.insertRow();
                row.insertCell().textContent = player.Player;
                row.insertCell().textContent = player.Team;
                row.insertCell().textContent = player.Role;
                row.insertCell().textContent = player.Span;
        
                let stats = statsType === 'batting' ?
                    ['Matches', 'Not Outs', 'Runs', 'HS', 'Batting_Ave', 'Balls Faced', 'SR', 'Centuries', 'Fifties', 'Ducks', 'Fours', 'Sixes'] :
                    ['Overs', 'Mdns', 'Runs_given', 'Wkts', 'Bowling_Ave', 'Econ', 'Bowling_SR', '4W', '5W'];
        
                stats.forEach(stat => {
                    let key = statSuffix ? `${stat}${statSuffix}` : stat;
                    console.log(`Accessing key: ${key} for player`, player); // Log the key being accessed
                    let cellValue = player[key] !== undefined ? player[key] : 'N/A';
                    row.insertCell().textContent = cellValue;
                });
            });
        }

    
        // Show and populate the appropriate table based on statsType

    
        // Event listener for the 'Get Stats' button
        // Add event listener to the 'Get Stats' button
    document.getElementById('getStatsButton').addEventListener('click', function() {
        fetchAndDisplayStats();
    });
// You can call this function to clear the table and hide it before fetching new stats

    
    
    });


