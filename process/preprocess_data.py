# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:27:06 2020

"""

import re
from datetime import datetime
from dateutil.parser import parse, ParserError 
import pandas as pd



def createDataFrame(data_path = 'whatsapp.txt'):
    """ Creates a DataFrame from a exported Whatsapp Chat
    
    Parameters:
    -----------
    data_path : path of txt file
        
    Returns:
    --------
    df : pandas dataframe
        Dataframe of all messages,dates,users and raw whatsapp message.
        
    """
    all_lines = []
    i = 0
    TYPE_MESSAGE="message"
    TYPE_CONTROL="control"
    
    for line in open(data_path, encoding= "utf8"):
        try:
            if not line:
                continue # emptyline
            line = line.replace("\xa0", " ")
            
    
            date=None
            if line.startswith("[") and "]" in line:
                timestamp = line.split("[")[1].split("]")[0]
                try:
                    date= parse(timestamp, default=datetime(1970,1,1))
                    if date.year==1970:
                        date.year=all_lines[-1].date.year
                except:
                    pass
            
            if date:
                #new line
                body=line.split("] ",1)[1]
                if(":"in body):
                    _type=TYPE_MESSAGE
                    sender,body=body.split(": ",1)
                else:
                    _type=TYPE_CONTROL
                    sender=""
                
                all_lines.append({               
                    "Date":date,
                    "Type":_type,
                    "User":sender,
                    "Body":body,
                    "Raw":line,
                })
            else:
                # existing
                all_lines[-1]['Raw'] += line
                all_lines[-1]['Body'] += line
        except KeyboardInterrupt as e:
            break
        except Exception as e:
            print("FAILED", line,e)
    
    df = pd.DataFrame(data =all_lines, columns=['Date','Type','User','Body','Raw'])
    return df

df = createDataFrame('whatsapp.txt')

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
    to_keep = to_keep.loc[to_keep['Body'] >= min_messages, 'User'].values
    df = df[df.User.isin(to_keep)]
    return df


def select_by_users(df,users):
    """Selects some of the users so we do not
    need to process every user in the group
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe of all messages 
    users: string array
        The users that you want to keep
        
    Returns:
    --------
    df : pandas dataframe
        Dataframe of all messages with selected users
    
    """
    df_new =  df.loc[df['User'].isin(users)]
    return df_new

###############################################################################
df1=remove_inactive_users(df,10)
users = df.User.value_counts()
###############################################################################
users1 = ['Selim Olcuoglu','Ufuk Ural','Deniz Yagmur Karatepe', 'Merve Sahin', 'Berfin Erdogan ']

users2 = ['Burak Ural','Basak Didem Daglioglu','Ufuk Ural','Berfin Erdogan']

user3 = ['Ege Hosgungor']

df3 = select_by_users(df1, user3)
plot_messages(df3, colors=None, trendline=False, savefig=False, dpi=100)
