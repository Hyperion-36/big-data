"""
Визуализация данных.
Мы считываем и визуализируем эпидемические данные по всем провинциям и городам, хранящиеся в базе данных.
Получите все данные о провинции или городе из базы данных, прочитайте ежедневные данные и нарисуйте картинку.
И сохраните их локально.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import os

plt.rcParams['font.size'] = 8
plt.rcParams['axes.unicode_minus'] = False
# coding:utf-8

diagnosis_dataframe = pd.read_excel('0.diagnosis_information.xlsx', sheet_name=0)
data = np.array(diagnosis_dataframe['diagnosis_count_list'])
print('start')
# Мы удаляем максимальное значение, которое очень сильно влияет на результат визуализации
data_list_less_province = [i for i in data if i < 5000]
data_less_province = [[i] for i in data if i < 5000]
print(data)
# K-means聚类
clusters_less_province = KMeans(n_clusters=3)
clusters_less_province.fit(data_less_province)
label_less_province = clusters_less_province.labels_
center_less_province = clusters_less_province.cluster_centers_
print(label_less_province)
x1 = []
data_dict_less_province = {'x1': data_list_less_province, 'label': list(label_less_province)}
data_dataframe_less_province = pd.DataFrame(data_dict_less_province)
label_0_less_province = list(data_dataframe_less_province[data_dataframe_less_province['label'] == 0]['x1'])
label_0_less_province = [[i] for i in label_0_less_province]
label_1_less_province = list(data_dataframe_less_province[data_dataframe_less_province['label'] == 1]['x1'])
label_1_less_province = [[i] for i in label_1_less_province]
label_2_less_province = list(data_dataframe_less_province[data_dataframe_less_province['label'] == 2]['x1'])
label_2_less_province = [[i] for i in label_2_less_province]
print(data_dataframe_less_province)
plt.scatter(label_0_less_province, label_0_less_province, label='0')
plt.scatter(label_1_less_province, label_1_less_province, label='1')
plt.scatter(label_2_less_province, label_2_less_province, label='2')
if not os.path.exists('visulation_result\\K-Means'):
    os.makedirs('visulation_result\\K-Means')
plt.savefig(os.path.join('visulation_result\\K-Means\\',
                         'less_province_K-Means.png'))

# Кластеризация числа случаев инфицирования в 34 провинциях или муниципалитетах,
# непосредственно подчиненных центральному правительству в Китае
data_list = [i for i in data]
data = [[i] for i in data]
print(data)
# K-means聚类
clusters = KMeans(n_clusters=3)
clusters.fit(data)
label = clusters.labels_
center = clusters.cluster_centers_
print(label)
x1 = []
data_dict = {'x1': data_list, 'label': list(label)}
data_dataframe = pd.DataFrame(data_dict)
label_0 = list(data_dataframe[data_dataframe['label'] == 0]['x1'])
label_0 = [[i] for i in label_0]
label_1 = list(data_dataframe[data_dataframe['label'] == 1]['x1'])
label_1 = [[i] for i in label_1]
label_2 = list(data_dataframe[data_dataframe['label'] == 2]['x1'])
label_2 = [[i] for i in label_2]
print(data_dataframe)
plt.scatter(label_0, label_0, label='0')
plt.scatter(label_1, label_1, label='1')
plt.scatter(label_2, label_2, label='2')
if not os.path.exists('visulation_result\\K-Means'):
    os.makedirs('visulation_result\\K-Means')
plt.savefig(os.path.join('visulation_result\\K-Means\\',
                         '34_province_K-Means.png'))

diagnosis_information = pd.read_excel('0.diagnosis_information.xlsx', sheet_name=0)
data = np.array(diagnosis_information['diagnosis_count_list'])
print('start')

# DBSCAN
raw_data = np.array(diagnosis_information['diagnosis_count_list'])
X = np.array([[i, i] for i in raw_data if i < 5000])
dbscan = DBSCAN(eps=1000, min_samples=5)  # eps---Радиус установлен равным 1000
dbscan.fit(X)
labels = dbscan.labels_
# dbscan.core_sample_indices_[:10]
plt.figure(figsize=(8, 6))
plt.subplot(111)
plt.scatter(X[labels == 0], X[labels == 0])
plt.scatter(X[labels == -1], X[labels == -1])
plt.title("DBSCAN_Радиус_1000")
if not os.path.exists('visulation_result\\DBSCAN'):
    os.makedirs('visulation_result\\DBSCAN')
plt.savefig(os.path.join('visulation_result\\DBSCAN\\',
                         'DBSCAN_Радиус_1000.png'))

data = np.array(diagnosis_dataframe['diagnosis_count_list'])
X = np.array([[i, i] for i in data if i < 5000])
dbscan = DBSCAN(eps=100, min_samples=5)  # eps---Радиус установлен равным 1000
dbscan.fit(X)
labels = dbscan.labels_
# dbscan.core_sample_indices_[:10]
plt.figure(figsize=(8, 6))
plt.subplot(111)
plt.scatter(X[labels == 0], X[labels == 0])
plt.scatter(X[labels == -1], X[labels == -1])
plt.title("DBSCAN_Радиус_100")
if not os.path.exists('visulation_result\\DBSCAN'):
    os.makedirs('visulation_result\\DBSCAN')
plt.savefig(os.path.join('visulation_result\\DBSCAN\\',
                         'DBSCAN_Радиус_100.png'))


if __name__ == '__main__':
    print('Start clustering.')
