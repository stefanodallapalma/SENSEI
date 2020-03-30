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


def preprocess(data):
    # 1) NULL preprocessing

    # Deleting columns with number of null > 9000
    for column in data.columns:
        if data[column].isnull().sum() > (data.shape[0]*0.9):
            del data[column]

    # Deleting rows with nans
    data = data.dropna()

    if "label" not in data:
        data["label"] = np.nan

    return data


def column_preprocess(data, scaling=False):
    # Dropping additional columns that will not be used for classification
    columns_not_to_use = ['timestamp', 'project_name', 'page']
    for column in columns_not_to_use:
        if column in data:
            del data[column]

    columns = [column for column in list(data.columns.values) if column != "label"]

    if scaling:
        scaler = MinMaxScaler()
        data[columns] = scaler.fit_transform(data[columns])

    return data


def label_encoder(data):
    # Convert main class to categorical values
    le = preprocessing.LabelEncoder()

    le.fit(data['label'])
    data['label'] = le.transform(data['label'])

    cv_dict = dict(zip(le.transform(le.classes_), le.classes_))

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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
    print(y_train)
    print(y_test)
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

    # Extract all cv
    cvs = []
    for key in cr:
        try:
            cv = int(key)
            cvs.append(cv)
        except:
            pass

    cr["Classes"] = {}
    for i in range(len(cvs)):
        cr[str(cvs[i])]["accuracy"] = cm.diagonal()[i]
        cr["Classes"][cv_dict[cvs[i]]] = cr.pop(str(cvs[i]))

    cr["accuracy"] = np.mean(cm.diagonal())
    #cr["Confusion Matrix"] = pd.Series(confusion_matrix(y_test, y_pred)).to_json(orient='records')

    return cr





