# Importing required libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Loading and reading the dataset
heart = pd.read_csv("heart_cleveland_upload.csv")

# Creating a copy of the dataset so that it will not affect our original dataset
heart_df = heart.copy()

# Renaming some of the columns
heart_df = heart_df.rename(columns={'condition':'target'})
print(heart_df.head())

# Checking class distribution
print(heart_df['target'].value_counts())

# Splitting our data into X and y. Here y contains target data and X contains rest of the features
X = heart_df.drop(columns='target')
y = heart_df['target']

# Using StratifiedShuffleSplit to ensure equal distribution of classes in train and test sets
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.25, random_state=42)

for train_index, test_index in sss.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# Feature scaling
scaler = StandardScaler()
X_train_scaler = scaler.fit_transform(X_train)
X_test_scaler = scaler.transform(X_test)

# Creating and evaluating different classifiers
# Logistic Regression
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train_scaler, y_train)
y_pred_log_reg = log_reg.predict(X_test_scaler)
print('Logistic Regression Accuracy: {}%\n'.format(round((accuracy_score(y_test, y_pred_log_reg) * 100), 2)))
print('Classification Report\n', classification_report(y_test, y_pred_log_reg))
print(confusion_matrix(y_test, y_pred_log_reg))

# K-Nearest Neighbors
knn = KNeighborsClassifier()
knn.fit(X_train_scaler, y_train)
y_pred_knn = knn.predict(X_test_scaler)
print('KNN Accuracy: {}%\n'.format(round((accuracy_score(y_test, y_pred_knn) * 100), 2)))
print('Classification Report\n', classification_report(y_test, y_pred_knn))
print(confusion_matrix(y_test, y_pred_knn))

# Decision Tree Classifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train_scaler, y_train)
y_pred_dt = dt.predict(X_test_scaler)
print('Decision Tree Accuracy: {}%\n'.format(round((accuracy_score(y_test, y_pred_dt) * 100), 2)))
print('Classification Report\n', classification_report(y_test, y_pred_dt))
print(confusion_matrix(y_test, y_pred_dt))

# Random Forest Classifier
rf = RandomForestClassifier(n_estimators=20, random_state=42)
rf.fit(X_train_scaler, y_train)
y_pred_rf = rf.predict(X_test_scaler)
print('Random Forest Accuracy: {}%\n'.format(round((accuracy_score(y_test, y_pred_rf) * 100), 2)))
print('Classification Report\n', classification_report(y_test, y_pred_rf))
print(confusion_matrix(y_test, y_pred_rf))

# Saving the best model 
filename = 'heart-disease-prediction-knn-model.pkl'
pickle.dump(knn, open(filename, 'wb'))
