# -*- coding: utf-8 -*-
"""DecisionTree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TKEf1ixWZUbR3qNwHlyeTU5fJTdbYOQK
"""

from google.colab import drive
from importlib import reload  # Py3 only; unneeded in py2.

drive = reload(drive)
drive.mount('/content/drive', force_remount=True)

!ls drive/My\ Drive

from google.colab import files
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

from google.colab import files

from pathlib import Path
from glob2 import glob
import pandas as pd
import numpy as np
import os
import zipfile as zf
import shutil
import re
import seaborn as sns
import random as ran

# files = zf.ZipFile("./drive/My Drive/dataset-resized.zip",'r')
# files.extractall()
# files.close()
# os.listdir(os.path.join(os.getcwd(),"dataset-resized"))

path_csv = 'drive/My Drive/Response4.xlsx 的副本'
# data_csv = pd.read_csv(path_csv)
data_csv = pd.read_excel(path_csv)
data_csv

# auth.authenticate_user()
# gauth = GoogleAuth()
# gauth.credentials = GoogleCredentials.get_application_default()
# drive = GoogleDrive(gauth)


# downloaded = drive.CreateFile({'id': "1MMvuEKKwJlE8IRabv_3l25Bn9vsrILhp"})

data_csv['生理性別'].fillna("男",inplace=True)

# data_csv = data_csv.dro
# data_continuous = data_csv.loc[:,['翹課堂數/上課堂數', '入學管道', '平均成績％數','就讀的學校', '時間戳記', '左手的掌心照', '近視度數', '喜歡的顏色', '每週運動幾次', '如果有打工的話 打工時薪多少', '你喜歡自己讀的科系嗎']]
# print(data_continuous)
unused_feat = ['翹課堂數/上課堂數', '就讀的學校', '時間戳記', '左手的掌心照','喜歡的顏色']
numerical_feat = ['近視度數', '每週運動幾次', '如果有打工的話 打工時薪多少', '你喜歡自己讀的科系嗎', '平均每天讀書時間(小時)']
target_feat = '平均成績％數'

data_drop = data_csv.drop(columns= [target_feat] + unused_feat + numerical_feat)
data_encoding = pd.get_dummies(data_drop)

data_t = pd.concat([data_encoding, data_csv.loc[:, numerical_feat]], axis=1)
data_t

print(data_csv['平均睡幾個小時'])

from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()

labelencoder.fit(list(data_csv['平均成績％數']))
u = labelencoder.transform(data_csv['平均成績％數'])
print(u)
# labelencoder.fit(list(data_csv['你喜歡自己讀的科系嗎']))
# v = labelencoder.transform(data_csv['每天花多久時間在休閒娛樂上'])
# print(v)
# scatter the sepal_length against the sepal_width
ax.scatter(u, data_csv['你喜歡自己讀的科系嗎'])
# ax.hist(data_csv['平均每天讀書時間(小時)'], facecolor='orange')
# ax.hist(u, facecolor='orange')

# set a title and labels
ax.set_title('Relation')
ax.set_xlabel('Grade')
ax.set_ylabel('degree of like')

from sklearn.preprocessing import LabelEncoder
data_te = data_csv[target_feat]
# print(data_te)
y = []
for i in range(data_te.shape[0]):
    # print(data_te[i])
    if data_te[i]=='0-10%' or data_te[i]=='11-20%' or data_te[i]=='21-30%' or data_te[i]=='31-40%':
        y.append(0)
    else:
        y.append(1);
# labelencoder.fit(list(data_te.values))
# y = labelencoder.transform(data_te)
y = np.array(y)
y

from sklearn.model_selection import train_test_split

X = data_t
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

print(X_train)

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

clf = RandomForestClassifier(n_estimators=100)

clf = clf.fit(X_train, y_train) # train model
Pred_x = clf.predict(X_test) # predict model
yy = clf.predict_proba(X_test) # probability of each class

from sklearn.svm import SVC

clf = SVC(kernel='linear')

from sklearn import tree
clf = tree.DecisionTreeClassifier()

from sklearn.neighbors import KNeighborsClassifier

clf = KNeighborsClassifier(n_neighbors=3)

from sklearn.linear_model import LogisticRegression

clf = LogisticRegression()

clf = clf.fit(X_train, y_train) # train model
Pred_x = clf.predict(X_test) # predict model
yy = clf.predict_proba(X_test) # probability of each class

imp = clf.feature_importances_
# sort(imp)
# print(imp)
plt.title('feature importance')

plt.bar(['study time', 'nearsighted', 'degree', 'sport', 'money'], [0.288692, 0.1, 0.07, 0.07, 0.05], color='red')
plt.figure(figsize=(20,4))
plt.show()

yy

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
cm = confusion_matrix(y_test, Pred_x)
print(cm)
df_cm = pd.DataFrame(cm,[0, 1],[0, 1])

plt.figure(figsize=(10,8))
sns.heatmap(df_cm,annot=True,fmt="d",cmap="YlGnBu")

correct = 0
total = len(Pred_x)

for i in range(total):
    if Pred_x[i]==y_test[i]:
        correct+=1
print(correct / total)

fpr = dict()
tpr = dict()
roc_auc = dict()
import numpy as np
from sklearn import metrics

# print(y)
y_ = pd.get_dummies(y_test)
# print(y_)
# print(y_)
# print(y_.iloc[:,1])
# print(preds[0][:])
# print(preds[0][:,0])
# print(y_.iloc[:,0])

for i in range(2):
    fpr[i], tpr[i], _ = metrics.roc_curve( y_.iloc[:,i], yy[:,i] ) 
    roc_auc[i] = metrics.auc(fpr[i], tpr[i])
plt.figure()
lw = 2
col = ['darkorange', 'green', 'red']
name = ['first', 'second']
plt.plot(fpr[0], tpr[0], color=col[0], lw=lw, label='first (area = %0.2f)' % roc_auc[i])
plt.plot(fpr[1], tpr[1], color=col[1], lw=lw, label='second (area = %0.2f)' % roc_auc[i])

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve')
plt.legend(loc="lower right")
plt.show()