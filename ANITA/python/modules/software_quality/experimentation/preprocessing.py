import pandas as pd, numpy as np, json
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import RandomOverSampler

from .algorithm import *
from database.anita.controller.SonarqubeController import SonarqubeController


def three_classifiers(label_column):
    if label_column in ['Pornography','Drugs','Violence','Counterfeit Credit-Cards','Counterfeit Money','Counterfeit Personal-Identification',
                     'Hacking','Cryptolocker','Marketplace','Services','Forum','Fraud']:
        return 'Suspicious'
    if label_column in ['Down','Empty', 'Locked']:
        return 'Unknown'
    else:
        return 'Normal'


def preprocessing(data, scaling=False):
    # 1) NULL preprocessing

    # Deleting columns with number of null > 9000
    columns_to_drop = []
    for column in data.columns:
        if data[column].isnull().sum() > (data.shape[0]*0.9):
            columns_to_drop.append(column)

    columns_of_interest = [elem for elem in data.columns if elem not in columns_to_drop]

    # Deleting rows with nans
    data = data[columns_of_interest].dropna()

    # 2) Useless columns preprocessing

    # Dropping additional columns that will not be used for classification
    columns_not_to_use = ['timestamp', 'project_name', 'page']
    columns_to_use = [elem for elem in data.columns if elem not in columns_not_to_use and elem != "label"]
    for column in columns_not_to_use:
        del data[column]

    if scaling:
        scaler = MinMaxScaler()
        data[columns_to_use] = scaler.fit_transform(data[columns_to_use])

    return data


def label_encoder(data):
    # Convert main class to categorical values
    le = preprocessing.LabelEncoder()

    le.fit(data['label'])
    le_classes_cv = le.transform(le.classes_)

    cv_dict = dict(zip(le_classes_cv, le.classes_))
    data['label'] = le_classes_cv

    return cv_dict


def label_decoder(label_map, encoder_list):
    decode_list = []
    for encoder in encoder_list:
        decode_list.append(label_map[encoder])

    return decode_list


def feature_selection(X, y):
    bestfeatures = SelectKBest(score_func=chi2, k=30)
    fit = bestfeatures.fit(X, y)

    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)

    featureScores = pd.concat([dfcolumns, dfscores], axis=1)
    featureScores.columns = ['Specs', 'Score']

    return featureScores.nlargest(17, 'Score')["Specs"].tolist()


def train_test(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    return X_train, X_test, y_train, y_test


def oversampling(X_train, y_train):
    ros = RandomOverSampler()
    X_train, y_train = ros.fit_sample(X_train,y_train)

    return X_train, y_train


def evaluate(y_test, y_pred, cv_dict):
    cr = classification_report(y_test, y_pred, output_dict=True)

    # Get the confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Now the normalize the diagonal entries
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    for i in range(len(cv_dict)):
        cr[str(i)]["accuracy"] = cm.diagonal()[i]

    cr["accuracy"] = np.mean(cm.diagonal())
    cr["Confusion Matric"] = str(cm)

    for key in cv_dict:
        cr[key] = cr.pop(str(cv_dict[key]))

    return cr





