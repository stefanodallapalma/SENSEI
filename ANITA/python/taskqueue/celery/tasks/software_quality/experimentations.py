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
from database.anita.decoder.sonarqube_decoder import SonarqubeDBDecoder
from database.anita.model.SonarqubeBean import SonarqubeBean
from modules.software_quality.experimentation.algorithm import *
from modules.software_quality.experimentation.preprocessing import *

# Task ID
EVALUATION_TASK_ID = "EVALUATION"
PREDICTION_TASK_ID = "PREDICTION"


@celery.task(bind=True)
def evaluation_task(self, project_name):
    # Response content
    result = {"3_classes": {}, "26_classes": {}}
    self.update_state(state=states.STARTED, meta=result)

    if project_name is None:
        error = {"error": "Project not valid"}
        self.update_state(state=states.FAILURE, meta=error)
        return error

    # Load data
    sq_controller = SonarqubeController()
    tmp_sq_models = sq_controller.select_by_project_name(project_name)
    sq_models = [model for model in tmp_sq_models if model["label"] is not None]

    if not sq_models:
        error = {"error": "The project selected is not labelled"}
        self.update_state(state=states.FAILURE, meta=error)
        return error

    project_dataframe = pd.DataFrame(sq_models)

    for i in range(2):
        df_copy = project_dataframe.copy()

        if i == 0:  # 3 classes
            key = "3_classes"
            del df_copy["label"]
            df_copy.rename(columns={"label_three": "label"}, inplace=True)
        else:       # 26 classes
            key = "26_classes"
            del df_copy["label_three"]

        # Preprocessing
        df_copy = preprocess(df_copy)
        df_copy = column_preprocess(df_copy, scaling=True)
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
        result[key]["knn"] = evaluate(y_test, y_pred_knn, label_map)
        self.update_state(state='PROGRESS', meta=result)

        y_pred_rf, best_model = random_forest(X_train, y_train, X_test)
        result[key]["Random forest"] = evaluate(y_test, y_pred_rf, label_map)
        self.update_state(state='PROGRESS', meta=result)

        y_pred_lr, best_model = logistic_regression(X_train, y_train, X_test)
        result[key]["Logistic regression"] = evaluate(y_test, y_pred_lr, label_map)
        self.update_state(state='PROGRESS', meta=result)

        y_pred_svc, best_model = svc(X_train, y_train, X_test)
        result[key]["SVC"] = evaluate(y_test, y_pred_svc, label_map)
        self.update_state(state='PROGRESS', meta=result)

    self.update_state(state=states.SUCCESS, meta=result)
    return result


@celery.task(bind=True)
def prediction_task(self, project_name, algorithm, save):
    content = []
    self.update_state(state=states.STARTED, meta=content)

    algorithm_list = ["knn", "random-forest", "logistic-regression", "csv"]
    if algorithm not in algorithm_list:
        error = {"error": "algorithm undefined"}
        self.update_state(state=states.FAILURE, meta=error)
        return error

    sq_controller = SonarqubeController()
    sq_models_labelled = sq_controller.select_all_labelled()
    sq_models = sq_controller.select_by_project_name(project_name)

    for sq_model in sq_models:
        no_label_model = dict(sq_model)
        no_label_model["label"] = None
        no_label_model["label_three"] = None
        content.append(no_label_model)

    train_dataframe = pd.DataFrame(sq_models_labelled)
    test_dataframe = pd.DataFrame(content)
    self.update_state(state='PROGRESS', meta=content)

    keys = ["label", "label_three"]
    for key in keys:
        train_copy = train_dataframe.copy()
        test_copy = test_dataframe.copy()

        if key == "label_three":  # 3 classes
            del train_copy["label"]
            train_copy.rename(columns={"label_three": "label"}, inplace=True)
        else:  # 26 classes
            del train_copy["label_three"]

        # Preprocessing
        train_copy = preprocess(train_copy)
        sub_train = column_preprocess(train_copy.copy(), scaling=True)

        test_copy = preprocess(test_copy)
        sub_test = column_preprocess(test_copy.copy(), scaling=True)

        label_map = label_encoder(sub_train)

        y_train = sub_train["label"]
        del sub_train["label"]
        X_train = sub_train

        best_features = feature_selection(X_train, y_train)

        X_train = sub_train[best_features]
        X_test = sub_test[best_features]

        # Oversampling
        X_train, y_train = oversampling(X_train, y_train)

        if algorithm == "knn":
            y_pred, best_model = knn(X_train, y_train, X_test)
        elif algorithm == "random-forest":
            y_pred, best_model = random_forest(X_train, y_train, X_test)
        elif algorithm == "logistic-regression":
            y_pred, best_model = logistic_regression(X_train, y_train, X_test)
        else:
            y_pred, best_model = svc(X_train, y_train, X_test)

        test_copy["label"] = label_decoder(label_map, y_pred)
        content = add_label_to_content(content, test_copy, key)

        self.update_state(state='PROGRESS', meta=content)

        if save:
            for page in content:
                if page[key] is not None:
                    sq_model = SonarqubeBean(timestamp=page["timestamp"], project_name=page["project_name"],
                                         page=page["page"])
                    if key == "label":
                        sq_model.label = page[key]
                    else:
                        sq_model.label_three = page[key]
                    sq_models.append(sq_model)

            sq_controller.update_beans(sq_models)

    self.update_state(state=states.SUCCESS, meta=content)
    return content


def add_label_to_content(content, df, key):
    for index, row in df.iterrows():
        timestamp = row["timestamp"]
        project_name = row["project_name"]
        page = row["page"]
        label = row["label"]
        for i in range(len(content)):
            page_content = content[i]
            if page_content["timestamp"] == timestamp and page_content["project_name"] == project_name and \
                    page_content["page"] == page:
                content[key] = label
                break

    return content


def merge_df(df, sub_df):
    df_copy = df.copy()

    for index, row in df_copy.iterrows():
        # Check if the unique row is also in the subset
        if row["page"] in sub_df["page"].values and row["timestamp"] in sub_df["timestamp"].values and \
                row["project_name"] in sub_df["project_name"].values:
            for sub_index, sub_row in sub_df.iterrows():
                if sub_row["page"] == row["page"] and sub_row["timestamp"] == row["timestamp"] and \
                        sub_row["project_name"] == row["project_name"]:
                    print(sub_df["label"][sub_index])
                    df_copy["label"][index] = sub_df["label"][sub_index]
                    print(df_copy["label"][index])
                    break

    return df_copy

