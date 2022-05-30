import streamlit as st
import pandas as pd
import numpy as np



# Reading Data
url = 'https://drive.google.com/file/d/1-0FlARiLI7RMiKCUYwAOGBCXGI1895j4/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

data = pd.read_csv(path)




st.title("Drug Recommendation System")

popular_conditions = ('Birth Control','Depression','Pain','Anxiety','Acne','Bipolar Disorde','Insomnia','Weight Loss',
                      'Obesity','ADHD', 'Diabetes, Type 2', 'Emergency Contraception', 'High Blood Pressure','Migrane')
conditions = data.loc[data['condition'].isin(popular_conditions)]


user_choice = st.selectbox("Select Condition", popular_conditions)

col1, col2 = st.columns(2)

with col1:
    st.title("Top 5 Drugs")
    st.dataframe(data[data['condition'] == user_choice][['drugName','usefulness']].sort_values(by = 'usefulness',
                                                 ascending = False).head().reset_index(drop = True))
with col2:
    st.title("Bottom 5 Drugs")
    st.dataframe(data[data['condition'] == user_choice][['drugName','usefulness']].sort_values(by = 'usefulness',
                                                 ascending = True).head().reset_index(drop = True))
