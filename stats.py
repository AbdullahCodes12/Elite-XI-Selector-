import pandas as pd

# Load the dataset
df = pd.read_csv("C:/Users/hp/Desktop/fyp2/corrected_processed_odidataset.csv")

# Function to get player statistics
# Function to get player statistics
# Function to get player statistics
# Function to get player statistics
import numpy as np

# Function to get player statistics
def get_player_stats(df, choice, team, opponent_or_host, is_host=False):
    # Filter for the selected team
    team_df = df[df['Team'] == team]

    # Determine the columns to display based on user choice
    if choice == 'batting':
        base_stats_cols = ['Matches', 'Not Outs', 'Runs', 'HS', 'Batting_Ave', 'Balls Faced', 'SR', 'Centuries', 'Fifties', 'Ducks', 'Fours', 'Sixes']
    else:  # choice == 'bowling'
        base_stats_cols = ['Overs', 'Mdns', 'Runs_given', 'Wkts', 'Bowling_Ave', 'Econ', 'Bowling_SR', '4W', '5W']

    # Adjust column names based on opponent or host
    suffix = ''
    if opponent_or_host and opponent_or_host.lower() not in ['select host/opponent', 'none']:
        suffix = f"_vs_{opponent_or_host}" if not is_host else f"_in_{opponent_or_host}"

    # Select columns to display
    display_cols = ['Player', 'Team', 'Role', 'Span'] + [f"{col}{suffix}" for col in base_stats_cols]

    # Convert 'N/A' strings to actual NaN values
    team_df.replace('N/A', np.nan, inplace=True)

    # Convert numeric columns to numeric types
    numeric_cols = [col for col in display_cols if col not in ['Player', 'Team', 'Role', 'Span']]
    team_df[numeric_cols] = team_df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    return team_df[display_cols]






# Main function
# ...

def main():
    # User input for choice
    choice = input("Do you want to view batting or bowling stats? Enter 'batting' or 'bowling': ").lower()
    while choice not in ['batting', 'bowling']:
        choice = input("Invalid input. Enter 'batting' or 'bowling': ").lower()

    # User input for team
    team = input("Enter the team name: ").title()
    while team not in ["Pakistan", "India", "Australia", "England", "South Africa", "Bangladesh", "New Zealand", "Srilanka", "Scotland", "Zimbabwe", "West Indies", "USA", "UAE", "Papa New Guinea", "Afghanistan", "Canada", "Hong Kong", "Ireland", "Kenya", "Namibia", "Nepal", "Netherlands", "Oman"]:
        team = input("Invalid team name. Please enter again: ").title()

    # User input for opponent or host
    opponent_or_host_choice = input("Do you want to filter by opponent or host country? Enter 'opponent', 'host', or 'none': ").lower()
    opponent_or_host = None
    is_host = False

    if opponent_or_host_choice == 'opponent':
        opponent_or_host = input("Enter the opponent team name: ").title()
    elif opponent_or_host_choice == 'host':
        opponent_or_host = input("Enter the host country name: ").title()
        is_host = True

    # Retrieve player statistics based on user input
    player_stats = get_player_stats(df, choice, team, opponent_or_host, is_host)

    # Display the results
    if not player_stats.empty:
        print(player_stats)
    else:
        print("No data available for the given combination.")

if __name__ == "__main__":
    main()
