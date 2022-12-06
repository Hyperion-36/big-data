"""
The analysis of covid-19 data in Shanghai and its districts.
It contains:
1:Data acquisition of Shanghai,China and its district.(from excel)
2.Data preprocessing of Shanghai City and its district.(Process and save the required data)
3.Visualization of Shanghai and its district data.

Анализ данных по covid-19 в Шанхае и его районах.
Он содержит:
1: Сбор данных о Шанхае, Китай, и его округе. (из excel)
2.Предварительная обработка данных о городе Шанхай и его районе.(Обработайте и сохраните необходимые данные)
3.Визуализация Шанхая и его районных данных.
"""

import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import matplotlib
import math
import numpy as np
import turtle
import os

# file_shanghai = ('D:\研究生\Наука о данных и аналитика больших объемов информации 数据科学与大数据分析\作业'
#                  '\data\shanghai_covid19_data\shanghai_covid19_data.xlsx')
shanghai_covid19_data = pd.read_excel('shanghai_covid19_data.xlsx', sheet_name=0)
# # get the data of all district
baoshan_covid19_data = pd.read_excel('district_covid19_data\\baoshan.xls', sheet_name=0)
changning_covid19_data = pd.read_excel('district_covid19_data\\changning.xls', sheet_name=0)
chongming_covid19_data = pd.read_excel('district_covid19_data\\chongming.xls', sheet_name=0)
fengxian_covid19_data = pd.read_excel('district_covid19_data\\fengxian.xls', sheet_name=0)
hongkou_covid19_data = pd.read_excel('district_covid19_data\\hongkou.xls', sheet_name=0)
huangpu_covid19_data = pd.read_excel('district_covid19_data\\huangpu.xls', sheet_name=0)
jiading_covid19_data = pd.read_excel('district_covid19_data\\jiading.xls', sheet_name=0)
jingan_covid19_data = pd.read_excel('district_covid19_data\\jingan.xls', sheet_name=0)
jinshan_covid19_data = pd.read_excel('district_covid19_data\\jinshan.xls', sheet_name=0)
minhang_covid19_data = pd.read_excel('district_covid19_data\\minhang.xls', sheet_name=0)
pudong_covid19_data = pd.read_excel('district_covid19_data\\pudong.xls', sheet_name=0)
putuo_covid19_data = pd.read_excel('district_covid19_data\\putuo.xls', sheet_name=0)
qingpu_covid19_data = pd.read_excel('district_covid19_data\\qingpu.xls', sheet_name=0)
songjiang_covid19_data = pd.read_excel('district_covid19_data\\songjiang.xls', sheet_name=0)
xuhui_covid19_data = pd.read_excel('district_covid19_data\\xuhui.xls', sheet_name=0)
yangpu_covid19_data = pd.read_excel('district_covid19_data\\yangpu.xls', sheet_name=0)
translation_form = pd.read_excel('translation.xlsx', sheet_name=0)
cumulative_diagnosis_data = shanghai_covid19_data['Cumulative diagnosis']
newly_diagnosed_data = shanghai_covid19_data['Newly diagnosed']
# date = shanghai_covid19_data['date']

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False


def visualation_data(x, y, label_name, savefig_name):
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    y = y.replace('-', 0)
    # plt.plot(date, cumulative_diagnosis_data, linewidth='1', label="Совокупный диагноз")
    # plt.plot(date, newly_diagnosed_data, 'o', linewidth='1', label="Недавно диагностированный")
    plt.plot(x, y, linewidth='1', label=label_name)
    plt.legend()
    plt.savefig(savefig_name)
    plt.subplot(111)
    plt.cla()


# def district_visualation(data, district_name):
#     # visualization of the whole newly diagnosed data
#     visualation_data(data['时间'],  data['本土新增'],
#                      district_name + "Недавно диагностированный", district_name + '_1.all_newly_diagnosed_line.png')
#
#     # visualization of the whole cumulative diagnosis data
#     visualation_data(data['时间'], data['本土累计确诊'],
#                      district_name + "Совокупный диагноз", district_name + '_2.all_cumulative_diagnosis_line.png')
#
#     # visualization of the whole cumulative deaths data
#     visualation_data(data['时间'], data['累计死亡'],
#                      district_name + "Совокупная смертность", district_name + '_3.all_cumulative_deaths_line.png')


# visualization of the whole newly diagnosed data
visualation_data(shanghai_covid19_data['date'], shanghai_covid19_data['Newly diagnosed'],
                 "Недавно диагностированный", '1.all_newly_diagnosed_line.png')

# visualization of the whole cumulative diagnosis data
visualation_data(shanghai_covid19_data['date'], shanghai_covid19_data['Cumulative diagnosis'],
                 "Совокупный диагноз", '2.all_cumulative_diagnosis_line.png')

# visualization of the whole cumulative deaths data
visualation_data(shanghai_covid19_data['date'], shanghai_covid19_data['death added'],
                 "Смерть добавила", '3.all_death_added_line.png')

# visualization of the whole cumulative deaths data
visualation_data(shanghai_covid19_data['date'], shanghai_covid19_data['Cumulative deaths'],
                 "Совокупная смертность", '4.all_cumulative_deaths_line.png')

# district_visualation(baoshan_covid19_data, 'baoshan')
# district_visualation(changning_covid19_data, 'changning')
# district_visualation(chongming_covid19_data, 'chongming')
# district_visualation(fengxian_covid19_data, 'fengxian')
# district_visualation(hongkou_covid19_data, 'hongkou')
# district_visualation(huangpu_covid19_data, 'huangpun')
# district_visualation(jiading_covid19_data, 'jiading')
# district_visualation(jingan_covid19_data, 'jingan')
# district_visualation(jinshan_covid19_data, 'jinshan')
# district_visualation(minhang_covid19_data, 'minhang')
# district_visualation(pudong_covid19_data, 'pudong')
# district_visualation(putuo_covid19_data, 'putuo')
# district_visualation(qingpu_covid19_data, 'qingpu')
# district_visualation(songjiang_covid19_data, 'songjiang')
# district_visualation(xuhui_covid19_data, 'xuhui')
# district_visualation(yangpu_covid19_data, 'yangpu')

if __name__ == '__main__':
    print('Start data visualization')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
