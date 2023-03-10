# -*- coding: utf-8 -*-
"""Copy of Copy of Microchip_Concerns_ML_(imporving_Health) (01-DTreeShar).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IyBqTwJ576syzECBxBhGFFd98lFTQYki
"""

import pandas as pd

import csv
import numpy as np

#pwd
!ls

pwd

dfx = pd.read_csv("dataX.csv")
dfy = pd.read_csv("datay.csv")

pwd

ls

dfx.head()

dfx.columns

dfx.info()

"""#Trian, Test """

from sklearn.model_selection import train_test_split

dfx.info()

#Droping columns that are not needed
X = dfx.drop(['Code1','Code2', 'Code3', 'Code4', 'Code5', 'Code6', 'Code7', 'hrlabel'] , axis=1)
y = dfx['hrlabel']

#Participants Demographic Information
X

# saved X as Excel file


# saved X as CSV file

dfx.columns

#Taerget Variable (Health Risk)
y

dfx.info()

dfx['gender'] = dfx['gender'].astype('object')

dfx['gender']

#
dfx['gender'].replace(['M','F'],[1,2], inplace=True)
#c.rename_categories({'a': 'A', 'c': 'C'})

dfx['gender'] = dfx['gender'].astype('category')

dfx.info()

df1=dfx #Creating a copy of df for XGBoost because we wanted to change the data type of Cat to int for that model as we got the Error

dfx['gender']

####################################################################
#df['Code1'].value_counts()

#df["Code1"] = df["Code1"].str.lower()

##################################################################3
#Starting the Model Training>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

from sklearn.tree import DecisionTreeClassifier

dtree = DecisionTreeClassifier()

dtree.fit(X_train,y_train)

"""# Predictions

"""

predictions = dtree.predict(X_test)

from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,predictions))
print(confusion_matrix(y_test,predictions))

"""## Tree Visualization

"""

!pip install pydot

from IPython.display import Image  
#from sklearn.externals.six import StringIO  
from six import StringIO
from sklearn.tree import export_graphviz
import pydot 

features = list(X.columns)
features

dot_data = StringIO()  
export_graphviz(dtree, out_file=dot_data,feature_names=features,filled=True,rounded=True)

graph = pydot.graph_from_dot_data(dot_data.getvalue())  
Image(graph[0].create_png())

"""#Purunning the Decision Tree




"""

import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn import tree
from sklearn.metrics import accuracy_score,confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

#Train, Test Data again for Purunning:
x_train,x_test,y_train,y_test = train_test_split(X,y,stratify=y)
print(x_train.shape)
print(x_test.shape)

#we will fit a normal decision tree without any fine tuning and check the results
clf = tree.DecisionTreeClassifier(random_state=0)
clf.fit(x_train,y_train)
y_train_pred = clf.predict(x_train)
y_test_pred = clf.predict(x_test)

dfx.columns

#Visualizing decision tree
plt.figure(figsize=(30,30))
#features = df.columns
classes = ['Not health risk','hearlth risk']
tree.plot_tree(clf,feature_names=features,class_names=classes,filled=True)
plt.show()

# helper function
def plot_confusionmatrix(y_train_pred,y_train,dom):
    print(f'{dom} Confusion matrix')
    cf = confusion_matrix(y_train_pred,y_train)
    sns.heatmap(cf,annot=True,yticklabels=classes
               ,xticklabels=classes,cmap='Reds', fmt='g')
    plt.tight_layout()
    plt.show()

print(f'Train score {accuracy_score(y_train_pred,y_train)}')
print(f'Test score {accuracy_score(y_test_pred,y_test)}')
plot_confusionmatrix(y_train_pred,y_train,dom='Train')
plot_confusionmatrix(y_test_pred,y_test,dom='Test')

#Pre pruning techniques
params = {'max_depth': [2,4,6,8,10,12],
         'min_samples_split': [2,3,4],
         'min_samples_leaf': [1,2]}

clf = tree.DecisionTreeClassifier()
gcv = GridSearchCV(estimator=clf,param_grid=params)
gcv.fit(x_train,y_train)

GridSearchCV(estimator=DecisionTreeClassifier(),
             param_grid={'max_depth': [2, 4, 6, 8, 10, 12],
                         'min_samples_leaf': [1, 2],
                         'min_samples_split': [2, 3, 4]})

model = gcv.best_estimator_
model.fit(x_train,y_train)
y_train_pred = model.predict(x_train)
y_test_pred = model.predict(x_test)

print(f'Train score {accuracy_score(y_train_pred,y_train)}')
print(f'Test score {accuracy_score(y_test_pred,y_test)}')
plot_confusionmatrix(y_train_pred,y_train,dom='Train')
plot_confusionmatrix(y_test_pred,y_test,dom='Test')

model #The best case

X

X.columns

features

#Visualization after Puruning:
plt.figure(figsize=(30,30))
#features = df.columns
classes = ['No health risk','health risk']
tree.plot_tree(model,feature_names=features,class_names=classes,filled=True)
plt.show()

#After prunning Calculation (Added by Sh(me))
#from sklearn.metrics import classification_report,confusion_matrix
print(classification_report(y_test,y_test_pred))
#print(confusion_matrix(y_test,predictions))
print(confusion_matrix(y_test,y_test_pred))