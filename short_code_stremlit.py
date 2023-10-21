# Importation data
@st.cache_data
def load_data():
    data = pd.read_csv(
        "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/data/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
    )  # Assurez-vous de spécifier le bon chemin vers votre fichier CSV
    return data


# Charger le DataFrame en utilisant la fonction mise en cache
data = load_data()
# Créer un widget multiselect pour les noms des joueurs
selected_players = st.multiselect(
    "Sélectionnez les joueurs", data["Player Name"].unique()
)

# Filtrer le DataFrame en fonction des joueurs sélectionnés
filtered_data = data[data["Player Name"].isin(selected_players)]

# Afficher les données filtrées avec ajustement automatique des colonnes
st.write("Données des joueurs sélectionnés :")
st.dataframe(
    filtered_data, width=0, height=0
)  # width=0 signifie une largeur automatique
