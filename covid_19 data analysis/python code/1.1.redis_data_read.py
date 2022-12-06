"""
Сохраните данные из файла Excel в базе данных redis.

Сначала нам нужно открыть порты базы данных redis 6379 и 6380.
Мы считываем данные в разных местах файла raw excel data отдельно и сохраняем их в разных местах на разных портах.
Среди них в DB1-DB15 порта 6379 сначала хранятся данные об эпидемии в провинциях Шанхай, Чжэцзян и Цзянсу.
После этого были сохранены соответствующие данные из различных регионов Шанхая.
Порт 6380 хранит все данные, связанные с эпидемией, в 16 регионах Шанхая.
Местоположение, имя, перевод имени и другая информация из этих таблиц хранятся в db0 на порту 6379.
И эта информация также сохраняется в виде excel в локальном файле "0.file_all_информация.xlsx" внутри.
"""
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import redis
import os

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False
# coding:utf-8


def redis_data_save(file_name, file, ip, port, db):
    """
    читываем файл excel и сохраняем его в базе данных redis
    :param file_name: Имя файла
    :param file: Расположение файла
    :param ip: номер host
    :param port: номер port
    :param db: номер db
    """
    # создаем объект book
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)  # открываем первый лист
    # Подключение к redis
    rd = redis.Redis(host=ip, port=port, db=db, decode_responses=True)
    # копируем столбец excel в cols
    cols = sheet.ncols
    for cols_number in range(0, cols):  # вставляем в цикл в зависимости от количества строк
        if sheet.col_values(cols_number)[0] == 'date' or sheet.col_values(cols_number)[0] == '时间':
            resault_rare = sheet.col_values(cols_number)
            resault = []
            for list_number in range(len(resault_rare)):
                if list_number == 0:
                    resault.append(resault_rare[list_number])
                else:
                    delta = pd.Timedelta(str(resault_rare[list_number]) + 'days')
                    resault.append(str(pd.to_datetime('1899-12-30') + delta))
        else:
            resault = sheet.col_values(cols_number)  # Получение данных i-го столбца представляет собой список
        for j in range(1, len(resault)):  # получаем длину списка и записываем значение из вторых данных
            rd.rpush(resault[0], resault[j])  # 0-е данные используются в качестве имени ключа
            # print(f'正在插入第{resault[0]}的第{j}个数据')
    if file_name != '-':
        data_translation(file_name)
    file_list.append(file)
    file_name_list.append(file_name)
    ip_list.append(ip)
    port_list.append(port)
    db_list.append(db)


def data_translation(file_name):
    """
    Переводим имя файла на соответствующий китайский, английский и русский языки
    :param file_name:  Имя файла
    """
    if '.xlsx' in file_name:
        name = file_name[:-5]
    else:
        name = file_name[:-4]
    if name in list(translation_form.English):
        position = translation_form[translation_form.English == name].index.tolist()[0]
    elif name in list(translation_form.Chinese):
        position = translation_form[translation_form.Chinese == name].index.tolist()[0]
    else:
        position = translation_form[translation_form.Russian == name].index.tolist()[0]
    chinese_name = translation_form['Chinese'][position:position+1].values[0]
    english_name = translation_form['English'][position:position+1].values[0]
    russian_name = translation_form['Russian'][position:position+1].values[0]
    file_chinese_name_list.append(chinese_name)
    file_english_name_list.append(english_name)
    file_russian_name_list.append(russian_name)


if __name__ == '__main__':
    file_list = []
    file_name_list = []
    file_chinese_name_list = []
    file_english_name_list = []
    file_russian_name_list = []
    ip_list = []
    port_list = []
    db_list = []
    translation_form = pd.read_excel('translation.xlsx', sheet_name=0)

    # # shanghai covid19 data and district data(population,age, area...) read in redis port 6380
    # print('Start read data of shanghai covid19 data and district data')
    # # shanghai covid19 data
    # file_name = r'shanghai_covid19_data.xlsx'
    # redis_data_save(file_name, '127.0.0.1', 6379, 1)

    # data file position
    file_position = 'raw excel data'
    # province covid-19 data(shanghai jiangsu and zhejiang 3 provinces)
    filePath = 'province covid-19 data'
    nameList = os.listdir(file_position + '\\' + filePath)
    for i in range(len(nameList)):
        xls_name = file_position + '\\' + filePath + '\\' + nameList[i]
        redis_data_save(nameList[i], xls_name, '127.0.0.1', 6379, i + 1)
        # print('the file ' + nameList[i] + 'is in db' + str(i+1))

    # district data(population,age, area...)
    filePath = 'district data'
    nameList = os.listdir(file_position + '\\' + filePath)
    for i in range(len(nameList)):
        xls_name = file_position + '\\' + filePath + '\\' + nameList[i]
        redis_data_save(nameList[i], xls_name, '127.0.0.1', 6379, i+4)
        # print('the file ' + nameList[i] + 'is in db' + str(i+4))

    # district covid19 data(16 district) data read in redis port 6380
    print('Start read data of district covid19 data')
    filePath = 'district covid-19 data'
    nameList = os.listdir(file_position + '\\' + filePath)
    for i in range(len(nameList)):
        xls_name = file_position + '\\' + filePath + '\\' + nameList[i]
        redis_data_save(nameList[i], xls_name, '127.0.0.1', 6380, i)

    # file all information save in port 6379 db 0, and in 0.file_all_information.xlsx
    file_all_dict = {'file path': file_list, 'file name': file_name_list,
                     'file_chinese_name': file_chinese_name_list,
                     'file_english_name': file_english_name_list,
                     'file_russian_name': file_russian_name_list,
                     'ip name': ip_list, 'port name': port_list, 'db name': db_list}
    file_all_dataframe = pd.DataFrame(file_all_dict)
    file_all_dataframe.to_excel('0.file_all_information.xlsx')
    redis_data_save('-', '0.file_all_information.xlsx', '127.0.0.1', 6379, 0)
