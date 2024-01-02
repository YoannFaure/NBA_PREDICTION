import streamlit as st
import pandas as pd

## Initalisation de la page ## 

st.set_page_config(
    page_title="Les données",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

st.sidebar.header("LES DATASETS")

## LOAD DATA ##

@st.cache_data
def load_data():
    shot_location = pd.read_csv("data/raw/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.zip")
    player = pd.read_csv("data/raw/NBA_Players_stats_since_1950/Players.zip")
    players_data = pd.read_csv("data/raw/NBA_Players_stats_since_1950/player_data.zip")
    seasons_stats = pd.read_csv("data/raw/NBA_Players_stats_since_1950/Seasons_Stats.zip")

    return shot_location, player, players_data, seasons_stats

shot_location, player, players_data, seasons_stats = load_data()

## BODY ##

st.header("LES DATASETS")
st.markdown("""---""")


tab1, tab2, tab3, tab4 = st.tabs(["SHOT LOCATION", "PLAYERS", "PLAYER DATA", "SEASONS STATS"])

with tab1:
   st.write("#### La table 'shot_location'")
   st.dataframe(shot_location.head(1000))
   
   with st.expander("Voir les détails du dataset"):
        st.markdown(
            """
            La table "shot_location" est composée de :red[**4 729 512 lignes**] et contient une description des shots des matchs de basket-ball.

            1. :red[**Game ID**] (*int64*) - Identifiant du match - *NA : 0,00%*
            2. :red[**Game Event ID**] (*int64*) - Identifiant de l'événement du match - *NA : 0,00%*
            3. :red[**Player ID**] (*int64*) - L'identifiant du joueur - *NA : 0,00%*
            4. :red[**Player Name**] (*str*) - Le nom du joueur de basket-ball - *NA : 0,00%*
            5. :red[**Team ID**] (*int64*) - L'identifiant de l'équipe - *NA : 0,00%*
            6. :red[**Team Name**] (*str*) - Le nom de l'équipe - *NA : 0,00%*
            7. :red[**Period**] (*int64*) - Le numéro de période du match - *NA : 0,00%*
            8. :red[**Minutes Remaining**] (*int64*) - Le nombre de minutes restantes dans la période - *NA : 0,00%*
            9. :red[**Seconds Remaining**] (*int64*) - Le nombre de secondes restantes dans la période - *NA : 0,00%*
            10. :red[**Action Type**] (*object*) - Le type d'action effectuée (par exemple, un tir, une passe, etc.) - *NA : 0,00%*
            11. :red[**Shot Type**] (*str*) - Le type de tir (par exemple, un tir à trois points, un tir à deux points, etc.) - *NA : 0,00%*
            12. :red[**Shot Zone Basic**] (*str*) - La zone de tir de base - *NA : 0,00%*
            13. :red[**Shot Zone Area**] (*str*) - La zone de tir (zone sur le terrain) - *NA : 0,00%*
            14. :red[**Shot Zone Range**] (*str*) - La portée de la zone de tir (proche, moyenne, lointaine, etc.) - *NA : 0,00%*
            15. :red[**Shot Distance**] (*int64*) - La distance du tir par rapport au panier - *NA : 0,00%*
            16. :red[**X Location**] (*int64*) - La coordonnée X de l'emplacement du tir sur le terrain - *NA : 0,00%*
            17. :red[**Y Location**] (*int64*) - La coordonnée Y de l'emplacement du tir sur le terrain - *NA : 0,00%*
            18. :red[**Shot Made Flag**] (*int64*) - Un indicateur de réussite du tir (par exemple, si le tir a été réussi ou manqué) - *NA : 0,00%*
            19. :red[**Game Date**] (*int64*) - La date du match - *NA : 0,00%*
            20. :red[**Home Team**] (*str*) - Le nom de l'équipe à domicile - *NA : 0,00%*
            21. :red[**Away Team**] (*str*) - Le nom de l'équipe à l'extérieur - *NA : 0,00%*
            22. :red[**Season Type**] (*str*) - Le type de saison (par exemple, saison régulière, séries éliminatoires, etc.) - *NA : 0,00%*
                """
            )
    
with tab2:
   st.write("#### La table 'player'")
   st.dataframe(player.head(1000))
   
   with st.expander("Voir les détails du dataset"):
        st.markdown(
            """
            La table "players" est composée de :red[**3 922 lignes**] et contient des informations détaillées sur les joueurs de basket-ball.

            1. :red[**Unnamed: 0**] (*int64*) - Colonne d'index - *NA : 0,00%*
            2. :red[**Player**] (*str*) - Le nom du joueur de basket-ball - *NA : 0,03%*
            3. :red[**height**] (*float64*) - La taille du joueur en unités spécifiques - *NA : 0,03%*
            4. :red[**weight**] (*float64*) - Le poids du joueur en unités spécifiques - *NA : 0,03%*
            5. :red[**collage**] (*str*) - Le nom de l'établissement d'enseignement supérieur ou université où le joueur a fréquenté - *NA : 8,90%*
            6. :red[**born**] (*float64*) - La date de naissance du joueur - *NA : 0,03%*
            7. :red[**birth_city**] (*str*) - La ville de naissance du joueur - *NA : 11,98%*
            8. :red[**birth_state**] (*str*) - L'État de naissance du joueur - *NA : 12,32%*
            """
            )

with tab3:
   st.write("#### La table 'players_data'")
   st.dataframe(players_data.head(1000))
   
   with st.expander("Voir les détails du dataset"):
        st.markdown(
            """
            La table "players_data" est composée de :red[**4 550 lignes**] et contient des informations sur les carractéristique des joueurs.

            1. :red[**name**] (*object*) - Le nom du joueur de basket-ball - *NA : 0,00%*
            2. :red[**year_start**] (*int64*) - L'année de début de carrière du joueur dans la NBA - *NA : 0,00%*
            3. :red[**year_end**] (*int64*) - L'année de fin de carrière du joueur dans la NBA - *NA : 0,00%*
            4. :red[**position**] (*object*) - La position ou le poste de jeu du joueur sur le terrain - *NA : 0,02%*
            5. :red[**height**] (*object*) - La taille du joueur en unités spécifiques - *NA : 0,02%*
            6. :red[**weight**] (*float64*) - Le poids du joueur en unités spécifiques - *NA : 0,13%*
            7. :red[**birth_date**] (*object*) - La date de naissance du joueur - *NA : 0,68%*
            8. :red[**college**] (*object*) - Le nom de l'établissement d'enseignement supérieur ou université où le joueur a fréquenté - *NA : 6,64%*
            """
            )


with tab4:
   st.write("#### La table 'seasons_stats'")
   st.dataframe(seasons_stats.head(1000))
   
   with st.expander("Voir les détails du dataset"):
    st.markdown(
        """
        La table "seasons_stats" est composée de :red[**24 691 lignes**] et contient des données statistiques sur les joueurs de basket-ball pour différentes saisons.

        1. :red[**Unnamed: 0**] (*int64*) - Colonne d'index ou d'identifiant unique - *NA : 0,00%*
        2. :red[**Year**] (*float64*) - L'année des données statistiques - *NA : 0,27%*
        3. :red[**Player**] (*str*) - Le nom du joueur - *NA : 0,27%*
        4. :red[**Pos**] (*str*) - La position du joueur sur le terrain - *NA : 0,27%*
        5. :red[**Age**] (*float64*) - L'âge du joueur à la fin de la saison - *NA : 0,30%*
        6. :red[**Tm**] (*str*) - L'abréviation de l'équipe du joueur pour la saison - *NA : 0,27%*
        7. :red[**G**] (*float64*) - Le nombre de matchs joués par le joueur - *NA : 0,27%*
        8. :red[**GS**] (*float64*) - Le nombre de matchs joués en tant que titulaire - *NA : 26,16%*
        9. :red[**MP**] (*float64*) - Le nombre de minutes jouées par le joueur - *NA : 2,24%*
        10. :red[**PER**] (*float64*) - L'Indice d'efficacité du joueur - *NA : 2,39%*
        11. :red[**TS%**] (*float64*) - Le pourcentage de tir réel du joueur - *NA : 0,62%*
        12. :red[**3PAr**] (*float64*) - Le pourcentage de tentatives de tir à trois points - *NA : 23,70%*
        13. :red[**FTr**] (*float64*) - Le ratio de tentatives de lancer franc - *NA : 0,67%*
        14. :red[**ORB%**] (*float64*) - Le pourcentage de rebonds offensifs pris par le joueur - *NA : 15,79%*
        15. :red[**DRB%**] (*float64*) - Le pourcentage de rebonds défensifs pris par le joueur - *NA : 15,79%*
        16. :red[**TRB%**] (*float64*) - Le pourcentage de rebonds totaux pris par le joueur - *NA : 12,64%*
        17. :red[**AST%**] (*float64*) - Le pourcentage d'assists réalisés par le joueur - *NA : 8,65%*
        18. :red[**STL%**] (*float64*) - Le pourcentage de vols de balle réalisés par le joueur - *NA : 15,79%*
        19. :red[**BLK%**] (*float64*) - Le pourcentage de contres réalisés par le joueur - *NA : 15,79%*
        20. :red[**TOV%**] (*float64*) - Le pourcentage de pertes de balle du joueur - *NA : 20,69%*
        21. :red[**USG%**] (*float64*) - Le pourcentage d'utilisation du joueur - *NA : 20,46%*
        22. :red[**blanl**] (*float64*) - Une colonne vide ou non utilisée - *NA : 100,00%*
        23. :red[**OWS**] (*float64*) - Les victoires créées par le joueur en attaque - *NA : 0,43%*
        24. :red[**DWS**] (*float64*) - Les victoires créées par le joueur en défense - *NA : 0,43%*
        25. :red[**WS**] (*float64*) - Les victoires totales créées par le joueur - *NA : 0,43%*
        26. :red[**WS/48**] (*float64*) - Les victoires totales créées par le joueur par 48 minutes jouées - *NA : 2,39%*
        27. :red[**blank2**] (*float64*) - Une colonne vide ou non utilisée - *NA : 100,00%*
        28. :red[**OBPM**] (*float64*) - Le point marqué par un joueur au-dessus de la moyenne par 100 possessions en attaque - *NA : 15,77%*
        29. :red[**DBPM**] (*float64*) - Le point marqué par un joueur au-dessus de la moyenne par 100 possessions en défense - *NA : 15,77%*
        30. :red[**BPM**] (*float64*) - Le point marqué par un joueur au-dessus de la moyenne par 100 possessions - *NA : 15,77%*
        31. :red[**VORP**] (*float64*) - La valeur du joueur par rapport à un joueur remplaçant - *NA : 15,77%*
        32. :red[**FG**] (*float64*) - Le nombre de tirs réussis - *NA : 0,27%*
        33. :red[**FGA**] (*float64*) - Le nombre total de tentatives de tir - *NA : 0,27%*
        34. :red[**FG%**] (*float64*) - Le pourcentage de réussite des tirs - *NA : 0,67%*
        35. :red[**3P**] (*float64*) - Le nombre de tirs à trois points réussis - *NA : 23,34%*
        36. :red[**3PA**] (*float64*) - Le nombre total de tentatives de tirs à trois points - *NA : 23,34%*
        37. :red[**3P%**] (*float64*) - Le pourcentage de réussite des tirs à trois points - *NA : 37,56%*
        38. :red[**2P**] (*float64*) - Le nombre de tirs à deux points réussis - *NA : 0,27%*
        39. :red[**2PA**] (*float64*) - Le nombre total de tentatives de tirs à deux points - *NA : 0,27%*
        40. :red[**2P%**] (*float64*) - Le pourcentage de réussite des tirs à deux points - *NA : 0,79%*
        41. :red[**eFG%**] (*float64*) - Le pourcentage de réussite des tirs ajusté en tenant compte des tirs à trois points - *NA : 0,67%*
        42. :red[**FT**] (*float64*) - Le nombre de lancers francs réussis - *NA : 0,27%*
        43. :red[**FTA**] (*float64*) - Le nombre total de tentatives de lancers francs - *NA : 0,27%*
        44. :red[**FT%**] (*float64*) - Le pourcentage de réussite des lancers francs - *NA : 3,75%*
        45. :red[**ORB**] (*float64*) - Le nombre de rebonds offensifs - *NA : 15,77%*
        46. :red[**DRB**] (*float64*) - Le nombre de rebonds défensifs - *NA : 15,77%*
        47. :red[**TRB**] (*float64*) - Le nombre total de rebonds - *NA : 1,53%*
        48. :red[**AST**] (*float64*) - Le nombre d'assists - *NA : 0,27%*
        49. :red[**STL**] (*float64*) - Le nombre de vols de balle réalisés - *NA : 15,77%*
        50. :red[**BLK**] (*float64*) - Le nombre de contres réalisés - *NA : 15,77%*
        51. :red[**TOV**] (*float64*) - Le nombre de pertes de balle - *NA : 20,44%*
        52. :red[**PF**] (*float64*) - Le nombre de fautes personnelles commises - *NA : 0,27%*
        53. :red[**PTS**] (*float64*) - Le nombre total de points marqués - *NA : 0,27%*
        """
    )
    
