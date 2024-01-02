import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import json
import random
import datetime
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


target_names = ['Panier Manqué', 'Panier Réussi']

def seconds_to_hms(seconds):
    return str(datetime.timedelta(seconds=seconds))



st.set_page_config(
    page_title="Machine Learning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

st.header("Machine Learning")
st.sidebar.header("Machine Learning")
st.markdown("""---""")

directory = "models/best_player/"

ListModels = []
ListModels_dp = []


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f.endswith("model.joblib"):
        model_data = joblib.load(f)

        modeldef = {
            "Name": model_data['name'],
            "Meilleurs paramètres": model_data['best_params'],
            "Temps de recherche des hyperparametres": model_data['execution_time_search_params'],
            "Temps d'exécution de l'entraînement": model_data['execution_time_training'],
            "Matrice de confusion": model_data['confusion_matrix'],
            "Rapport de classification": model_data['classification_report'],
            "Accuracy": model_data['accuracy'],
            "Precision": model_data['precision'],
            'Recall': model_data['recall'],
            'F1_Score': model_data['f1_score'],
            'Auc': model_data['auc'],
            'best_model': model_data['best_model'],
        }

        modeldef_dp = {
            "Name": model_data['name'],
            "Meilleurs paramètres": json.dumps(model_data['best_params']),
            "Temps de recherche des hyperparametres": seconds_to_hms(model_data['execution_time_search_params']) ,
            "Temps d'exécution de l'entraînement": seconds_to_hms(model_data['execution_time_training']),
            "Accuracy": model_data['accuracy'],
            "Precision": model_data['precision'],
            'Recall': model_data['recall'],
        }
        ListModels.append(modeldef)
        ListModels_dp.append(modeldef_dp)

def get_model_from_name(name):
    return next(model for model in ListModels if model["Name"] == name)


def add_linebreaks(s):
    return s.replace('\n', '<br>')

df = pd.DataFrame(ListModels_dp)

multi = '''### Accuracy

En terme d' accuracy, nos modeles arrivent à des résultats très similaires, somme toute assez decevants'
'''

st.markdown(multi)

# ceci ne fonctionne pas comme prevu
styled_df = df.style.applymap(add_linebreaks, subset=['Meilleurs paramètres'])

st.write(styled_df, unsafe_allow_html=True)



# Affichage de 2 modèles en Side by Side

st.markdown("### Matrice de confusion")

list_of_names = [model["Name"] for model in ListModels]

title = 'Confusion Matrix'
col1, col2 = st.columns(2)
with col1:
    fig1, ax = plt.subplots()
    selected_modelname_col1 = st.selectbox("Sélectionnez un modèle", list_of_names, key='modele_res_col1')
    selected_model_col1 = get_model_from_name(selected_modelname_col1)
    st.json(selected_model_col1['Meilleurs paramètres'])
    cm = selected_model_col1['Matrice de confusion']
    heatmap_1 = sns.heatmap(cm, annot=True, fmt="d", cmap='Blues', cbar=False, ax=ax)

    ax.set_xlabel('Prédiction')
    ax.set_ylabel('Réalité')
    ax.set_title(title)
    st.write(fig1)

with col2:
    fig2, ax = plt.subplots()
    selected_modelname_col2 = st.selectbox("Sélectionnez un modèle", list_of_names, key='modele_res_col2')
    selected_model_col2 = get_model_from_name(selected_modelname_col2)
    st.json(selected_model_col2['Meilleurs paramètres'])
    cm = selected_model_col2['Matrice de confusion']
    heatmap_2 = sns.heatmap(cm, annot=True, fmt="d", cmap='Blues', cbar=False, ax=ax)

    ax.set_xlabel('Prediction')
    ax.set_ylabel('Réalité')
    ax.set_title(title)

    st.write(fig2)



st.markdown("### Démonstration / Prédiction")



start_value = 1
end_value = 50

EventCount = st.number_input(
    "Sélectionnez un nombre d'événements compris entre {} et {}".format(start_value, end_value),
    min_value=start_value,
    max_value=end_value,
    step=5,
    value=10
)

selected_model_demo = st.selectbox("Sélectionnez un de nos modèles entrainés", list_of_names, key='modele_demo')



data = pd.read_csv("data/processed/best_player_preprocessed.csv")
features = data.drop('SHOT_MADE_FLAG', axis=1)
target = data['SHOT_MADE_FLAG']




def highlight_target_col(s):
    return ['background-color: lightblue' if (s.name == 'SHOT_MADE_FLAG') or (s.name == 'SHOT_MADE_FLAG_PREDICT')  else '' for _ in s]


def DoPredictions():
    with st.spinner('Predicting...'):

        # selection de X lignes au hasard
        options = list(range(0, len(data)))
        selected_lines = random.sample(options, EventCount)
        selected_features = features.iloc[selected_lines]

        SampleDF = data.iloc[selected_lines]

        selected_model = get_model_from_name(selected_model_demo)


        SampleDF['SHOT_MADE_FLAG_PREDICT'] = (selected_model['best_model']).predict(selected_features)

        cols = ['SHOT_MADE_FLAG', 'SHOT_MADE_FLAG_PREDICT'] + [col for col in SampleDF.columns if col not in ['SHOT_MADE_FLAG', 'SHOT_MADE_FLAG_PREDICT']]
        SampleDF = SampleDF.reindex(columns=cols)

        st.dataframe(SampleDF.style.apply(highlight_target_col))

        accuracy = accuracy_score(SampleDF['SHOT_MADE_FLAG'], SampleDF['SHOT_MADE_FLAG_PREDICT'])

        st.write("accuracy =", accuracy )

        cm = confusion_matrix(SampleDF['SHOT_MADE_FLAG'], SampleDF['SHOT_MADE_FLAG_PREDICT'])
        st.write(pd.DataFrame(cm))

        report = classification_report(SampleDF['SHOT_MADE_FLAG'], SampleDF['SHOT_MADE_FLAG_PREDICT'], target_names=target_names, output_dict=True)
        st.write(pd.DataFrame(report).transpose())

    st.success('Prediction completed!')




if st.button("Predict"):
    DoPredictions()






