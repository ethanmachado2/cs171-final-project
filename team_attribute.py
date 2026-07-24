import pandas as pd

match = pd.read_csv('data/Match.csv')

match['date'] = pd.to_datetime(match['date'])


# Filter relevant columns for ML model
match = match[['match_api_id', 'date', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal', 'B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA']]

match = match.sort_values(by='date')

match.rename(columns={'date': 'match_date'}, inplace=True)

# filter team attributes table to only numbers
ta = pd.read_csv('data/Team_Attributes.csv')

ta['date'] = pd.to_datetime(ta['date'])

ta = ta.sort_values(by='date')

ta.rename(columns={'date': 'ta_date'}, inplace=True)

ta = ta[['team_api_id', 'ta_date', 'buildUpPlaySpeed', 
    'buildUpPlayPassing', 'chanceCreationPassing', 'chanceCreationCrossing', 'chanceCreationShooting', 
    'defencePressure', 'defenceAggression', 'defenceTeamWidth']]

#Merge team attributes with match data
match_with_att = pd.merge_asof(
    match,
    ta.add_prefix('h_'),
    left_on = 'match_date',
    right_on = 'h_ta_date',
    left_by = 'home_team_api_id',
    right_by = 'h_team_api_id',
    direction = 'backward'
)

#merging away team attributes with match data
match_with_att = pd.merge_asof(
    match_with_att,
    ta.add_prefix('a_'),
    left_on = 'match_date',
    right_on = 'a_ta_date',
    left_by = 'away_team_api_id',
    right_by = 'a_team_api_id',
    direction = 'backward'
)


#Drop unnecessary columns and rows with null values
match_with_att = match_with_att.drop(columns=['home_team_api_id', 'h_ta_date', 'h_team_api_id', 'away_team_api_id', 'a_ta_date', 'a_team_api_id'])

match_with_att.dropna(subset=['h_buildUpPlaySpeed', 'a_buildUpPlaySpeed'], inplace=True)


#Export to CSV for ML model
match_with_att.to_csv("match_with_att_dropna_bettingNA.csv", index=False)

