# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 14:31:00 2021

@author: Jaden
"""

# import libraries
from sportsreference.ncaab.teams import Teams
from sportsreference.ncaab.roster import Player
from sportsreference.ncaab.roster import Roster

import pandas as pd
import csv
import os


#function to get team names
def get_team_id():
    """
    Creates CSV file of every teams' unique id
    
    example : 
        
        st. John's University - ST-JOHNS-NY
    """
    team_abb = []
    for team in Teams():
        team_abb.append(team.abbreviation)
    
    with open('Data/team_abb.csv','w',newline='') as result_file:
        wr = csv.writer(result_file, quoting=csv.QUOTE_ALL)
        wr.writerow(team_abb)
        

# Function to get player_ids
def get_player_id(school,start,end):
    """
    Creates csv with all player_ids from [X] school
    
    Parameters : school (string) - A string containing the abbreviation of team name
                 start (int) - Beginning year of search
                 end (int) -  last year of search - 1
    """
    player_id = []
    for i in range(start,end):
        for player in Roster(school,i).players:
            player_id.append(player.player_id)
    
    # 
    player_id = set(player_id)
    
    # Output list of player_id to a csv file
    with open('sportsref_Data/%s_player_id.csv' %school,'w',newline='') as result_file:
        wr = csv.writer(result_file, quoting=csv.QUOTE_ALL)
        wr.writerow(player_id)


 

def start_script(team_id,start,end):
        """
        Calls get_player_id() function and loops
    
        Parameters : team_id (string) - A string containing the abbreviation of team name
                     start (int) - Beginning year of search
                     end (int) -  last year of search - 1
        """
        for i in team_id:
            try:
                get_player_id(i,start,end)
                print(f'Successful : {i}')
            except:
                print(f'ERROR : {i}')



# List of team_ids imported from cssv  
with open('Data/team_abb.csv', newline='') as f:
    reader = csv.reader(f)
    team_ids = list(reader)
    team_ids = team_ids[0]
    
##################################################################### 
# Uncomment to begin script
start_script(team_ids,2000,2018)
#####################################################################

# Combining all collected player_id into a single csv
for path, subdirs, files in os.walk('sportsref_Data/'):
    f = [os.path.join(path,name) for name in files]

combined_csv = pd.concat( [ pd.read_csv(filename) for filename in f ] )
combined_csv.to_csv( "sportsref_Data/combined_csv.csv", index=False )

# Read csv[contains all player_ids] into a list
with open('sportsref_Data/combined_csv.csv', newline='') as f:
    reader = csv.reader(f)
    all_player_id = list(reader)
    all_player_id = all_player_id[0]

#initiate empty pandas DataFrame object
players_df = pd.DataFrame()

#loop through list of player_ids and pass to Player() API module to get their career stats
for i in all_player_id:
    # Only want the end of the dataframe (df[-2] is the last year played/ df[-1] is career stats)
    df = Player(i).dataframe.tail(2)
    # Creating a new column of the last year they played (used to differenciate players with the same names )
    df['year']= str(df.index[0])
    # Removing df[-2] because we only need career stats
    df = df.loc['Career']
    df = df.set_index('player_id')
    
    players_df = players_df.append(df)

players_df.to_csv('NCAA_players_career_data')





























