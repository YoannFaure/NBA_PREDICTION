import streamlit as st
from streamlit_shap import st_shap
import shap
import joblib
import pandas as pd
shap.initjs()

import matplotlib.pyplot as plt


from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import datasets


# Configuration de la page Streamlit
st.set_page_config(
    page_title="Visualisation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.header("INTERPRETABILITÉ DES MODELES")
st.markdown("""---""")

st.write("Cette page nous donne un aperçu de l'interpretabilité des différents modèles sur le jeu de donnné de test")



# Load data
data_split = joblib.load("models/best_player/best_player_split.joblib")
X_train, X_test, y_train, y_test = data_split['X_train'], data_split['X_test'], data_split['y_train'], data_split['y_test']

best_player_adaboost_model = joblib.load("models/best_player/best_player_adaboost_model.joblib")
adaboost_model = best_player_adaboost_model['best_model']

shap_values_logistic_model = joblib.load('models/shap_values/shap_values_logistic_model.joblib')
shap_values_decision_tree_model = joblib.load('models/shap_values/shap_values_decision_tree_model.joblib')
shap_values_gradient_boosting_model = joblib.load('models/shap_values/shap_values_gradient_boosting_model.joblib')
shap_values_lightgbm_model = joblib.load('models/shap_values/shap_values_lightgbm_model.joblib')
shap_values_xgboosting_model = joblib.load('models/shap_values/shap_values_xgboost_model.joblib')
 
 
 

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["LOGISTIC MODEL", "DECISION TREE MODEL", "GRADIENT BOOSTING MODEL", "LIGHT GBM MODEL","XG BOOST MODEL", "ADA BOOST MODEL"])

 
 ########################
#### LOGISTIC MODEL ####
########################

with tab1:
    
    col1, col2 = st.columns([1,3])
    with col1: 
        interpretation = st.select_slider("Choisir un niveau d'interpretation", options=['Global', 'Local'], key="LOGISTIC_MODEL")
        
        if interpretation == 'Local':
            id = st.number_input("Entrez l'ID", min_value=0, max_value=len(shap_values_logistic_model) - 1, step=1, key="LOGISTIC_MODEL_loc")
            st.write(f"Interprétation pour l'ID {id}")
            st.write(f"Valeur de y_test pour l'ID {id} est : {y_test.iloc[id]}")
            
    with col2:                  
        if interpretation == 'Global':
            st_shap(shap.plots.bar(shap_values_logistic_model))
            st_shap(shap.plots.beeswarm(shap_values_logistic_model))
                
        if interpretation == 'Local' and id < len(X_test.index):
            st_shap(shap.plots.waterfall(shap_values_logistic_model[id]))
            st_shap(shap.plots.force(shap_values_logistic_model[id]))


#############################
#### DECISION TREE MODEL ####
#############################
           
with tab2:
    col1, col2 = st.columns([1,3])
    
    with col1: 
        st.write("Intrepretation global")
      
    with col2: 
                  
        st_shap(shap.summary_plot(shap_values_decision_tree_model, X_test))
    

    
#################################
#### GRADIENT BOOSTING MODEL ####
#################################

with tab3:
    col1, col2 = st.columns([1,3])
    
    with col1: 
   
        interpretation = st.select_slider(
            "Choisir un niveau d'interpretation",
            options=['Global', 'Local'], key="GRADIENT BOOSTING MODE")
        
        if interpretation == 'Local':
            id = st.number_input("Entrez l'ID", min_value=0, max_value=len(shap_values_gradient_boosting_model)-1, step=1, key="GRADIENT BOOSTING MODE_loc")
            st.write(f"Interprétation pour l'ID {id}")
            st.write(f"Valeur de y_test pour l'ID {id} est : {y_test.iloc[id]}")

    with col2: 
                  
        if interpretation == 'Global':
            st.image("reports/figures/interpretabilite/gradient_boosting_feature_importance.png")
            st.image("reports/figures/interpretabilite/gradient_boosting_beeswarm_plot.png")

        if interpretation == 'Local':
            st_shap(shap.plots.waterfall(shap_values_gradient_boosting_model[id]))
            st_shap(shap.plots.force(shap_values_gradient_boosting_model[id]))


#########################
#### LIGHT GBM MODEL ####
#########################

with tab4:
    col1, col2 = st.columns([1,3])
    
    with col1: 
   
        interpretation = st.select_slider(
            "Choisir un niveau d'interpretation",
            options=['Global', 'Local'], key="LIGHT GBM MODEL")
        
        if interpretation == 'Local':
            id = st.number_input("Entrez l'ID", min_value=0, max_value=len(shap_values_lightgbm_model)-1, step=1, key="LIGHT GBM MODEL_loc")
            st.write(f"Interprétation pour l'ID {id}")
            st.write(f"Valeur de y_test pour l'ID {id} est : {y_test.iloc[id]}")

    with col2: 
                  
        if interpretation == 'Global':
            st.image("reports/figures/interpretabilite/lightgbm_model_feature_importance.png")
            st.image("reports/figures/interpretabilite/lightgbm_model_beeswarm_plot.png")

            
        if interpretation == 'Local':
            st_shap(shap.plots.waterfall(shap_values_lightgbm_model[id]))
            st_shap(shap.plots.force(shap_values_lightgbm_model[id]))


###########################
#### XG BOOSTING MODEL ####
###########################


with tab5:
    col1, col2 = st.columns([1,3])
    
    with col1: 
   
        interpretation = st.select_slider(
            "Choisir un niveau d'interpretation",
            options=['Global', 'Local'], key="XG BOOSTING MODEL")
        
        if interpretation == 'Local':
            id = st.number_input("Entrez l'ID", min_value=0, max_value=len(shap_values_xgboosting_model)-1, step=1, key="XG BOOSTING MODEL_loc")
            st.write(f"Interprétation pour l'ID {id}")
            st.write(f"Valeur de y_test pour l'ID {id} est : {y_test.iloc[id]}")

    with col2: 
                  
        if interpretation == 'Global':
            st_shap(shap.plots.bar(shap_values_xgboosting_model))
            st_shap(shap.plots.beeswarm(shap_values_xgboosting_model))

            
        if interpretation == 'Local':
            st_shap(shap.plots.waterfall(shap_values_xgboosting_model[id]))
            st_shap(shap.plots.force(shap_values_xgboosting_model[id]))



#########################
#### ADA BOOST MODEL ####
#########################

with tab6:
    col1, col2 = st.columns([1,3])
    
    with col1: 
        st.write("Intrepretation global")
      
    with col2:
           with st.container():
                feature_importance = adaboost_model.feature_importances_
                df_feature_importance = pd.DataFrame({'Feature': X_test.columns, 'Importance': feature_importance})
                df_feature_importance = df_feature_importance.sort_values(by='Importance', ascending=True).tail(10)
                plt.figure(figsize=(10, 6))
                plt.barh(df_feature_importance['Feature'], df_feature_importance['Importance'])
                plt.xlabel('Importance')
                plt.tight_layout()

                # Afficher le graphique dans Streamlit
                st.pyplot(plt)    