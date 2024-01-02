import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Preprocessing",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

st.header("Preprocessing")
st.sidebar.header("Preprocessing")
st.markdown("""---""")


multi = '''
En quoi consiste notre preprocessing.

1. Catégorisation
2. Filtrage des données
3. Réduction des colonnes non pertinentes ou redondantes
4. Ajout de données additionnelles

'''
st.markdown(multi)



st.markdown("# Catégorisation")
multi = '''

Notre table pricipale décrivait très précisemment le type de "tir" effectué par le joueur lors de sa tentative de panier.
Ce type de tir pouvait prende plus de 70 valeurs différentes - Ce nombre est beaucoup trop important, 
et nous avons procédé en une catégorisation pour aboutir à 4 categories distinctes.

Lors de ces opérations, il est clair que la connaissance "métier" peut s'avérer indispensable.
'''
st.markdown(multi)



st.markdown("# Filtrage des données")
multi = '''

Afin de réduire notre dataset, nous nous sommes concentrés sur les 20 meilleurs joueurs de la NBA.

'''
st.markdown(multi)

top_players = pd.read_csv("data/config/TopPlayers.csv")

st.write(top_players)


st.markdown("# Ajouts de données additionnelles")
multi = '''

Nous avons pensé que le poste du joueur pouvait aider le modèle et nous faire gagner quelques points :-)
Cette donnée a été cuisinée à l'aide de tables externes, et nous avons pu par cela établir quel etait le poste majoritaire d'un joueur pour une année donnée.

Paralellement, la taille et le poids du joueur ont également été ajoutés à nos variables explicatives.
'''
st.markdown(multi)


