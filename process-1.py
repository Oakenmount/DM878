import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","West Virginia","Wisconsin","Wyoming","Washington"]
#import data
df = pd.read_csv("us-states.csv")
df = df.drop(columns=["fips"])
df.insert(4,"infected",0)
#print(df)
previous = {}
for date in df.date.unique():
    for state in states:
        #if entry doesn't exist, we add it. First entry has been manually added
        if len(df.loc[(df['date']==date) & (df['state']==state)]) == 0:
            prev = previous[state]
            index = prev.index[0]
            prev.at[index,"date"] = date
            df = df.append(prev)
            # We don't worry about updating previous, since only the date is changed.

        #get row for this date and state
        cur = df.loc[(df['date']==date) & (df['state']==state)]

        #Compare case numbers
        if state in previous.keys(): #doesn't exist on first run
            prev = previous[state]
            pindex = prev.index[0]
            index = cur.index[0]
            infected = cur.at[index,"cases"] - prev.at[pindex,"cases"]
            df.at[index,"infected"] = infected

        #update previous to current date
        previous[state] = cur

df.to_csv("out1.csv")
