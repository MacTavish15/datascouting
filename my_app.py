import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image


def check_level(value):
    if value <=0.25:
        return 0
    elif value > 0.25 and value <=.5:
        return 1
    elif value > 0.5 and value <=.75:
        return 2
    elif value >.75 and value <= 1:
        return 3
    else:
        return -1

def addlabels(ax,x,y):
    for i in range(len(x)):
        ax.text(i,y[i],y[i],fontsize=12,color = "white")
        ax.text(i,y[i],y[i],fontsize=12,color = "white")




img = Image.open("Logo-Banner.png")
st.sidebar.image(img,use_column_width=True)


data = pd.read_csv('FBRef Data/2024/Filtered_Combined_Data_2024.csv')
data['attribut_defensive'] = (data['Tackles_Won_per90']+data['Tackles_Def_3rd_per90']+data['Dribblers_Tackled_per90']+data['Blocks_per90']+data['Passes_Blocked_Def_per90']+data['Interceptions_per90'])/6
data['attribut_progression'] = (data['Passes_1/3_per90']+data['Passes_Long_Cmp_per90']+data['Progressive_Passes_per90']+data['Prg_Carries_per90']+data['Prg_Passes_per90'])/5
data['attack_intelligence'] = (data['xA_per90']+data['A-xAG_per90']+data['Goals_per90']+data['G+A_per90']+data['xG_per90']+data['xAG_per90_y']+data['xG+xAG_per90']+data['Shots_total_per90']+data['Shots_on_target_per90']+data['Goals_per_shot']+data['Goals_per_shot_on_target'])/11
data['creating_chances'] = (data['Key_Passes_per90']+data['xA_per90']+data['Passes_Penalty_Area_per90']+data['Crosses_Penalty_Area_per90']+data['Carries_Penalty_Area_per90'])/5
data['attribut_dribble'] = (data['Carries_per90']+data['Take_Ons_Succ_per90'])/2

numerical_data = data[['attribut_defensive','attribut_progression','attack_intelligence','creating_chances','attribut_dribble']]
array = numerical_data.to_numpy()
scaler = StandardScaler()
scaler.fit(array)
array = scaler.transform(array)
scaler = MinMaxScaler()
scaled_scores = scaler.fit_transform(array)
df = pd.DataFrame(scaled_scores, columns=numerical_data.columns)

df.insert(0, "Player", data.Player.to_numpy(), True)
df.insert(0, "Pos", data.Pos.to_numpy(), True)
df.insert(0, "Squad", data.Squad.to_numpy(), True)
df.insert(0, "Age", data.Age.to_numpy(), True)
midfielders = df[df['Pos'].str.contains('MF')]
young_midfielders = midfielders[midfielders.Age <=25]

select_player = st.sidebar.selectbox('Players',young_midfielders.Player.unique())

young_midfielders['Score'] = (young_midfielders['attribut_defensive']+young_midfielders['attribut_progression']+young_midfielders['attack_intelligence']+young_midfielders['creating_chances']+young_midfielders['attribut_dribble'])/5

young_midfielders.sort_values(['Score'],ascending=False)[["Squad","Player","Score"]].head(30)

year = 2024
player = select_player


value_player = young_midfielders[young_midfielders.Player == player]

st.write(""" Player Qualifications """)

st.table(value_player)
st.write(""" Player Qualifications Plot """)

face_color = "#b3cde0"


fig = plt.figure(figsize=(8,8))
fig.patch.set_facecolor(face_color)
import matplotlib as mpl
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.left'] = False
mpl.rcParams['axes.spines.bottom'] = False
y_label = ['Poor','Medium','Good','Elite']

# AX1
ax1 = fig.add_axes([0,.8,1,0.2])
ax1.patch.set_facecolor(face_color)
ax1.text(0.05,0.2,fontsize=15,s= player + " ("+value_player.Squad.unique()[0]  + ") Qualifications / "+ str(year) + " @WalidBOUMAHDI",color ="#011f4b",ha="left")
ax1.text(0.05,0.2,fontsize=15,s= player + " ("+value_player.Squad.unique()[0]  + ") Qualifications / "+ str(year) + " @WalidBOUMAHDI",color ="#011f4b",ha="left")
ax1.text(0.05,0.05,fontsize=15,s= "Total Score :" + str(value_player.Score.unique()[0].round(2)) + " - " + y_label[check_level(value_player.Score.unique()[0])] + " Player"  ,color ="#011f4b",ha="left")

# AX2
ax2= fig.add_axes([.0,.0,.2,0.8])
ax2.patch.set_facecolor(face_color)
colors = ["#6497b1","#005b96","#03396c","#011f4b"]
ax2.text(0.4,0,fontsize=20,s=y_label[0],color =colors[0],ha="left")
ax2.text(0.2,0.25,fontsize=20,s=y_label[1],color =colors[1],ha="left")
ax2.text(0.3,0.5,fontsize=20,s=y_label[2],color =colors[2],ha="left")
ax2.text(0.3,.75,fontsize=20,s=y_label[3],color =colors[3],ha="left")
# AX3
ax3 = fig.add_axes([.2,.0,.8,0.8])
ax3.patch.set_facecolor(face_color)
x_label = ['Defensive Actions','Progression','Atk Intelligence','Creating Chances','Dribbling']
values =  value_player[['attribut_defensive','attribut_progression','attack_intelligence','creating_chances','attribut_dribble']].to_numpy()[0]
indices = []
for v in values:
    indices.append(check_level(v))
bar_colors = [colors[indices[0]],colors[indices[1]],colors[indices[2]],colors[indices[3]],colors[indices[4]]]
bar_container = ax3.bar(x_label,values, label=x_label,color=bar_colors)

ax3.axhline(y=0,linestyle="--",linewidth=0.5,color='#6497b1')
ax3.axhline(y=0.25,linestyle="--",linewidth=0.5,color='#005b96')
ax3.axhline(y=0.5,linestyle="--",linewidth=0.5,color='#03396c')
ax3.axhline(y=.75,linestyle="--",linewidth=0.5,color='#011f4b')
ax3.set_ylim(0,1)
ax3.tick_params(axis='x', colors='#011f4b', size=18)
addlabels(ax3,x_label, values.round(2))
plt.xticks(fontsize=14,rotation=45)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
st.pyplot(fig)


###https://datascouting-3epkjldyav7wu5ecfqqoeh.streamlit.app/
