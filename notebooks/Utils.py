import time
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score



class modelDefinition:
    def __init__(this, name, params, estimator):
        this.name = name
        this.params = params
        this.estimator = estimator

class megaGridSearch:
    def __init__(this, name, features, target, test_size=0.2):
        this.Models = []
        this.name = name
        # Division des matrices pour l'ensemble de données complet
        this.X_train, this.X_test, this.y_train, this.y_test = train_test_split(features, target, test_size=test_size, stratify = target)

        # Save the training and testing data
        data_split = {
            'X_train': this.X_train,
            'X_test': this.X_test,
            'y_train': this.y_train,
            'y_test': this.y_test
        }

        file_path = f"../models/{this.name}/{this.name}_split.joblib"

        # create directory
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        joblib.dump(data_split, file_path)

    def AddModel(this, model):
        this.Models.append(model)

    def run(this):
        for model in this.Models:
            model_data = train_model(model.estimator, model.params, this.X_train, this.y_train, this.X_test, this.y_test, model.name)            
            joblib.dump(model_data, f"../models/{this.name}/{this.name}_{model.name}.joblib")


# Créer une fonction d'entrainement de model
def train_model(model, param_grid, X_train, y_train, X_test, y_test, model_name):
    start_time_search_params = time.time()
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    end_time_search_params = time.time()
    execution_time_search_params = end_time_search_params - start_time_search_params

    best_model = model.set_params(**best_params)
    start_time_training = time.time()
    best_model.fit(X_train, y_train)
    end_time_training = time.time()
    execution_time_training = end_time_training - start_time_training

    y_pred = best_model.predict(X_test)

    model_data = {
        'name': model_name,
        'best_params': best_params,
        'best_model': best_model,
        'y_pred': y_pred,
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred),
        'execution_time_search_params': execution_time_search_params,
        'execution_time_training': execution_time_training,
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'auc': roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
    }

    return model_data


