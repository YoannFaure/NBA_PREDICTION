import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

## Initalisation de la page ## 

st.set_page_config(
    page_title="Visualisation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

## LOAD DATA ##

@st.cache_data
def load_data():
    df = pd.read_csv("data/preprocessed/best_player.csv")
    return df

df = load_data()


## BODY ##

##################### STATISTIQUE DU DATASET #####################

st.header("STATISTIQUES DES 20 MEILLEURS JOUEURS DE NBA")
st.markdown("""---""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"##### ⛹️ {len(df['PLAYER_NAME'].unique())} JOUEURS")
with col2:
    st.markdown(f"##### 📆 {len(df['GAME_ID'].unique())} MATCH UNIQUES")
with col3:
    st.markdown(f"##### 🏀 {df.shape[0]} SHOTS")
with col4:
    st.markdown(f"##### 🗑️ {sum(df['SHOT_MADE_FLAG'] == 1)} RÉUSSIS / {sum(df['SHOT_MADE_FLAG'] == 0)} LOUPÉS")
st.markdown("""---""")

##################### DATA VISUALISATION #####################

tab1, tab2, tab3, tab4 = st.tabs(["SUCCÈS DES TIRS", "SUCCÈS PAR CATÉGORIE ", "SUCCÈS PAR ZONE", "SUCCES / TEMPS RESTANT"])

# SUCCÈS DES TIRS # 
with tab1:
    col5, col6 = st.columns([1,3])
    
    with col5:
        # Ajout de la colonne 'Total' pour le tableau
        # Filtrer les données pour les tirs réussis et manqués
        made_shots = df[df['SHOT_MADE_FLAG'] == 1]
        missed_shots = df[df['SHOT_MADE_FLAG'] == 0]

        # Compter le nombre de tirs réussis et manqués par joueur
        made_counts = made_shots['PLAYER_NAME'].value_counts()
        missed_counts = missed_shots['PLAYER_NAME'].value_counts()

        # Créer un DataFrame avec le total des tirs réussis et manqués par joueur
        shots_df = pd.DataFrame({'Player': made_counts.index, 'Made': made_counts.values, 'Missed': missed_counts.values})

        # Calculer le total de tirs (réussis + manqués) par joueur
        shots_df['Total'] = shots_df['Made'] + shots_df['Missed']  # Calcul du total

        # Trier les joueurs par nombre total de tirs
        shots_df = shots_df.sort_values(by='Total', ascending=True)
            
        shots_df['Total'] = shots_df['Made'] + shots_df['Missed']
        st.table(shots_df[['Player', 'Made', 'Missed', 'Total']].sort_values(by='Total', ascending=False))

    
    with col6:
        def shot_made_player_bar(df):
        
            # Création de la figure
            fig = go.Figure() 

            # Ajout des traces de barres pour les SHOT_MADE_FLAG par joueur
            fig.add_trace(
                go.Bar(
                    y=shots_df['Player'],  # Les joueurs
                    x=shots_df['Made'],  # Nombre de tirs réussis
                    name='MADE',
                    orientation='h',  # Orientation horizontale pour inverser les axes
                    marker_color='#17408B',
                    text = ((shots_df['Made'] / (shots_df['Made'] + shots_df['Missed'])) * 100).round(2),
                    hoverinfo='x+text',  # Informations supplémentaires au survol
                    marker=dict(line=dict(color='rgba(0,0,0,0)'))  # Supprime le contour blanc
                )
            )

            fig.add_trace(
                go.Bar(
                    y=shots_df['Player'],  # Les joueurs
                    x=shots_df['Missed'],  # Nombre de tirs manqués
                    name='MISSED',
                    orientation='h',  # Orientation horizontale pour inverser les axes
                    marker_color='#C9082A',
                    text = ((shots_df['Missed'] / (shots_df['Made'] + shots_df['Missed'])) * 100).round(2),
                    hoverinfo='x+text',  # Informations supplémentaires au survol
                    marker=dict(line=dict(color='rgba(0,0,0,0)'))
                )
            )
            
             # Mise en forme du texte pour afficher les pourcentages dans le graphique
            for annotation in fig.layout.annotations:
                annotation.text = f"{round(float(annotation.text), 2)}%"

            # Mise en forme du titre et des axes
            fig.update_layout(
                yaxis_title='Joueur',
                xaxis_title='Nombre de tir',
                barmode='stack',
                height=700
            )
            
            return fig, shots_df

        fig, shots_df = shot_made_player_bar(df)  # Réassigner les valeurs retournées par la fonction
        st.plotly_chart(fig, use_container_width=True)
    

# SUCCÈS PAR CATÉGORIE # 
with tab2: 
    
    categories = [
        'SHOT_ACTION_CATEGORY_DUNK',
        'SHOT_ACTION_CATEGORY_LAYUP',
        'SHOT_ACTION_CATEGORY_SHOOT',
        'SHOT_ACTION_CATEGORY_OTHER'
    ]
    
    aggregated_cat = {'SHOT_ACTION_CATEGORY': [], 'MADE': [], 'MISSED': [], 'TOTAL': []}
    
    
    col7, col8 = st.columns([1,3])
    
    with col7:
        # Récupérer la liste des noms de joueurs uniques et les trier
        player_names = sorted(df['PLAYER_NAME'].unique())

        # Checkbox pour sélectionner tous les joueurs
        df_cat = df
        on = st.toggle('Selectionner un joueur', key = "action_category_1")
        if on:
            selected_player = st.selectbox('Sélectionnez un joueur', player_names, key = "action_category_2")
            
            # Filtrer le DataFrame initial par le joueur sélectionné
            df_cat = df_cat[df_cat['PLAYER_NAME'] == selected_player]

        # Pour chaque catégorie de tir
        for category in categories:
            # Compter les tirs réussis et manqués
            made_count = df_cat[df_cat[category] == 1]['SHOT_MADE_FLAG'].sum()
            missed_count = len(df_cat[(df_cat[category] == 1) & (df_cat['SHOT_MADE_FLAG'] == 0)])

            # Calculer le total
            total_count = made_count + missed_count

            # Ajouter les données agrégées au dictionnaire
            aggregated_cat['SHOT_ACTION_CATEGORY'].append(category.split('_')[-1])
            aggregated_cat['MADE'].append(made_count)
            aggregated_cat['MISSED'].append(missed_count)
            aggregated_cat['TOTAL'].append(total_count)

        # Créer un DataFrame à partir du dictionnaire
        aggregated_df = pd.DataFrame(aggregated_cat)
        st.dataframe(aggregated_df.sort_values(by='TOTAL', ascending=False), hide_index=True)

    with col8:

        # Création d'un DataFrame pour stocker les données agrégées
        aggregated_data = {
            "SHOT_ACTION_CATEGORY": [],
            "TYPE": [],
            "COUNT": []
        }

        # Pour chaque catégorie de tir
        for category in categories:
            # Compter les tirs réussis et manqués
            made_count = df_cat[df_cat[category] == 1]["SHOT_MADE_FLAG"].sum()
            missed_count = len(df_cat[(df_cat[category] == 1) & (df_cat["SHOT_MADE_FLAG"] == 0)])

            # Ajouter les données agrégées au dictionnaire pour le succès
            aggregated_data["SHOT_ACTION_CATEGORY"].append(category.split("_")[-1])
            aggregated_data["TYPE"].append("MADE")
            aggregated_data["COUNT"].append(made_count)

            # Ajouter les données agrégées au dictionnaire pour les ratés
            aggregated_data["SHOT_ACTION_CATEGORY"].append(category.split("_")[-1])
            aggregated_data["TYPE"].append("MISSED")
            aggregated_data["COUNT"].append(missed_count)

        # Créer un DataFrame à partir du dictionnaire
        aggregated_df = pd.DataFrame(aggregated_data)
        
        # Créer un dictionnaire de correspondance des couleurs pour les catégories 'TYPE'
        color_map = {'SHOT_ACTION_CATEGORY': 'black', 'MISSED': '#C9082A', 'MADE': '#17408B'}

        # Create the Sunburst object with specific colors for 'TYPE'
        sunburst = px.sunburst(
            aggregated_df,
            path=['SHOT_ACTION_CATEGORY', 'TYPE'],
            values='COUNT',
            color='TYPE',  # Coloration basée sur la catégorie 'TYPE'
            color_discrete_map=color_map,  # Associe les couleurs spécifiques aux catégories 'MISSED' et 'MADE'
            branchvalues='total'  # Utilisation des valeurs totales pour les branches
        )

        # Mettre à jour le style des marqueurs (bordure et lignes)
        sunburst.update_traces(marker=dict(line=dict(color='white', width=1)), textinfo='label+percent entry')

        # Mettre à jour la taille du graphique
        sunburst.update_layout(width=600, height=600)

        # Afficher le graphique Sunburst
        st.plotly_chart(sunburst, use_container_width=True)

    
# SUCCÈS PAR ZONE # 
with tab3:
    
    col9, col10 = st.columns([1,3])
    
    with col9:
    
        # Récupérer la liste des noms de joueurs uniques et les trier
        player_names = sorted(df['PLAYER_NAME'].unique())
        df_zone = df

        # Checkbox pour sélectionner tous les joueurs
        
        on = st.toggle('Selectionner un joueur', key = "zone_category_1" )
        if on:
            selected_player = st.selectbox('Sélectionnez un joueur', player_names, key = "zone_category_2")
            
            # Filtrer le DataFrame initial par le joueur sélectionné
            df_zone = df_zone[df_zone['PLAYER_NAME'] == selected_player]

        
        selected_graph = st.selectbox("Sélectionner un graphique", ['SHOT TYPE', 'SHOT ZONE BASIC', 'SHOT ZONE AREA', 'SHOT ZONE RANGE'])

    with col10:

        def display_sunburst(df_zone, category):
            # Créer un DataFrame agrégé pour la catégorie spécifiée
            aggregated_data = df_zone.groupby([category, 'SHOT_MADE_FLAG']).size().reset_index(name='COUNT')
            aggregated_data['SHOT_MADE_FLAG'] = aggregated_data['SHOT_MADE_FLAG'].replace({1: 'MADE', 0: 'MISSED'})

            # Définir la couleur pour le premier niveau et pour 'MADE' et 'MISSED'
            color_map = {category: 'black', 'MISSED': '#C9082A', 'MADE': '#17408B'}

            # Créer le Sunburst pour la catégorie spécifiée
            fig = px.sunburst(
                aggregated_data,
                path=[category, 'SHOT_MADE_FLAG'],
                values='COUNT',
                color='SHOT_MADE_FLAG',
                color_discrete_map=color_map
            )

            # Ajouter une bordure blanche
            fig.update_traces(
                marker=dict(line=dict(color='white', width=1)),
                insidetextfont=dict(color='white'),
                textinfo='label+percent entry'
            )
            
            fig.update_layout(width=600, height=600)
            
            return fig

  
        if selected_graph == 'SHOT TYPE':
            fig1 = display_sunburst(df_zone, 'SHOT_TYPE')
            st.plotly_chart(fig1, use_container_width=True)
            
     
        elif selected_graph == 'SHOT ZONE BASIC':
            fig2 = display_sunburst(df_zone, 'SHOT_ZONE_BASIC')
            st.plotly_chart(fig2, use_container_width=True)
            
        elif selected_graph == 'SHOT ZONE AREA':
            fig3 = display_sunburst(df_zone, 'SHOT_ZONE_AREA')
            st.plotly_chart(fig3, use_container_width=True)

        elif selected_graph == 'SHOT ZONE RANGE':
            fig1 = display_sunburst(df_zone, 'SHOT_ZONE_RANGE')
            st.plotly_chart(fig1, use_container_width=True)
            

# SUCCES / TEMPS RESTANT # 
with tab4:
    
    col11, col12 = st.columns([1,3])
    
    with col11:
    
        # Récupérer la liste des noms de joueurs uniques et les trier
        player_names = sorted(df['PLAYER_NAME'].unique())
        df_time = df

        # Checkbox pour sélectionner tous les joueurs
        
        on = st.toggle('Selectionner un joueur', key = "time_1" )
        if on:
            selected_player = st.selectbox('Sélectionnez un joueur', player_names, key = "time_2")
            
            # Filtrer le DataFrame initial par le joueur sélectionné
            df_time = df_zone[df_zone['PLAYER_NAME'] == selected_player]
                    
        selected_periode = st.slider('Sélectionnez une période de jeu', min_value=1, max_value=4, value=1)
        df_time = df_time[(df_time['GAME_PERIOD'] == selected_periode)]

    with col12:        
        
        df_time = df_time[['PLAYER_NAME', 'GAME_PERIODE_SECOND_REMAINGING', 'SHOT_MADE_FLAG']]
        df_time['GAME_PERIODE_MINUTE_REMAINGING'] = df_time['GAME_PERIODE_SECOND_REMAINGING'] // 60
        df_time = df_time.drop(['GAME_PERIODE_SECOND_REMAINGING'], axis=1)

        # Grouper les données pour obtenir le nombre de tirs réussis et manqués par minute
        shots_time_remaining = df_time.groupby(['PLAYER_NAME', 'GAME_PERIODE_MINUTE_REMAINGING', 'SHOT_MADE_FLAG']).size().unstack(fill_value=0)
        shots_time_remaining.columns = ['MISSED', 'MADE']
        shots_time_remaining.reset_index(inplace=True)
        
        # Décaler les minutes de 1
        # shots_time_remaining_minute['GAME_PERIODE_MINUTE_REMAINGING'] += 1

        fig = px.bar(shots_time_remaining, 
                    x='GAME_PERIODE_MINUTE_REMAINGING', 
                    y=['MISSED', 'MADE'], 
                    barmode='group',
                    color_discrete_map={'MISSED': '#C9082A', 'MADE': '#17408B'},
                    labels={'value': 'Count', 'variable': 'Type', 'GAME_PERIODE_MINUTE_REMAINGING': 'Minute'}
                    )

        fig.update_layout(xaxis_title='Minutes restantes',
                          yaxis_title='Nombre de tirs'
                          )
        
        fig.update_xaxes(autorange="reversed")


        # Afficher la figure
        st.plotly_chart(fig, use_container_width=True)


##################### PLAYER VIZ #####################

st.markdown("""---""")
st.header("PLAYER STAT")

# Récupérer la liste des noms de joueurs uniques et les trier
player_names = sorted(df['PLAYER_NAME'].unique())

# Sélectionner automatiquement le premier joueur par défaut
default_player = player_names[0] if player_names else None

# Sélection multiselect avec les noms triés par ordre alphabétique et le premier joueur sélectionné par défaut
selected_player = st.selectbox('Sélectionnez un joueur', player_names, index=player_names.index(default_player) if default_player else 0)


# Filtrer le DataFrame initial par le joueur sélectionné
filtered_df = df[df['PLAYER_NAME'] == selected_player]

col1, col2 = st.columns(2)
with col1:
    
        game_years = sorted(filtered_df['GAME_YEAR'].unique())
        default_year = game_years[0] if game_years else None
        selected_year = st.slider('Sélectionnez une année de jeu', min_value=min(game_years), max_value=max(game_years), value=default_year)
        filtered_df = filtered_df[(filtered_df['GAME_YEAR'] == selected_year)]
        
        selected_player_info = filtered_df.iloc[0]  # Sélectionner le premier joueur pour afficher ses informations
        st.metric("Equipe ", selected_player_info['GAME_TEAM_NAME'])
        col3, col4, col5, col6, col7 = st.columns(5)
        col3.metric("Poste", selected_player_info['PLAYER_POS'])
        col4.metric("Age", str(selected_player_info['PLAYER_GAME_AGE']))  # Convertir en chaîne de texte pour affichage
        col5.metric("Naissance ", str(selected_player_info['PLAYER_BORN_YEAR']))
        col6.metric("Taille ", str(selected_player_info['PLAYER_HEIGHT']))
        col7.metric("Poids ", str(selected_player_info['PLAYER_WEIGHT']))
        
        # Filtre année et season type pour le graphique        
        st.write("Selectionner une saison")
        
        col8, col9 = st.columns(2)
        with col8: 
            season_type_regular = st.checkbox('Saison régulière', value=True)
        
        with col9:     
            season_type_playoffs = st.checkbox('Playoffs', value=True)

        selected_season_types = []
        if season_type_regular:
            selected_season_types.append('Regular Season')
        if season_type_playoffs:
            selected_season_types.append('Playoffs')

        # Filtrer le DataFrame par les types de saison sélectionnés
        filtered_df = filtered_df[filtered_df['GAME_SEASON_TYPE'].isin(selected_season_types)]

    
with col2:

    ###################### DRAW PLAYER SHOT CHART ######################

    #################### Draw Court #####################


    def add_court_shapes(fig):
        """Adds a basketball court to a Plotly graph.

        Args:
        fig: A Plotly graph object.

        Returns:
        A Plotly graph object with the basketball court added.
        """

        # Cercle 1
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=-3,
            y0=-3,
            x1=3,
            y1=3,
            line=dict(color="Grey", width=1),
        )

        # Cercle 2
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=-60,
            y0=77,
            x1=60,
            y1=197,
            line=dict(color="Grey", width=1),
        )

        # Cercle center
        fig.add_shape(
            type="circle",
            xref="x",
            yref="y",
            x0=-60,
            y0=357,
            x1=60,
            y1=477,
            line=dict(color="Grey", width=1),
        )

        # Backboard
        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=-30,
            y0=-7.5,
            x1=30,
            y1=-7.5,
            line=dict(color="Grey", width=1),
        )

        # Court width=50ft, height=47ft
        fig.add_shape(
            type="rect",
            x0=-250,
            y0=-53,
            x1=250,
            y1=417,
            line=dict(color="Grey", width=1),
        )

        # intern width=16ft, height=19ft
        fig.add_shape(
            type="rect",
            x0=-80,
            y0=-53,
            x1=80,
            y1=137,
            line=dict(color="Grey", width=1),
        )

        # Add the 3-point line
        fig.add_shape(
            type="path", path="M-220, 87 Q 0,390 220,87", line=dict(color="Grey", width=1)
        )

        fig.add_shape(
            type="path", path="M -40,0 Q 0,40 40,0", line=dict(color="Grey", width=1)
        )

        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=-220,
            y0=-53,
            x1=-220,
            y1=87,
            line=dict(color="Grey", width=1),
        )

        fig.add_shape(
            type="line",
            xref="x",
            yref="y",
            x0=220,
            y0=-53,
            x1=220,
            y1=87,
            line=dict(color="Grey", width=1),
        )
        fig.update_layout(
            width=635,  # Largeur en pixels
            height=800,  # Hauteur en pixels
            xaxis_range=[-300, 300],  # Ajustez les limites de l'axe X
            yaxis_range=[-100, 500],  # Ajustez les limites de l'axe Y
            showlegend=False,  # Masquez la légende
            xaxis_fixedrange=True,  # Désactive le zoom sur l'axe X
            yaxis_fixedrange=True,  # Désactive le zoom sur l'axe Y
            xaxis_autorange=False,  # Désactive l'autoscale sur l'axe X
            yaxis_autorange=False,  # Désactive l'autoscale sur l'axe Y
        )
        # Supprimez les lignes des axes
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        # Supprimez les valeurs des axes
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        # Supprimez la légende
        fig.update_layout(showlegend=False)
        # Inversez les valeurs y de la figure
        fig.update_yaxes(autorange=False, range=[500, -100])


    fig = go.Figure()
    add_court_shapes(fig)


    #################### PLAYER SHOT LOCATION #####################

    fig = go.Figure()
    add_court_shapes(fig)
    fig.add_trace(
        go.Scatter(
            x=filtered_df[filtered_df["SHOT_MADE_FLAG"] == 1]["SHOT_X_LOCATION"],
            y=filtered_df[filtered_df["SHOT_MADE_FLAG"] == 1]["SHOT_Y_LOCATION"],
            mode="markers",
            marker=dict(color="#17408B", size=5),
            hoverinfo="text",
            showlegend=True,
            name="Made Shots",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_df[filtered_df["SHOT_MADE_FLAG"] == 0]["SHOT_X_LOCATION"],
            y=filtered_df[filtered_df["SHOT_MADE_FLAG"] == 0]["SHOT_Y_LOCATION"],
            mode="markers",
            marker=dict(color="#C9082A", size=5),
            hoverinfo="text",
            showlegend=True,
            name="Missed Shots",
        )
    )

    st.plotly_chart(fig)
