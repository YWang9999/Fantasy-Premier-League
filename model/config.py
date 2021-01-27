
from google.oauth2 import service_account
import os
import pandas_gbq


WEBSCRAPE_DATA_PATH = os.path.abspath(os.path.join(os.getcwd(), 'data')) 

FEATURE_COLUMNS = ['assists', 'bonus', 'bps', 'clean_sheets', 'creativity', 'element',
                   'fixture', 'goals_conceded', 'goals_scored', 'ict_index', 'influence',
                   'kickoff_time', 'minutes', 'opponent_team', 'own_goals',
                   'penalties_missed', 'penalties_saved', 'red_cards', 'round', 'saves',
                   'selected', 'team_a_score', 'team_h_score', 'threat', 'total_points',
                   'transfers_balance', 'transfers_in', 'transfers_out', 'value',
                   'was_home', 'yellow_cards']

INGESTED_DATA = "gw_raw"
FEATURE_DATA = "features_df"
PREDICTIONS = "predictions"


credentials = service_account.Credentials.from_service_account_file(
    os.environ.get("PATH_TO_JSON_KEY"),
)
# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = credentials

PROJECT_ID = os.environ.get("PROJECT_ID")
pandas_gbq.context.project = PROJECT_ID

PARAMS = {'n_estimators': 500,
          'max_depth': 4,
          'min_samples_split': 5,
          'learning_rate': 0.01,
          'loss': 'ls'}
          
PAST_WEEKS_NUM = [1, 3, 6, 12]
TARGET_TYPE = "AVG"
TARGET_WEEKS_INTO_FUTURE = 6
TIME_RELATED_FEATURES = ['assists', 'bonus', 'bps', 'clean_sheets', 'creativity',
                         'goals_conceded', 'goals_scored', 'ict_index', 'influence',
                         'minutes', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'saves',
                         'selected', 'threat', 'total_points',
                         'transfers_balance', 'transfers_in', 'transfers_out', 'value',
                         'yellow_cards', 'team_goals_scored', 'team_points', 'xpts',
                         'xG', 'xGA']
