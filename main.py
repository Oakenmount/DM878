import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#import data
covid = pd.read_csv("out2.csv")
states = pd.read_csv("statedata.tsv",sep="\t")
mandates = pd.read_csv("mask-mandates.tsv",sep="\t")

'''
#add political parameter
states.insert(1,"political","neutral")
for index,row in states.iterrows():
    if row["demVotes"] > 0.55:
        states.at[index,"political"] = "Blue"
    elif row["demVotes"] > 0.51:
        states.at[index,"political"] = "Blue majority"
    elif row["demVotes"] > 0.49:
        states.at[index,"political"] = "split"
    elif row["demVotes"] > 0.45:
        states.at[index,"political"] = "Red majority"
    else:
        states.at[index,"political"] = "Red"
'''

df = covid.join(states.set_index("state"), on="state")

#update deaths to death per 1 mil population
for i in range(len(df)):
    deaths = df.at[i,"deaths"]
    population = df.at[i,"population"]
    df.at[i,"deaths"] = (deaths/population)*1000000
for i in range(len(df)):
    infected = df.at[i,"cases"]
    population = df.at[i,"population"]
    df.at[i,"cases"] = (infected/population)*1000000


fig = px.scatter(df,x="deaths", y="cases",animation_frame="date",
    hover_name="state", log_x=False,
    animation_group="state",color="demVotes",color_continuous_scale=[(0,"red"), (0.5,"grey"),(1,"blue")],range_color=[0.45,0.55],
    size="population",text="state",
    size_max=45,range_x=[0,2100], range_y=[0,125000]
 )
fig.add_annotation(x=600, y=110000,
    text="Cross indicates state-wide mask mandate.",
    showarrow=False)
# Tune marker appearance and layout
fig.update_traces(mode="markers", marker=dict(sizemode="area"),textposition='top center')
#Add more descriptors to figure.
fig.update_layout(
title="US COVID-19 cases and death per million population",
 xaxis=dict(
     title="Deaths per million population",
     gridcolor="white",
     gridwidth=2,
 ),
 yaxis=dict(
     title="Cases per million population",
     gridcolor="white",
     gridwidth=2,
 ),
 coloraxis_colorbar=dict(
    title="Democrat votes",
    tickvals=[0.45,0.48,0.5,0.52,0.55],
    ticktext=["45%", "48%", "50%", "52%", "55%"],
),
 paper_bgcolor='rgb(243, 243, 243)',
 plot_bgcolor='rgb(243, 243, 243)',
 transition_duration=300,
)

#store mask symbol for each state, to be used during frame overwrite.
symbols = {}
states = ["District of Columbia","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","West Virginia","Wisconsin","Wyoming","Washington"]
for state in states:
    symbols[state] = "circle"

#update frames to overwrite markers. This was the only hack I could come up with to change markers during the animation.
for i in range(len(fig.frames)):
    frame = fig.frames[i]
    date = frame.name
    found = mandates.loc[mandates["date"]==date] #Check if a mandate was added on this date
    if len(found) > 0: #at least one was found
        for state in found.state:
            symbols[state] = "x" #use mask
    updatedSymbols = updatedSymbols = list(map(lambda x : symbols[x],frame.data[0].ids)) #map mask mandate to state order in frame.
    frame.data[0].marker.symbol = updatedSymbols #set symbols for frame

    #check if any states added a mandate

# change animation speed set by button
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400

fig.show()
