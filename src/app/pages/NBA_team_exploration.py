import streamlit as st
import pandas as pd
import plotly.express as px


# Création page
st.sidebar.markdown("NBA team exploration")
st.title("NBA team exploration")


# Importation data
@st.cache_data
def load_data():
    data = pd.read_csv(
        "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/NBA/data/NBA_games_data/ranking.csv"
    )
    return data


# Charger le DataFrame en utilisant la fonction mise en cache
Teams_ranking = load_data()

st.header("NBA games dataset")

# Afficher des informations sur le dataframe
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"#### 🏀 {games_details['PLAYER_ID'].nunique()} Teams Played")
with col2:
    st.markdown(f"#### 📆 {games_details['GAME_ID'].nunique()} Unique Dates")
with col3:
    st.markdown(f"#### 🗑️ {games_details['PTS'].sum()} Points")
with col4:
    st.markdown(f"#### ⛹️ {games_details['FGM'].sum()} Field Goals")

st.header("NBA Team Average Stats")


st.write("Moyenne Point/Game")

st.dataframe(games_details.head(50))

games = games_details


st.header("Match results")

st.header("Match analyse")
