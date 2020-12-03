"""
Created by  Ege of the House Hoşgüngör, the First of His Name  at 22:09 1.12.2020
"""
import sys
import datetime as dt
#Regular expressions            
import re 
import pandas as pd


    
    
##Example

# message = '[7.10.2016 15:05:29] Reyhan Cagac: Batıya söyleniyor'
# pattern = '\[([0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\, [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9])\] (.+)\: (.*)'

# matches = re.search(pattern,message)
# print(matches.group(0))
# date = matches.group(1)
# username = matches.group(2)
# mess1 = matches.group(3)

def createDataFrame(data_path = 'whatsapp_e.txt', data_pattern= 0):
    
    if data_pattern == 0:
        pattern = '\[([0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\, [0-9][0-9]\:[0-9][0-9]\:[0-9][0-9])\] (.+)\: (.*)'
    elif data_pattern == 1:
        pattern = '\[([0-9]+\.[0-9]+\.[0-9]+ [0-9]+\:[0-9]+\:[0-9]+)\] (.+)\: (.*)'
    
    with open(data_path, encoding = 'utf-8') as outfile:
        raw_text = outfile.readlines()
        messages = {}
        #Create an empty dataframe
        df1 = []
        for message in raw_text:
            matches = re.search(pattern,message)
            
            if (re.match(pattern,message)):      
                date_str = matches.group(1)
                if data_pattern == 0:
                    date = dt.datetime.strptime(date_str, '%d/%m/%Y, %H:%M:%S')
                elif data_pattern == 1:
                    date = dt.datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')
                    
                name = matches.group(2)
                mess = matches.group(3)
                
                       
                data = [date,name,mess]
                df1.append(data) 
            else:
                continue
                #print('There are some outliers phencot in the data')       
                #print(message)
                
        df1 = pd.DataFrame(data =df1, columns=['Date','User','Raw_Message'])
    return df1

df = createDataFrame('whatsapp.txt', data_pattern = 1)
df1 = createDataFrame('whatsapp_e.txt', data_pattern = 0)
df2 = createDataFrame('whatsapp_death.txt', data_pattern = 0)

def remove_inactive_users(df, min_messages=10):
    """ Removes inactive users or users that have 
    posted very few messages. 
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe of all messages 
    min_messages: int, default 10
        Number of minimum messages that a user must have
        
    Returns:
    --------
    df : pandas dataframe
        Dataframe of all messages
        
    """
    # Remove users that have not posted more than min_messages
    to_keep = df.groupby('User').count().reset_index()
    to_keep = to_keep.loc[to_keep['Raw_Message'] >= min_messages, 'User'].values
    df = df[df.User.isin(to_keep)]
    return df

df2=remove_inactive_users(df2,10)


#Top 10 users who talks too much
users = df.User.value_counts()
users = users[0:10]
users = users.reset_index()
