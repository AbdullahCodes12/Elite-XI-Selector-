from flask import Flask, request, jsonify, render_template
import pandas as pd
import main  # Import main.py
import stats
import traceback

app = Flask(__name__)

df = pd.read_csv("C:/Users/hp/Desktop/fyp2/corrected_processed_odidataset.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_combined_recommendations', methods=['POST'])
def get_combined_recommendations_route():
    try:
        data = request.json
        print("Received data:", data)  # Print the received data
        recommendations = main.get_combined_recommendations(
            user_team=data['user_team'],
            user_opponent=data['user_opponent'],
            user_host_country=data['user_host_country'],
            user_status_preference=data['user_status_preference'],
            num_batsmen=data['num_batsmen'],
            num_bowlers=data['num_bowlers'],
            num_all_rounders=data['num_all_rounders'],
            ar_primary_role=data['ar_primary_role']
        )
        recommendations = main.get_combined_recommendations(**data)
        return jsonify(recommendations)
    except Exception as e:
        print("Error processing request:", e)  # Print the error
        return jsonify({'error': 'Error processing request'}), 500
@app.route('/get_player_stats', methods=['POST'])
def get_player_stats_route():
    try:
        data = request.json
        print("Received data:", data)  # Print the received data

        player_stats = stats.get_player_stats(
            df, 
            data['choice'], 
            data['team'], 
            data['opponent_or_host'], 
            data.get('is_host', False)
        )
        
        print("Player stats:", player_stats)  # Debug print

        json_data = player_stats.to_json(orient='records')
        print(json_data)  # Debug print
        return json_data
    except Exception as e:
        traceback.print_exc()  # Print full traceback
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
