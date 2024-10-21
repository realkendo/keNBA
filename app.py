# import logging
# from flask import Flask, render_template
# from nba_api.stats.endpoints import leaguedashteamstats
# from nba_api.stats.library.parameters import SeasonAll
# import pandas as pd
# import time

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s %(message)s')

# # Function to fetch NBA team stats with retry mechanism
# def fetch_nba_team_stats(retries=3, delay=2):
#     """Fetch NBA team stats with retry logic and error handling."""
#     for attempt in range(retries):
#         try:
#             # Fetch NBA team stats for the current season
#             team_stats = leaguedashteamstats.LeagueDashTeamStats(season=SeasonAll.default).get_data_frames()[0]
#             logging.info(f"Data fetched successfully on attempt {attempt + 1}")
            
#             # Check if the DataFrame is empty
#             if team_stats.empty:
#                 logging.warning("Fetched data is empty")
#                 return None
            
#             # Return the team stats DataFrame
#             return team_stats
        
#         except Exception as e:
#             logging.error(f"Error fetching data: {e}")
#             logging.debug(f"Retrying... ({attempt + 1}/{retries})")
#             time.sleep(delay)  # Wait before retrying
    
#     logging.critical("Failed to fetch data after multiple attempts")
#     return None

# @app.route('/')
# def index():
#     try:
#         # Attempt to fetch the NBA team stats
#         team_stats = fetch_nba_team_stats()

#         # If no data is returned, show a message
#         if team_stats is None:
#             logging.error("No data available after retries")
#             return "Error: No data available at the moment. Please try again later."

#         # Convert DataFrame to a list of dictionaries for template
#         team_stats = team_stats[['TEAM_NAME', 'W', 'L', 'W_PCT', 'PTS']].to_dict(orient='records')
        
#         # Render the HTML template with team stats
#         return render_template('index.html', team_stats=team_stats)
    
#     except pd.errors.EmptyDataError:
#         logging.exception("Pandas encountered an EmptyDataError")
#         return "Error: No data available."
    
#     except Exception as e:
#         logging.exception(f"Unexpected error: {e}")
#         return "Error: Something went wrong while fetching NBA data."

# if __name__ == '__main__':
#     # Running the Flask app in debug mode
#     app.run(debug=True)


import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Replace with your actual API key from The SportsDB
API_KEY = 'your_api_key_here'
BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}/"

# Main route to the home page
@app.route('/')
def home():
    return render_template('index.html')  # Create this HTML file for your main page

# New route to fetch NBA team data
@app.route('/nba-teams')
def nba_teams():
    try:
        response = requests.get(f"{BASE_URL}search_all_teams.php?l=NBA")
        data = response.json()

        # Check if 'teams' key exists in the response
        if 'teams' in data and data['teams']:
            teams = data['teams']
            return render_template('nba_teams.html', teams=teams)  # Render the NBA teams page
        else:
            return "No NBA teams data available."

    except Exception as e:
        return f"Error fetching NBA team data: {e}"

if __name__ == '__main__':
    app.run(debug=True)
