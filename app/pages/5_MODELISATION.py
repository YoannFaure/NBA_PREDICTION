import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Modelisation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

st.header("Modelisation")
st.sidebar.header("Modelisation")
st.markdown("""---""")

multi = '''

## Approche

L'approche que nous avons retenu est de construire une "Super-GridSearchCV".  L'idée est d'en fait de s'appuyer sur la GridSearchCV standard, mais de l'utiliser sur 6 différents modeles, et sur un nombre de hyper-parametres assez conséquent.
Nous savions que le choix des hyperparametres est à la fois difficile, mais il peut être determinant !

Il a fallu pas moins de 50 minutes, sur une machine assez puissante pour effectuer ces 6 GridSearchCV.
Une fois ces opérations effecutées, nous avons conservés le résultat de ces opérations, et nous sommes concentrés sur les hyper-parametres fournissant le meilleur score pour chaque model.
'''

st.markdown(multi)

ListModels = []

ListModels.append( {
                    "name" :'logistic_model',
                    "params" : {
                        'penalty': ['l1', 'l2'],
                        'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                        'solver': ['liblinear', 'saga'] }})

ListModels.append({
                    "name" : 'decision_tree_model',
                    "params" : {
                        'splitter': ['best', 'random'],
                        'max_depth': [None, 10, 20, 30, 40, 50],
                        'min_samples_split': [2, 5, 10],
                        'min_samples_leaf': [1, 2, 4] }})

ListModels.append({
                    "name" : 'gradient_boosting_model',
                    "params" : {
                        'n_estimators': [100, 200],
                        'max_depth': [3, 4],
                        'subsample': [0.5, 0.6],
                        'learning_rate': [0.02, 0.03] }})

ListModels.append({
                    "name" : 'xgboost_model',
                    "params" : {
                        'n_estimators': [100, 200],
                        'max_depth': [3, 4],
                        'subsample': [0.5, 0.6],
                        'learning_rate': [0.02, 0.03],
                        'gamma': [0.1, 0.2],
                        'colsample_bytree': [0.5, 0.6] }})

ListModels.append({
                    "name" : 'adaboost_model',
                    "params" : {
                        'n_estimators': [50, 100, 150],
                        'learning_rate': [0.01, 0.1, 0.2],
                        'algorithm': ['SAMME', 'SAMME.R']}})


ListModels.append({
                    "name" : 'lightgbm_model',
                    "params" : {
                        'n_estimators': [100, 200],
                        'max_depth': [3, 4],
                        'learning_rate': [0.02, 0.03],
                        'subsample': [0.5, 0.6],
                        'objective': ['binary'],
                        'metric': ['binary_error']}})

ListModels_df = pd.DataFrame(ListModels)
st.dataframe(ListModels_df)

multi = ''' ## Metric

En terme de metric à optimiser, notre choix dans le cadre de ce projet s'est porté sur l' **Accuracy**
En effet, notre focus est de maximiser le taux de prédiction portant sur la réussite du panier pour un tir donné.
Les **Faux Négatifs**, ou **Faux Positifs** sont juste ici de mauvaises prédictions sans autre sématique particuliere.

On rappele que l'accuracy est calculé comme suit :
'''

st.markdown(multi)

st.latex(r'Accuracy = \frac{Nombre\ de\ prédictions\ correctes}{Nombre\ total\ de\ prédictions}')
