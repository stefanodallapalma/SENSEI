from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def knn(X_train, y_train, X_test):
    print("KNN")
    neighbors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50]

    hyperparameter = {"n_neighbors": neighbors}

    knn = KNeighborsClassifier()
    clf = GridSearchCV(knn, hyperparameter)

    # Fit the model
    best_model = clf.fit(X_train, y_train)

    # Prediction
    y_pred = clf.predict(X_test)

    return y_pred, best_model


def random_forest(X_train, y_train, X_test):
    print("Random Forest")

    hyperparameter = {
        "max_depth": [3, 10, 50, None],
        'n_estimators': [10, 20, 30, 50, 100, 200, 500, 1000, 2000]}

    rf = RandomForestClassifier()

    clf = GridSearchCV(rf, hyperparameter)

    # Fit the model
    clf.fit(X_train, y_train)

    # Prediction
    y_pred = clf.predict(X_test)

    return y_pred


def logistic_regression(X_train, y_train, X_test):
    print("Logistic regression")

    hyperparameter = {
        'solver': ['newton-cg', 'lbfgs', 'sag'],
        'max_iter': [50, 100, 300, 500, 1000]}

    lr = LogisticRegression()
    clf = GridSearchCV(lr, hyperparameter)

    # Fit the model
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    return y_pred


def svc(X_train, y_train, X_test):
    print("SVC")

    hyperparameter = {'gamma': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 0.0001, 0.00001, 0.000001],
                      'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000, 1000000]}

    svc = SVC()
    clf = GridSearchCV(svc, hyperparameter)

    # Fit the model
    clf.fit(X_train, y_train)

    # Prediction
    y_pred = clf.predict(X_test)

    return y_pred