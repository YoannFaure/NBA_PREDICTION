import streamlit as st

## Initalisation de la page ## 

st.set_page_config(
    page_title="Projet NBA",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="collapsed"
)
## BODY ##
st.image("reports/NBA_white.png")
st.header("BIENVENUE DANS L'APP -  NBA SHOT PREDICTION !")
st.markdown("""---""")

st.markdown(
    """
    Ce projet captivant représente une étape cruciale de notre formation en data science dispensée par l'organisme Datascientest,
    nous permettant de plonger au cœur de l'analyse des performances des plus grands joueurs de la NBA du 21ème siècle.
    
    Grâce à des ensembles de données provenant d'un jeu de donnée Kaggle, nous explorons les données sur les tirs des joueurs de la NBA entre 1997 et 2019.
    La taille du dataset nous permet d'étudier la fréquence  et l'efficacité des tirs, tout en cherchant à établir des modèles prédictifs fiables pour estimer la probabilité de réussite d'un tir 
    en fonction de multiples variables.

    Cette démarche analytique, entreprise dans le cadre de notre formation, vise à décrypter les subtilités des performances sportives,
    ouvrant ainsi la voie à une compréhension plus profonde des stratégies et des compétences mises en œuvre par les plus grands joueurs de la NBA.
    """
    )

st.write("#### Téléchargement des jeux de données :")
if st.checkbox("Afficher les liens"):
    st.markdown(
        """
        - dataset des tirs NBA entre 1997 et 2019 : [kaggle](https://www.kaggle.com/jonathangmwl/nba-shot-locations)
        - dataset des bilans d’équipe entre 2014 et 2018 : [kaggle](https://www.kaggle.com/nathanlauga/nba-games?select=ranking.csv)
        - dataset des joueurs de NBA depuis 1950 : [kaggle](https://www.kaggle.com/drgilermo/nba-players-stats?select=Players.csv)
        """
    )
    

