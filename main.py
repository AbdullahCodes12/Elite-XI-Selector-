import joblib
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np



# Function to get combined recommendations
def get_combined_recommendations(user_team, user_opponent, user_host_country, user_status_preference, num_batsmen, num_bowlers, num_all_rounders, ar_primary_role):
    df_batsmen = pd.read_csv('cleaned_batting_stats.csv')
    df_bowling = pd.read_csv('final_bowling_stats_with_performance_category.csv')
    model_directory_batsmen = 'saved_model_no_8'
    model_directory_bowling = 'saved_model_bowling_09'

    if 'Total_Matches' not in df_bowling.columns:
        df_bowling['Total_Matches'] = df_bowling.filter(regex='Matches_').sum(axis=1)

    batsmen_recommendations = predict_top_batsmen(user_team, user_opponent, user_host_country, 'BAT', user_status_preference, df_batsmen, model_directory_batsmen, num_batsmen)
    bowler_recommendations = predict_top_bowlers(user_team, user_opponent, user_host_country, 'BOWL', user_status_preference, df_bowling, model_directory_bowling, num_bowlers)

    if ar_primary_role == 'BATTING':
        ar_recommendations = predict_top_batsmen(user_team, user_opponent, user_host_country, 'AR', user_status_preference, df_batsmen, model_directory_batsmen, num_all_rounders)
    else:
        ar_recommendations = predict_top_bowlers(user_team, user_opponent, user_host_country, 'AR', user_status_preference, df_bowling, model_directory_bowling, num_all_rounders)

    combined_recommendations = pd.concat([batsmen_recommendations, bowler_recommendations, ar_recommendations]).reset_index(drop=True)
    return combined_recommendations.to_dict(orient='records')


# Common Functions
def get_team_name(prompt, team_mapping):
    while True:
        try:
            choice = int(input(prompt))
            return team_mapping[choice]
        except (ValueError, KeyError):
            print("Invalid selection. Please enter a valid number.")

def get_player_status_preference_batsmen():
    while True:
        status_preference = input("Do you want to see all batsmen or only current batsmen (All/Current): ").upper()
        if status_preference in ['ALL', 'CURRENT']:
            return status_preference
        else:
            print("Invalid selection. Please enter All or Current.")

def get_player_status_preference_bowlers():
    while True:
        status_preference = input("Do you want to see all bowlers or only current bowlers (All/Current): ").upper()
        if status_preference in ['ALL', 'CURRENT']:
            return status_preference
        else:
            print("Invalid selection. Please enter All or Current.")
def get_combined_player_status_preference():
    while True:
        status_preference = input("Do you want to see all players or only current players (All/Current): ").upper()
        if status_preference in ['ALL', 'CURRENT']:
            return status_preference
        else:
            print("Invalid selection. Please enter All or Current.")

# Team mapping
team_mapping = {
    1: "Pakistan", 2: "India", 3: "Australia", 4: "England", 5: "South Africa",
    6: "Bangladesh", 7: "New Zealand", 8: "Srilanka", 9: "Scotland",
    10: "Zimbabwe", 11: "West Indies", 12: "USA", 13: "UAE",
    14: "Papua New Guinea", 15: "Afghanistan", 16: "Canada", 17: "Hong Kong",
    18: "Ireland", 19: "Kenya", 20: "Namibia", 21: "Nepal", 22: "Netherlands", 23: "Oman"
}

# Print team options
for number, name in team_mapping.items():
    print(f"{number}: {name}")

# Batsmen specific functions and code
def feature_engineering_batsmen(df, team, opponent, host_country, stats_weights):
    # ... [rest of the feature_engineering_batsmen function] ...
    # This is similar to the 'feature_engineering' function from the batsmen code
    stats = ['Matches', 'Runs', 'HS', 'Batting_Ave', 'SR', 'Centuries', 'Fifties', 'Fours', 'Sixes']
    
    # Filter for the team
    team_df = df[df['Team'] == team]

    # Select columns for overall, vs opponent, and in host country
    overall_cols = [f'Overall_{stat}' for stat in stats]
    vs_opponent_cols = [f'{stat}vs{opponent}' for stat in stats]
    in_host_cols = [f'{stat}in{host_country}' for stat in stats]

    # Include the 'Performance_Category' column
    selected_cols = ['Performance_Category'] + overall_cols + vs_opponent_cols + in_host_cols
    selected_cols = [col for col in selected_cols if col in team_df.columns]

    # Explicitly include the 'Span' column for filtering
    if 'Span' not in selected_cols:
        selected_cols.append('Span')

    feature_df = team_df[['Player', 'Role'] + selected_cols]  # 'Span' is already in selected_cols

    # Calculate the weighted stat score
    weighted_stat_cols = [col for col in feature_df.columns if col.split('_')[0] in stats_weights]
    feature_df['Weighted_Stat_Score'] = feature_df.apply(
        lambda row: sum(row[col] * stats_weights[col.split('_')[0]] for col in weighted_stat_cols),
        axis=1
    )

    # Define numeric columns excluding 'Performance_Category' and 'Span'
    numeric_cols = [col for col in selected_cols if col not in ['Performance_Category', 'Span']]
    numeric_cols.append('Weighted_Stat_Score')  # Add the new feature

    # Normalize features (excluding 'Performance_Category' and 'Span')
    scaler = MinMaxScaler()
    already_normalized_cols = [col for col in numeric_cols if 'Overall_' in col]
    cols_to_normalize = list(set(numeric_cols) - set(already_normalized_cols))

    # Normalize only the necessary columns
    if cols_to_normalize:
        feature_df[cols_to_normalize] = scaler.fit_transform(feature_df[cols_to_normalize])

    return feature_df

def predict_top_batsmen(team, opponent, host_country, role_preference, status_preference, df, model_directory, num_players):
    model_filename = f'{model_directory}/model_{team}_vs_{opponent}_in_{host_country}.sav'
    
    # Fallback to the alternative filename format if the primary one is not found
    if not os.path.exists(model_filename):
        model_filename = f'{model_directory}/model_{team}vs{opponent}in{host_country}.sav'

    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        return f"No model found for {team} vs {opponent} in {host_country}"

    # Load the saved LabelEncoder
    label_encoder_filename = f'{model_directory}/label_encoder.sav'
    try:
        label_encoder = joblib.load(label_encoder_filename)
    except FileNotFoundError:
        return "Label encoder file not found."
    stats_weights = {
        'Runs': 0.22,        # Highest precedence
        'Batting_Ave': 0.18,
        'SR': 0.15,
        'Centuries': 0.13,
        'Fifties': 0.11,
        'HS': 0.09,
        'Fours': 0.07,
        'Sixes': 0.05         # Lowest precedence
    }
    # Update this line to use the correct function name
    feature_df = feature_engineering_batsmen(df, team, opponent, host_country, stats_weights)



    # Apply role preference filtering
    if role_preference != 'NONE':
        feature_df = feature_df[feature_df['Role'] == role_preference]

    if feature_df.empty:
        return "No data available for this combination."
    
    if status_preference == 'CURRENT':
        # Filter based on 'Span' column
        span_series = feature_df['Span'].astype(str)
        feature_df = feature_df[span_series.str.endswith('2023')]

    # Prepare the data for prediction
    players = feature_df['Player']
    # Exclude 'Player', 'Role', 'Performance_Category', and 'Span' from the features
    X = feature_df.drop(['Player', 'Role', 'Performance_Category', 'Span'], axis=1)

    # ... (rest of the code for making predictions)

    # Make predictions
    predictions = model.predict_proba(X)

    # Determine the predicted class indices
    predicted_class_indices = np.argmax(predictions, axis=1)

    # Safely translate indices to class labels
    try:
        predicted_classes = label_encoder.inverse_transform(predicted_class_indices)
    except ValueError:
        # Handle unseen labels here
        predicted_classes = ['Unknown' for _ in predicted_class_indices]

    # Determine the probability for the predicted class
    high_performance_prob = np.max(predictions, axis=1)

    # Create a DataFrame for players, their probabilities, and predicted classes
    player_predictions = pd.DataFrame({
        'Player': players,
        'Probability': high_performance_prob
    })

    # Sort and select top players based on probability
    top_players = player_predictions.sort_values(by='Probability', ascending=False).head(num_players)

    return top_players


# Bowlers specific functions and code
# Bowlers specific functions and code
def feature_engineering_bowling(df, team, opponent, host_country, stats_weights, min_matches_threshold=10):
    # Define the stats list here
    stats = ['Matches', 'Wkts', 'Bowling_Ave', 'Econ', 'Bowling_SR', '5W', '4W', 'Mdns', 'Overs']

    team_df = df[(df['Team'] == team) & (df['Total_Matches'] >= min_matches_threshold)]
    if 'Total_Matches' not in df.columns:
        df['Total_Matches'] = df.filter(regex='Matches_').sum(axis=1)

    overall_cols = [f'Overall_{stat}' for stat in stats]
    vs_opponent_cols = [f'{stat}_vs_{opponent}' for stat in stats]
    in_host_cols = [f'{stat}_in_{host_country}' for stat in stats]

    selected_cols = ['Performance_Category', 'Total_Matches'] + overall_cols + vs_opponent_cols + in_host_cols
    selected_cols = [col for col in selected_cols if col in team_df.columns]

    if 'Span' not in selected_cols:
        selected_cols.append('Span')

    feature_df = team_df[['Player', 'Role'] + selected_cols]
    if len(feature_df) == 0:
        return pd.DataFrame()

    feature_df['Weighted_Stat_Score'] = feature_df.apply(
        lambda row: sum(
            (1 / row[col] if col in ['Bowling_Ave', 'Econ', 'Bowling_SR'] and row[col] != 0 else row[col]) * stats_weights.get(col.split('_')[0], 0) 
            for col in row.index if col.split('_')[0] in stats_weights
        ), 
        axis=1
    )

    numeric_cols = list(set(feature_df.columns) - {'Player', 'Role', 'Performance_Category', 'Span'})
    if numeric_cols:
        scaler = MinMaxScaler()
        feature_df[numeric_cols] = scaler.fit_transform(feature_df[numeric_cols])

    return feature_df

def refine_composite_score(df, stats_weights, experience_weight=0.1):
    # Assuming the function refines the composite score based on weights and experience
   
    df['Refined_Composite_Score'] = df['Weighted_Stat_Score'] + experience_weight * df['Total_Matches']
    return df

def predict_top_bowlers(team, opponent, host_country, role_preference, status_preference, df, model_directory, num_players):
    # ... [rest of the predict_top_bowlers function] ...
    model_filename = f'{model_directory}/model_{team}_vs_{opponent}_in_{host_country}.sav'
    label_encoder_filename = f'{model_directory}/label_encoder.sav'
    
    # Check if the file exists, if not, try the alternate format
    if not os.path.exists(model_filename):
        model_filename = f'{model_directory}/model_{team}vs{opponent}in{host_country}.sav'

    try:
        model = joblib.load(model_filename)
        label_encoder = joblib.load(label_encoder_filename)
    except FileNotFoundError:
        return f"Model or Label Encoder not found for {team} vs {opponent} in {host_country}"

    # Define stats_weights for bowlers here
    stats_weights = {
        'Wkts': 0.22, 'Bowling_Ave': 0.18, 'Econ': 0.15, 'Bowling_SR': 0.13, 
        '5W': 0.11, '4W': 0.09, 'Mdns': 0.07, 'Overs': 0.05
    }

    feature_df = feature_engineering_bowling(df, team, opponent, host_country, stats_weights)
    feature_df = refine_composite_score(feature_df, stats_weights)
    
    if role_preference != 'NONE':
        feature_df = feature_df[feature_df['Role'] == role_preference]
    if feature_df.empty:
        return "No data available for this combination."

    if status_preference == 'CURRENT':
        span_series = feature_df['Span'].astype(str)
        feature_df = feature_df[span_series.str.endswith('2023')]

    players = feature_df['Player']
    # Exclude 'Player', 'Role', 'Performance_Category', and 'Span' from features
    X = feature_df.drop(['Player', 'Role', 'Performance_Category', 'Span'], axis=1)
    predictions = model.predict_proba(X)

    predicted_class_indices = np.argmax(predictions, axis=1)
    predicted_classes = label_encoder.inverse_transform(predicted_class_indices)
    high_performance_prob = np.max(predictions, axis=1)

    player_predictions = pd.DataFrame({'Player': players, 'Probability': high_performance_prob})
    top_players = player_predictions.sort_values(by='Probability', ascending=True).head(num_players)

    return top_players



# Main function
def main():

        df_batsmen = pd.read_csv('cleaned_batting_stats.csv')
        df_bowling = pd.read_csv('final_bowling_stats_with_performance_category.csv')
        model_directory_batsmen = 'saved_model_no_8'
        model_directory_bowling = 'saved_model_bowling_09'

        user_team = get_team_name("Enter the number for your team: ", team_mapping)
        user_opponent = get_team_name("Enter the number for the opponent team: ", team_mapping)
        user_host_country = get_team_name("Enter the number for the host country: ", team_mapping)
        user_status_preference = get_combined_player_status_preference()  # Get combined preference
        num_batsmen = int(input("Enter the number of top batsmen you want to see: "))
        num_bowlers = int(input("Enter the number of top bowlers you want to see: "))
        num_all_rounders = int(input("Enter the number of top all-rounders you want to see: "))
        ar_primary_role = input("Enter primary role for All-Rounders (Batting/Bowling): ").upper()
        
        if 'Total_Matches' not in df_bowling.columns:
            df_bowling['Total_Matches'] = df_bowling.filter(regex='Matches_').sum(axis=1)


        # Get recommendations based on user's choice
        batsmen_recommendations = predict_top_batsmen(user_team, user_opponent, user_host_country, 'BAT', user_status_preference, df_batsmen, model_directory_batsmen, num_batsmen)
        bowler_recommendations = predict_top_bowlers(user_team, user_opponent, user_host_country, 'BOWL', user_status_preference, df_bowling, model_directory_bowling, num_bowlers)
        
        # All-rounder recommendations based on primary role
        if ar_primary_role == 'BATTING':
            ar_recommendations = predict_top_batsmen(user_team, user_opponent, user_host_country, 'AR', user_status_preference, df_batsmen, model_directory_batsmen, num_all_rounders)
        else:
            ar_recommendations = predict_top_bowlers(user_team, user_opponent, user_host_country, 'AR', user_status_preference, df_bowling, model_directory_bowling, num_all_rounders)

        # Combine and display recommendations
        combined_recommendations = pd.concat([batsmen_recommendations, bowler_recommendations, ar_recommendations]).reset_index(drop=True)
        print("\nCombined Team Recommendations:")
        print(combined_recommendations)
        
# Calling the main function
if __name__ == "__main__":
    main()