document.addEventListener('DOMContentLoaded', function() {
    // Variables to hold the user's selections
    let selectedUserTeamTeam = "";
    let selectedOpponentTeam = "";
    let selectedHostCountryTeam = "";
    let selectedPlayerSpanTeam = "";
    let selectedArPrimaryRole = "";

    // Populate dropdowns
    const teams = ["Pakistan", "India", "Australia", "England", "South Africa", 
                   "Bangladesh", "New Zealand", "Srilanka", "Scotland", "Zimbabwe", 
                   "West Indies", "USA", "UAE", "Papa New Guinea", "Afghanistan", 
                   "Canada", "Hong Kong", "Ireland", "Kenya", "Namibia", "Nepal", 
                   "Netherlands", "Oman"];

    function populateTeamDropdowns(dropdownId) {
        let dropdown = document.getElementById(dropdownId);
        teams.forEach(team => {
            let option = document.createElement('li');
            option.textContent = team;
            option.addEventListener('click', function() {
                document.getElementById(dropdownId).parentNode.childNodes[1].textContent = team; // Update button text
                updateSelectedValue(dropdownId, team);
            });
            dropdown.appendChild(option);
        });
    }
    
    function populateRoleAndSpanDropdowns(dropdownId, options) {
        let dropdown = document.getElementById(dropdownId);
        options.forEach(optionValue => {
            let option = document.createElement('li');
            option.className = 'dropdown-item';
            option.href = "#";
            option.textContent = optionValue;
            option.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent default anchor behavior
                let button = dropdown.parentNode.querySelector('.dropdown-toggle');
                button.textContent = optionValue;
                updateSelectedValue(dropdownId, optionValue);
            });
            dropdown.appendChild(option);
        });
    }

    function updateSelectedValue(dropdownId, selectedValue) {
        if (dropdownId.includes('Team')) {
            if (dropdownId.includes('userTeam')) selectedUserTeamTeam = selectedValue;
            else if (dropdownId.includes('opponent')) selectedOpponentTeam = selectedValue;
            else if (dropdownId.includes('host')) selectedHostCountryTeam = selectedValue;
            else if (dropdownId.includes('span')) selectedPlayerSpanTeam = selectedValue.toUpperCase(); // Convert to uppercase
            else if (dropdownId.includes('arPrimaryRole')) selectedArPrimaryRole = selectedValue.toUpperCase();
            console.log('Updated Selection:', dropdownId, selectedValue);
        }
    }
    

    // Populate dropdowns for team recommendations
    populateTeamDropdowns("userTeamDropdownTeam");
    populateTeamDropdowns("opponentDropdownTeam");
    populateTeamDropdowns("hostDropdownTeam");
    populateRoleAndSpanDropdowns("spanDropdownTeam", ["All", "Current"]);
    populateRoleAndSpanDropdowns("arPrimaryRoleDropdown", ["Batting", "Bowling"]);
    // Function to fetch recommendations
function fetchRecommendations(endpoint, data, recommendationDivId) {
    console.log("Fetching recommendations with data:", data);

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received data:", data);
        displayRecommendations(data, recommendationDivId);
    })
    .catch(error => console.error('Error:', error));
}

// Display recommendations
function displayRecommendations(data, recommendationDivId) {
    let recommendationsDiv = document.getElementById(recommendationDivId);
    recommendationsDiv.innerHTML = '';
    data.forEach(player => {
        let playerDiv = document.createElement('div');
        playerDiv.textContent = `${player.Player} - Probability: ${player.Probability.toFixed(2)}`;
        recommendationsDiv.appendChild(playerDiv);
    });
}

// Event listener for the 'Get Recommendation' button
document.getElementById('getTeamRecommendation').addEventListener('click', function() {

    console.log("Selected values:", selectedUserTeamTeam, selectedOpponentTeam, selectedHostCountryTeam, selectedPlayerSpanTeam, selectedArPrimaryRole);
    let numBatsmen = parseInt(document.getElementById('numBatsmenTeam').value);
    let numBowlers = parseInt(document.getElementById('numBowlersTeam').value);
    let numAllRounders = parseInt(document.getElementById('numAllRoundersTeam').value);

    let data = {
        user_team: selectedUserTeamTeam,
        user_opponent: selectedOpponentTeam,
        user_host_country: selectedHostCountryTeam,
        user_status_preference: selectedPlayerSpanTeam,
        ar_primary_role: selectedArPrimaryRole,
        num_batsmen: numBatsmen,
        num_bowlers: numBowlers,
        num_all_rounders: numAllRounders
    };

    console.log("Sending data for team recommendations:", data);
    fetchRecommendations('/get_combined_recommendations', data, 'team-recommendations');
});
});
