from flask import Flask, render_template
from nba_api.stats.endpoints import leaguedashteamstats

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch NBA team stats for the current season
    team_stats = leaguedashteamstats.LeagueDashTeamStats().get_data_frames()[0]
    
    # Convert DataFrame to a list of dictionaries to pass to the template
    team_stats = team_stats[['TEAM_NAME', 'W', 'L', 'W_PCT', 'PTS']].to_dict(orient='records')
    
    return render_template('index.html', team_stats=team_stats)

if __name__ == '__main__':
    app.run(debug=True)
