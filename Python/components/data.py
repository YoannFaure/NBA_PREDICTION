import pandas as pd

nba_shot_location = pd.read_csv(
    "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/data/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
)


def afficher_informations(df):
    # Affichage df
    print("Affichage df")
    print(df.head())

    # Affichage info
    print("\nAffichage info")
    print(df.info())

    # Affichage null
    print("\nAffichage null")
    print(df.isnull().sum())

    # Affichage valeurs uniques
    print("\nAffichage valeurs uniques")
    print(df.nunique())
