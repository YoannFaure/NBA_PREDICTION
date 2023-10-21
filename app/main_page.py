import requests
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(layout="wide")

# Création page
st.sidebar.markdown("#Dashboard")

st.title("NBA Player Stats Explorer")


# Importation data
@st.cache_data
def load_data():
    data = pd.read_csv(
        "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/data/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
    )  # Assurez-vous de spécifier le bon chemin vers votre fichier CSV
    return data


# Charger le DataFrame en utilisant la fonction mise en cache
data = load_data()

# Widget multiselect pour choisir un joueur
selected_player = st.multiselect("Sélectionnez un joueur", data["Player Name"].unique())

# Filtrer les données en fonction du joueur sélectionné
if selected_player:
    data = data[data["Player Name"].isin(selected_player)]


#########################################
# Plot data
#########################################
# Créez un scatter plot Plotly Express

fig = px.scatter(data, x="X Location", y="Y Location")
# Personnalisez la configuration de Plotly pour masquer les options de sélection
fig.update_layout(
    showlegend=False,  # Masque la légende
    modebar={"displayModeBar": False},  # Masque la barre d'options de sélection
)
# Affichez la figure Plotly dans Streamlit
st.plotly_chart(fig)
