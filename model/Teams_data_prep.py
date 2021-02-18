import pandas as pd
from config import WEBSCRAPE_DATA_PATH, OUTPUT_DATA_PATH
import os


def get_understat_filepaths(file_path):
    filepaths = []
    team = []
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if ('understat' in filename) and ('team' not in filename) and ('player' not in filename):
                filepaths += [f"{root}/{filename}"]
                team = team + [filename.split('_', 1)[1].split('.')[0].replace("_", " ")]
    return pd.DataFrame({'Filepath': filepaths,
                         }, index=team)


def create_teams_data(filepath):
    understat_year_df_dict = {}
    understat_year_df_with_opps_dict = {}
    for subdir in os.listdir(filepath):

        year = int(subdir[:4])
        understat_dict = {}

        players_path = os.path.join(os.path.normpath(filepath), subdir)
        understat_paths = get_understat_filepaths(os.path.join(players_path, 'understat'))
        print(understat_paths)
        teams_list = pd.DataFrame({'name': understat_paths.index.values})
        teams_list['id'] = teams_list.index + 1

        for team in understat_paths.index:
            understat_dict[team] = pd.read_csv(understat_paths.loc[team, 'Filepath'],
                                               usecols=['date', 'xG', 'xGA', 'xpts'])
            understat_dict[team]['Team'] = team
            understat_dict[team]['date'] = pd.to_datetime(understat_dict[team].date).dt.date
            understat_dict[team].sort_values(['date'], ascending=True, inplace=True)
            understat_dict[team]['Games_played'] = understat_dict[team].index + 1
        understat_year_df_dict[year] = pd.concat(understat_dict.values())
        understat_year_df_dict[year]['season'] = year
        understat_year_with_id = understat_year_df_dict[year].merge(teams_list,
                                                                    left_on='Team',
                                                                    right_on='name').drop('name', axis=1)
        understat_opponents_filtered = understat_year_with_id[['xG', 'xGA', 'xpts', 'Team', 'id']]
        understat_year_df_with_opps_dict[year] = understat_year_with_id.\
            merge(understat_opponents_filtered, left_on=['xG', 'xGA'], right_on=['xGA', 'xG'],
                  suffixes=('', '_opponent'), how='outer').drop(['xG_opponent', 'xGA_opponent'], axis=1)

    return understat_year_df_with_opps_dict


def main():
    teams_data_dict = create_teams_data(filepath=WEBSCRAPE_DATA_PATH)
    teams_data_with_understat = pd.concat(teams_data_dict.values())
    teams_data_with_understat.to_csv(os.path.join(OUTPUT_DATA_PATH, 'teams_data.csv'), index=False)


if __name__ == "__main__":
    main()
