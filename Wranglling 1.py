# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 21:55:29 2022

@author: Shubham
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import os

os.chdir(r"D:\New folder\Prof.Amruta ma'am")
os.listdir()
police = pd.read_csv("fatal-police-shootings-data.csv")

#Data Exploration:
police.head()

police.shape

police.dtypes

police.ndim

#Data Cleaning - Checking for Missing Values and Duplicates:

police.isna().any()

police[police.isna().any(axis=1)].shape
 
#The 5 columns has the Nan values at the 1115 row in all data.
#Replace all nan values in the columns with object types as "not
#specified"

police[["armed","gender","race","flee"]] = police[["armed","gender","race","flee"]].fillna(value="not specified")   

police.isna().any()

police.duplicated().any()

#Converting to datatime type:
police["date"] = police["date"].apply(pd.to_datetime)

#Race Characterisation:
police["race"].unique()

race = police["race"].value_counts()

rac =px.pie(race,values=race.values, names=["white","black","hispanic","unknown","asian","native american","other"],title="Racial distribution")
rac.update_layout(font_size=16)
rac.update_traces(textfont_size=18,hoverinfo='label+percent')
rac.show()

#Almost half of the killed people were white americans. However,
#black and hispanic occupy the second and third place.

#Total Number of Deaths of Men and Women:
#-----------------------------------------

gender = police["gender"].value_counts()

sex = px.pie(gender, values = gender.values,names=["male","female","unknown"],title="Gender distribution",color_discrete_sequence=["blue","orange","yellow"],hole=0.4)
sex.update_layout(font_size=16)
sex.update_traces(textfont_size=18, textposition="inside",hoverinfo='label+percent')
sex.show()

#Mostly the men were killed by police. The women ration is only 4.38%

#Distribution of Age and Manner of Death:
#-----------------------------------------

manner2 = police.groupby(["age","manner_of_death"])["name"].count().reset_index()

man2 = px.bar(manner2,color="manner_of_death",y="name",x="age")
man2.update_layout(yaxis_title="Number of death")
man2.show()

#considering the graph the small part of people were tasered. The people at age
#25-50 year were more like to be tasered than other. The elderly people were only
#shot.

#Were people Armed ? What kind of weapons they used ?
#-----------------------------------------------------
armed = police["armed"].value_counts()

tab = go.Figure(police=[go.Table(header=dict(values=["Kind of weapons","Count"],fill_color="lavender",font=dict(size=14,color='black')),
                                 cells=dict(values=[armed.index, armed.values],fill_color="#F5F5DC"))])
tab.show()

(318*100)/armed.values.sum()

arm = px.bar(armed, x=armed.index[:3],y=armed.values[:3],title="Top 3 kind of weapons")
arm.update_layout(xaxis_title="Kind of weapons",yaxis_title="Count")
arm.show()

#The most popular kind of weapons that victims had was guns and knives. However, people
#defended themselves with the most surprising objects that could find. Only 5.95% of the
#people were unarmed completely.

#Did people fleeing?
#--------------------

flee = police["flee"].value_counts()
flee

(3356*100)/(flee.values.sum()-250)

fle =px.bar(flee,x=flee.index[:3],y=flee.values[:3],title="Types of fleeting")
fle.update_layout(xaxis_title="Type of fleeting",yaxis_title="Count")
fle.show()

#64.95% of people were not fleeing. The others were using cars or were running from the police.

#Age distribution:
age_id = police.groupby("id").agg({"age":pd.Series.mean})
age_id = age_id.sort_values("age",ascending=False)
age_id.isna().sum()

age_id.dropna()

age_id.describe()

sns.histplot(data=age_id, x="age", bins=age_id["age"].nunique(), kde=True, alpha=0.4)
plt.show()

#The age distribution fluctuates from 6 to 91. The most popular age range of 30-40. The average
#37 years old with the most  killed cases.

#Race and age distribution:
#---------------------------

age_race = police.groupby(["race", "id"], as_index=False).agg({"age": pd.Series.mean})
age_race.dropna()

sns.histplot(data=age_race, x="age", hue="race", multiple="stack")
plt.show()