from __future__ import absolute_import

# Standard library imports
import json
import pandas as pd

# Third party imports
from celery import states

# Local application imports
from modules.software_quality.projects.combining_data import extra_features
from taskqueue.celery.config import celery
from database.anita.controller.SonarqubeController import SonarqubeController
from modules.software_quality.experimentation.algorithm import *
from modules.software_quality.experimentation.preprocessing import *

# Task ID
EVALUATION_TASK_ID = "3"
PREDICTION_TASK_ID = "4"


@celery.task(bind=True)
def evaluation_task(self, project_name=None):
    # Response content
    content = train_content_template()
    self.update_state(state='PROGRESS', meta=content)

    # Load data
    sq_controller = SonarqubeController()
    if project_name is None:
        sq_models = sq_controller.select_all_labelled()
    else:
        tmp_sq_models = sq_controller.select_by_project_name(project_name)
        sq_models = [model for model in tmp_sq_models if model["label"] is not None]
    dict_models = json.dumps(sq_models)
    project_dataframe = pd.DataFrame.from_dict(dict_models, orient='index')

    for i in range(2):
        df_copy = project_dataframe.copy()

        if i == 0:  # 3 classes
            key = "Train - 3 classes"
            df_copy["label"] = df_copy["label"].apply(three_classifiers)
        else:       # 26 classes
            key = "Train - 26 classes"
            df_copy["label"] = df_copy["label"].apply(three_classifiers)

        print("DATAFRAME")
        print(df_copy.values)

        # Preprocessing
        df_copy = preprocessing(df_copy, scaling=True)
        label_map = label_encoder(df_copy)

        y = df_copy["label"]
        del df_copy["label"]
        X = df_copy

        best_features = feature_selection(X, y)
        X = df_copy[best_features]

        # Train - Test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        X_train, y_train = oversampling(X_train, y_train)

        y_pred_knn, best_model = knn(X_train, y_train, X_test)
        content[key]["knn"] = evaluate(y_test, y_pred_knn, label_map)
        self.update_state(state='PROGRESS', meta=content)

        y_pred_rf, best_model = random_forest(X_train, y_train, X_test)
        content[key]["Random forest"] = evaluate(y_test, y_pred_rf, label_map)
        self.update_state(state='PROGRESS', meta=content)

        y_pred_lr, best_model = logistic_regression(X_train, y_train, X_test)
        content[key]["Logistic regression"] = evaluate(y_test, y_pred_lr, label_map)
        self.update_state(state='PROGRESS', meta=content)

        y_pred_svc, best_model = svc(X_train, y_train, X_test)
        content[key]["SVC"] = evaluate(y_test, y_pred_svc, label_map)
        self.update_state(state='PROGRESS', meta=content)

    self.update_state(state=states.SUCCESS, meta=content)
    return content


def train_content_template():
    return {
        "Train - 3 classes": {
            "knn": None,
            "Random forest": None,
            "Logistic regression": None,
            "SVC": None
        },
        "Train - 26 classes": {
            "knn": None,
            "random forest": None,
            "Logistic regression": None,
            "SVC": None
        }
    }


@celery.task(bind=True)
def prediction_task(self, project_name, algorithm, save):
    content = {}
    self.update_state(state=states.STARTED, meta=content)

    algorithm_list = ["knn", "random_forest", "logistic_regression", "csv"]
    if algorithm not in algorithm_list:
        content = {"error": "algorithm undefined"}
        self.update_state(state=states.FAILURE, meta=content)
        return content

    sq_controller = SonarqubeController()
    sq_models_labelled = sq_controller.select_all_labelled()
    sq_models = sq_controller.select_by_project_name(project_name)

    # Check if the prediction has already done
    null_labels = False
    for sq_model in sq_models:
        if sq_model["label"] is None:
            null_labels = True
            break

    # Project already processed
    if null_labels is False:
        self.update_state(state=states.SUCCESS, meta=sq_models)
        return sq_models

    self.update_state(state='PROGRESS', meta=content)

    dict_models = json.dumps(sq_models)
    test_dataframe = pd.DataFrame.from_dict(dict_models, orient='index')

    dict_train = json.dumps(sq_models_labelled)
    train_dataframe = pd.DataFrame.from_dict(dict_train, orient='index')

    for i in range(2):
        train_copy = train_dataframe.copy()
        test_copy = test_dataframe.copy()

        if i == 0:  # 3 classes
            key = "Train - 3 classes"
            train_copy["label"] = train_copy["label"].apply(three_classifiers)
        else:  # 26 classes
            key = "Train - 26 classes"
            train_copy["label"] = train_copy["label"].apply(three_classifiers)

        # Preprocessing
        train_copy = preprocessing(train_copy)
        test_copy = preprocessing(test_copy)
        label_map = label_encoder(train_copy)

        y_train = train_copy["label"]

        del train_copy["label"]
        X_train = train_copy

        best_features = feature_selection(X_train, y_train)
        X_train = train_copy[best_features]
        X_test = test_copy[best_features]

        # Oversampling
        X_train, y_train = oversampling(X_train, y_train)

        if algorithm == "knn":
            y_pred, best_model = knn(X_train, y_train, X_test)
        elif algorithm == "random forest":
            y_pred, best_model = random_forest(X_train, y_train, X_test)
        elif algorithm == "logistic regression":
            y_pred, best_model = logistic_regression(X_train, y_train, X_test)
        else:
            y_pred, best_model = svc(X_train, y_train, X_test)

        final_df = test_dataframe.copy()
        final_df["label"] = label_decoder(label_map, y_pred)
        content[key] = json_dataframe(final_df)
        self.update_state(state='PROGRESS', meta=content)

    if save:
        labels_dict = []
        for row in final_df["Train - 26 classes"]:
            label_dict = {row["page"]: row["label"]}
            labels_dict.append(label_dict)

        sq_controller.add_labels(project_name, labels_dict)

    self.update_state(state=states.SUCCESS, meta=content)
    return content


def json_dataframe(df):
    json_dataframe = []

    header = df.columns.values.tolist()
    for index, columns in df.iterrows():
        elem = {}
        for i in range(len(columns)):
            elem[header[i]] = columns[i]
        json_dataframe.append(elem)

    return json_dataframe
