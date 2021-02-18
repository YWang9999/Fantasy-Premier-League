import pandas as pd
from config import WEBSCRAPE_DATA_PATH, FEATURE_COLUMNS, OUTPUT_DATA_PATH, INGESTED_DATA
import os


def gameweek_filepaths(players_path):
    filepaths = []
    for root, dirs, files in os.walk(players_path):
        for filename in files:
            if filename == "gw.csv":
                filepaths += [f"{root}/{filename}"]
    return filepaths


def clean_player_name(year, path):
    if year < 2018:
        return os.path.split(os.path.dirname(path))[1]
    else:
        return os.path.split(os.path.dirname(path))[1].rsplit('_', 1)[0]


def create_features_df(players_path, year):
    player_features_dict_df = {}
    # ssn = f'{year}/{(year + 1) % 100}'
    # print(ssn)
    for path in gameweek_filepaths(players_path):
        if not os.path.exists(path):
            raise FileNotFoundError(path.rsplit('/', 2)[1] + " doesn't have any data in their gw.csv file")
        else:
            player_name = clean_player_name(year=year,
                                            path=path)

            player_features_dict_df[player_name] = pd.read_csv(path, encoding='utf-8')[FEATURE_COLUMNS]
            player_features_dict_df[player_name].sort_values(['kickoff_time'], ascending=True, inplace=True)
            player_features_dict_df[player_name]['Games_played'] = player_features_dict_df[player_name].index + 1
            player_features_dict_df[player_name]['kickoff_time'] = pd.to_datetime(player_features_dict_df[player_name]
                                                                                  ['kickoff_time']).dt.date
            player_features_dict_df[player_name]['player'] = player_name
            player_features_dict_df[player_name]['season'] = year

    return pd.concat(player_features_dict_df.values())


def create_position_df_for_year(players_path) -> pd.DataFrame:
    position_year_df = pd.read_csv(os.path.join(players_path, 'players_raw.csv'),
                                   usecols=['first_name', 'second_name',
                                            'id', 'element_type', 'team', 'team_code'],
                                   encoding='utf-8')

    position_year_df['player'] = position_year_df['first_name'] + "_" + position_year_df['second_name']
    return position_year_df[['player', 'element_type', 'team', 'team_code']]


def create_gw_raw_df_dict(filepath):
    gw_raw_year_df_dict = {}
    position_year_df_dict = {}
    features_year_df_dict = {}
    fixture_year_df_dict = {}
    for subdir in os.listdir(filepath):
        year = int(subdir[:4])
        players_path = os.path.join(os.path.normpath(filepath), subdir)

        position_year_df_dict[year] = create_position_df_for_year(players_path)
        print(f'position_year_df is shape {position_year_df_dict[year].shape} for {year}')

        features_year_df_dict[year] = create_features_df(players_path=players_path,
                                                         year=year)

        print(f'features_year_df_dict shape is {features_year_df_dict[year].shape} for {year}')
        gw_raw_year_df_dict[year] = pd.merge(position_year_df_dict[year], features_year_df_dict[year],
                                             on='player')

        fixture_year_df_dict[year] = (gw_raw_year_df_dict[year][['team', 'Games_played', 'opponent_team', 'season']])\
            .drop_duplicates(subset=['Games_played', 'team'])


        print(f'gw_raw_year_df_dict[{year}] shape is {gw_raw_year_df_dict[year].shape}')

    return gw_raw_year_df_dict, fixture_year_df_dict


def main():
    gw_raw_year_df_dict, fixture_year_df_dict = create_gw_raw_df_dict(filepath=WEBSCRAPE_DATA_PATH)

    gw_raw_df = pd.concat(gw_raw_year_df_dict.values())
    gw_raw_df.to_csv(os.path.join(OUTPUT_DATA_PATH, INGESTED_DATA), index=False)


if __name__ == "__main__":
    main()
