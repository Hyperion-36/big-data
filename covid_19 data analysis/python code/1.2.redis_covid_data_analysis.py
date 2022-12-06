"""
Мы визуализируем все данные, связанные с эпидемией.
Включая все эпидемиологические данные из Цзянсу, Чжэцзяна,  Шанхая и 16 регионов Шанхая.
"""
import matplotlib.pyplot as plt
import pandas as pd
import redis
import numpy as np
import os

# plt.rcParams['font.family'] = 'SimHei'
# plt.rcParams['font.family'] = "Times new roman"
plt.rcParams['font.size'] = 8
plt.rcParams['axes.unicode_minus'] = False
# coding:utf-8

host = '127.0.0.1'


def get_all_db_data(port, db):
    """
    Получите данные всей таблицы базы данных （获取整个db表的数据）
    Get the data of the entire database table
    :param port: Название порта
    :param db: Название db
    :return: dataframe Возвращает полную таблицу данных с типом Dataframe
    """
    r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    keys = r.keys()
    dict_all = {}
    # Цикл по имени, чтобы получить все данные по имени key
    for key_number in range(len(keys)):
        key_name = keys[key_number]
        # Получить данные столбца по имени key
        key_value = r.lrange(key_name, 0, -1)
        # Сохраните результат в словаре
        dict_part = {key_name: key_value}
        dict_all.update(dict_part)
    # Преобразовать словарь в формат dataframe
    dataframe = pd.DataFrame(dict_all)
    return dataframe


def get_list_data(port, db, key):
    """
    Получить данные столбца в таблице db с помощью ключа（获取某个db表中某个key的数据）
    Get the data of a key in a db table
    :param port: Название порта
    :param db: Название db
    :param key: Название key
    :return: key_value Возвращает данных с типом list
    """
    r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    key_value = r.lrange(key, 0, -1)
    return key_value


def data_type_transform(data, data_type):
    """
    Преобразуем тип данных Redis в нужный нам тип (дата, время и int)
    transform the type of Redis data into the type we need(date time and int)
    :param data: обычная дата
    :param data_type: тип данных (время или что-то еще)
    :return: data: данные, которые нам нужны
    """
    # Позволяет преобразовывать данные в формат float
    data = [0 if piece_data == '-' else piece_data for piece_data in data]
    # Если данные представляют время,
    # то данные необходимо преобразовать в формат временной метки, который можно визуализировать.
    if data_type == 'date':
        data = [pd.to_datetime(piece_data) for piece_data in data]
    # Если данные не редставляют время,
    # то данные необходимо преобразовать в формат float, который можно визуализировать.
    else:
        data = [int(float(piece_data)) for piece_data in data]
    return data


def select_desired_time(x_rare, y_rare, start_data='2022-01-15 00:00:00', end_data='2022-07-01 00:00:00',
                        x_type='date', y_type='number'):
    """
    Получите данные в течение времени, которое мы хотим проанализировать в соответствии со временем.
    Поскольку мы хотим проанализировать данные с января по июль, мы уже присвоили значение.
    Мы можем повторно присвоить значение, и изменить время,
    чтобы взять число и проанализировать данные в другое время.
    （根据时间获取我们想要分析的时间内的数据，因为我们想要分析一月到七月的数据，所以已经进行了赋值，后续可以重新赋值修改取数时间，分析其他时间的数据）
    :param x_rare: данные по оси x (данные о времени)
    :param y_rare: данные по оси y (Данные которые мы хотим проанализировать)
    :param start_data: Время начала(может указан повторно)
    :param end_data: Время окончила(может указан повторно)
    :param x_type: тип данных по оси x (может указан повторно, по умолчанию здесь используется время)
    :param y_type: тип данных по оси y (может указан повторно, по умолчанию здесь используется float)
    :return: x_part данные по оси x после завершения обработки
             y_part данные по оси y после завершения обработки
    """
    # Преобразуйте данные в нужный нам формат
    x_transform = data_type_transform(x_rare, x_type)
    y_transform = data_type_transform(y_rare, y_type)
    # Чтобы найти нужное нам время, нам нужно преобразовать данные временной метки в строковую форму
    x_str = [str(x_data) for x_data in x_transform]
    # Найдите место, где начинается и заканчивается время
    start_position = x_str.index(start_data)
    end_position = x_str.index(end_data)
    # Перехватывать необходимые данные
    x_part = x_transform[start_position:end_position]
    y_part = y_transform[start_position:end_position]
    return x_part, y_part


def visualization_date_data(x_date_data, y_date_data, label_name, save_path,
                            savefig_name, x_type='date', y_type='number'):
    """
    Сохраните визуальную картину временных данных (полное время, исключая захват времени)
    (保存时间数据的可视化图片（完整时间，不包含时间截取）
    :param x_date_data: данные по оси x (данные о времени)
    :param y_date_data: данные по оси y (Данные которые мы хотим проанализировать)
    :param label_name: Метка данных, используемая для описания данных
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    :param savefig_name: Имя изображения сохраненного изображения
    :param x_type: Формат данных по оси X
    :param y_type: Формат данных по оси Y
    :return:
    """
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    x_date_data = data_type_transform(x_date_data, x_type)
    y_date_data = data_type_transform(y_date_data, y_type)
    # Визуализация данных
    plt.plot(x_date_data, y_date_data, linewidth='1', label=label_name)
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join(save_path, savefig_name))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()


def visualization_part_data(x_part_data, y_part_data, label_name, save_path,
                            savefig_name, x_type='date', y_type='number'):
    """
    Сохранение визуальных изображений временных данных (включая захват времени)
    Чтобы получить необходимые нам анализируемые данные, перехватите фрагмент
    данных по времени, а затем выполните операции визуализации
    (保存时间数据的可视化图片（包含时间截取）为了得到我们需要的分析数据，截取片段, 基于时间的数据，然后执行可视化操作)
    :param x_part_data: данные по оси x (данные о времени)
    :param y_part_data: данные по оси y (Данные которые мы хотим проанализировать)
    :param label_name: Метка данных, используемая для описания данных
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    :param savefig_name: Имя изображения сохраненного изображения
    :param x_type: Формат данных по оси X
    :param y_type: Формат данных по оси Y
    """
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    x_part_data = data_type_transform(x_part_data, x_type)
    y_part_data = data_type_transform(y_part_data, y_type)
    # Выберите необходимое время
    x_part_data, y_part_data = select_desired_time(x_part_data, y_part_data)
    # Визуализация данных
    plt.plot(x_part_data, y_part_data, linewidth='1', label=label_name)
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join(save_path, savefig_name))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()


def district_visualization(data, district_visualization_name, number, save_path):
    """
    Визуальный анализ данных в каждом регионе (Выберите необходимые данные по названию столбца)
    :param data: Данные в формате Dataframe
    :param district_visualization_name: Название района
    :param number: Регионы сортируются по номерам, и цифры - это числа, представленные расположением регионов
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # visualization of the whole newly diagnosed data
    visualization_date_data(data['时间'], data['本土新增'], district_visualization_name + "Недавно диагностированный",
                            save_path, 'district' + number + '_' + district_visualization_name +
                            '_1.all_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_date_data(data['时间'], data['本土累计确诊'], district_visualization_name + "Совокупный диагноз",
                            save_path, 'district' + number + '_' + district_visualization_name +
                            '_2.all_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['时间'], data['累计死亡'], district_visualization_name + "Совокупная смертность",
                            save_path, 'district' + number + '_' + district_visualization_name +
                            '_3.all_cumulative_deaths_line.png')


def province_visualization(data, province_name, save_path):
    """
    Визуализация провинциальных и муниципальных данных (Выберите необходимые данные по названию столбца)
    :param data: Данные в формате Dataframe
    :param province_name: Название провинции
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # visualization of the whole Newly diagnosed data
    visualization_date_data(data['date'], data['Newly diagnosed'],
                            province_name + "Недавно диагностированный", save_path,
                            'province_' + province_name + '_1.all_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_date_data(data['date'], data['Cumulative diagnosis'],
                            province_name + "Совокупный диагноз", save_path,
                            'province_' + province_name + '_2.all_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['date'], data['death added'],
                            province_name + "Смерть добавила", save_path,
                            'province_' + province_name + '_3.all_death_added_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['date'], data['Cumulative deaths'],
                            province_name + "Совокупная смертность", save_path,
                            'province_' + province_name + '_4.all_cumulative_deaths_line.png')


def district_part_visualization(data, district_visualization_name, number, save_path):
    """
    Визуальный анализ данных в каждом регионе (Выберите необходимое время)
    :param data: Данные в формате Dataframe
    :param district_visualization_name: Название района
    :param number: Регионы сортируются по номерам, и цифры - это числа, представленные расположением регионов
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # visualization of the whole newly diagnosed data
    visualization_part_data(data['时间'], data['本土新增'], district_visualization_name + "Недавно диагностированный",
                            save_path, 'district' + number + '_' + district_visualization_name +
                            '_1.part_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_part_data(data['时间'], data['本土累计确诊'], district_visualization_name + "Совокупный диагноз",
                            save_path, 'district' + number + '_' +
                            district_visualization_name + '_2.part_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_part_data(data['时间'], data['累计死亡'], district_visualization_name + "Совокупная смертность",
                            save_path, 'district' + number + '_' + district_visualization_name +
                            '_3.part_cumulative_deaths_line.png')


def province_part_visualization(data, province_name, save_path):
    """
    Визуализация провинциальных и муниципальных данных (Выберите необходимое время)
    :param data: Данные в формате Dataframe
    :param province_name: Название провинции
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    visualization_part_data(data['date'], data['Newly diagnosed'],
                            province_name + "Недавно диагностированный", save_path,
                            'province_' + province_name + '_1.part_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_part_data(data['date'], data['Cumulative diagnosis'],
                            province_name + "Совокупный диагноз", save_path,
                            'province_' + province_name + '_2.part_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_part_data(data['date'], data['death added'],
                            province_name + "Смерть добавила", save_path,
                            'province_' + province_name + '_3.part_death_added_line.png')
    # visualization of the whole cumulative deaths data
    visualization_part_data(data['date'], data['Cumulative deaths'],
                            province_name + "Совокупная смертность", save_path,
                            'province_' + province_name + '_4.part_cumulative_deaths_line.png')


def histogram_visualization(x_data, y_data, savefig_name, label_name, title_name, ylabel_name, save_path):
    """
    Нарисуйте гистограмму(Горизонтальный дисплей)
    :param x_data: данные по оси x
    :param y_data: данные по оси y
    :param savefig_name:  Имя изображения сохраненного изображения
    :param label_name:  Метка данных, используемая для описания данных
    :param title_name: Название титула
    :param ylabel_name: Название оси y
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # Нарисуйте изображение
    figure, axi = plt.subplots()
    b = axi.barh(x_data, y_data, color='#6699CC', label=label_name)
    # bar_label
    # Добавить метку данных
    for piece_b in b:
        width_b = piece_b.get_width()
        axi.text(width_b, piece_b.get_y() + piece_b.get_height() / 2, '%.2f' % float(width_b), ha='left', va='center')
    # Установите метку галочки по оси Y
    axi.set_yticks(range(len(x_data)))
    axi.set_yticklabels(x_data)
    # Завершите процесс визуализации
    plt.title(title_name)
    plt.ylabel(ylabel_name)
    plt.legend()
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join(save_path, savefig_name))
    # plt.savefig(savefig_name)
    plt.subplot(111)
    plt.cla()
    plt.close()


def data_translation(name):
    """
    Найдите соответствующее значение в таблице перевода и переведите его на китайский, английский и русский языки
    :param name: Название значения
    :return: Словарь, содержащий всю информацию
    """
    # Найди местоположение значения
    if name in list(translation_form.English):
        file_position = translation_form[translation_form.English == name].index.tolist()[0]
    elif name in list(translation_form.other_name):
        file_position = translation_form[translation_form.other_name == name].index.tolist()[0]
    elif name in list(translation_form.Chinese):
        file_position = translation_form[translation_form.Chinese == name].index.tolist()[0]
    else:
        file_position = translation_form[translation_form.Russian == name].index.tolist()[0]
    # Найди соответствующий перевод по местоположению и сохраните его в словаре
    chinese_name = translation_form['Chinese'][file_position:file_position + 1].values[0]
    english_name = translation_form['English'][file_position:file_position + 1].values[0]
    russian_name = translation_form['Russian'][file_position:file_position + 1].values[0]
    name_dict = {'chinese_name': chinese_name, 'english_name': english_name,
                 'russian_name': russian_name}
    return name_dict


def autolabel(rects):
    """
    Отобразить значение в столбчатом（显示柱状图名称）
    :param rects: изображение
    """
    for piece_rect in rects:
        height = piece_rect.get_width()
        plt.text(height, piece_rect.get_y() + piece_rect.get_height() / 2,
                 '%.2f' % float(height), ha='left', va='center')


def dataframe_replace(data, replace_before, replace_after):
    """
    Заменить данные
    :param data: Данные в формате dataframe
    :param replace_before: Замените предыдущие данные
    :param replace_after: Замененные данные
    :return: Замените заполненные данные
    """
    for data_part in data:
        data[data_part] = data[data_part].str.replace(replace_before, replace_after, regex=True)
    return data


def data_float(dataframe, data_float_list):
    """
    Преобразуйте данные в формат float, который можно визуализировать,
    и результатом вывода будет список, состоящий из списков
    :param dataframe: Данные в формате dataframe
    :param data_float_list: Имена столбцов, которые необходимо преобразовать
    :return: list_final Выходной результат
    """
    list_final = []
    for data_float_part in data_float_list:
        list_final_part = list(float(data_float_part) for data_float_part in dataframe[data_float_part])
        list_final.append(list_final_part)
    return list_final


if __name__ == '__main__':
    # инициализировать
    translation_form = pd.read_excel('translation.xlsx', sheet_name=0)

    ####################################################################################################################
    # Визуализация данных об эпидемии за все время
    # whole data visualization
    # visualization of province data
    # visualization of shanghai data
    # get data
    shanghai_covid19_data = get_all_db_data(6379, 2)
    # shanghai data visualization
    province_visualization(shanghai_covid19_data, 'shanghai',
                           'visulation_result\\covid19_whole_data\\province_data\\1.shanghai\\')

    # visualization of jiangsu data
    # get data
    jiangsu_covid19_data = get_all_db_data(6379, 1)
    # jiangsu data visualization
    province_visualization(jiangsu_covid19_data, 'jiangsu',
                           'visulation_result\\covid19_whole_data\\province_data\\2.jiangsu\\')

    # visualization of zhejiang data
    # get data
    zhejiang_covid19_data = get_all_db_data(6379, 3)
    # zhejiang data visualization
    province_visualization(zhejiang_covid19_data, 'zhejiang',
                           'visulation_result\\covid19_whole_data\\province_data\\3.zhejiang\\')

    # visualization of 16 districts covid19 data
    # data file position
    file_position = 'raw excel data'
    filePath = 'district covid-19 data'
    name_list = os.listdir(file_position + '\\' + filePath)
    all_newly_diagnosed_data = []
    all_date_data = []
    all_district_name = []
    for i in range(len(name_list)):
        if '.xlsx' in name_list:
            district_name = name_list[i][:-5]
        else:
            district_name = name_list[i][:-4]
        district_covid19_data = get_all_db_data(6380, i)
        # # visualization of 16 districts covid19 the whole data
        # district_visualization(district_covid19_data, district_name, str(i))
        # visualization of 16 districts covid19 part data(include the date we want)
        district_visualization(district_covid19_data, district_name, str(i),
                               'visulation_result\\covid19_whole_data\\district_data\\' +
                               str(i+1) + '.' + district_name + '\\')

        all_district_name.append(district_name)
        all_date_data.append(district_covid19_data['时间'])
        all_newly_diagnosed_data.append(district_covid19_data['本土新增'])
        # инициализировать
        plt.figure(figsize=(20, 10))
        plt.subplot(111)
        # Преобразование формата данных
    for i in range(len(all_district_name)):
        x_axis_data = data_type_transform(all_date_data[i], 'date')
        y_axis_data = data_type_transform(all_newly_diagnosed_data[i], 'number')
        # Визуализация данных
        plt.plot(x_axis_data, y_axis_data, linewidth='1', label=all_district_name[i])
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_whole_data\\district_data\\'):
        os.makedirs('visulation_result\\covid19_whole_data\\district_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_whole_data\\district_data\\',
                             '16_district_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()

    ####################################################################################################################

    # Выбирать часть времени для визуализации данных об эпидемии
    # part data visualization
    # visualization of province data
    # visualization of shanghai data
    # get data
    shanghai_covid19_data = get_all_db_data(6379, 2)
    # shanghai data visualization
    province_part_visualization(shanghai_covid19_data, 'shanghai',
                                'visulation_result\\covid19_part_data\\province_data\\1.shanghai\\')

    # visualization of jiangsu data
    # get data
    jiangsu_covid19_data = get_all_db_data(6379, 1)
    # jiangsu data visualization
    province_part_visualization(jiangsu_covid19_data, 'jiangsu',
                                'visulation_result\\covid19_part_data\\province_data\\2.jiangsu\\')

    # visualization of zhejiang data
    # get data
    zhejiang_covid19_data = get_all_db_data(6379, 3)
    # zhejiang data visualization
    province_part_visualization(zhejiang_covid19_data, 'zhejiang',
                                'visulation_result\\covid19_part_data\\province_data\\3.zhejiang\\')

    # visualization of whole province data from 02.2020-09.2022
    shanghai_whole_date, shanghai_whole_diagnosed_data = select_desired_time(shanghai_covid19_data['date'],
                                                                             shanghai_covid19_data['Newly diagnosed'],
                                                                             start_data='2020-02-01 00:00:00',
                                                                             end_data='2022-09-01 00:00:00')
    jiangsu_whole_date, jiangsu_whole_diagnosed_data = select_desired_time(jiangsu_covid19_data['date'],
                                                                           jiangsu_covid19_data['Newly diagnosed'],
                                                                           start_data='2020-02-01 00:00:00',
                                                                           end_data='2022-09-01 00:00:00')
    zhejiang_whole_date, zhejiang_whole_diagnosed_data = select_desired_time(zhejiang_covid19_data['date'],
                                                                             zhejiang_covid19_data['Newly diagnosed'],
                                                                             start_data='2020-02-01 00:00:00',
                                                                             end_data='2022-09-01 00:00:00')

    # 3 province visualization(shanghai jiangsu zhejiang)
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    # Визуализация данных
    plt.plot(shanghai_whole_date, shanghai_whole_diagnosed_data, linewidth='1.5', label='shanghai whole new diagnosed')
    plt.plot(jiangsu_whole_date, jiangsu_whole_diagnosed_data, linewidth='1.5', label='jiangsu whole new diagnosed')
    plt.plot(zhejiang_whole_date, zhejiang_whole_diagnosed_data, linewidth='1.5', label='zhejiang whole new diagnosed')
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_part_data\\province_data\\'):
        os.makedirs('visulation_result\\covid19_part_data\\province_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_part_data\\province_data\\',
                             '3_province_whole_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()

    # 2 province visualization(jiangsu zhejiang)
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    # Визуализация данных
    plt.plot(jiangsu_whole_date, jiangsu_whole_diagnosed_data, linewidth='1.5', label='jiangsu whole new diagnosed')
    plt.plot(zhejiang_whole_date, zhejiang_whole_diagnosed_data, linewidth='1.5', label='zhejiang whole new diagnosed')
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_part_data\\province_data\\'):
        os.makedirs('visulation_result\\covid19_part_data\\province_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_part_data\\province_data\\',
                             '2_province_whole_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()

    # visualization of whole province data from 01.2022-09.2022
    shanghai_whole_date, shanghai_whole_diagnosed_data = select_desired_time(shanghai_covid19_data['date'],
                                                                             shanghai_covid19_data['Newly diagnosed'])
    jiangsu_whole_date, jiangsu_whole_diagnosed_data = select_desired_time(jiangsu_covid19_data['date'],
                                                                           jiangsu_covid19_data['Newly diagnosed'])
    zhejiang_whole_date, zhejiang_whole_diagnosed_data = select_desired_time(zhejiang_covid19_data['date'],
                                                                             zhejiang_covid19_data['Newly diagnosed'])

    # 3 province visualization(shanghai jiangsu zhejiang)
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    # Визуализация данных
    plt.plot(shanghai_whole_date, shanghai_whole_diagnosed_data, linewidth='1.5', label='shanghai whole new diagnosed')
    plt.plot(jiangsu_whole_date, jiangsu_whole_diagnosed_data, linewidth='1.5', label='jiangsu whole new diagnosed')
    plt.plot(zhejiang_whole_date, zhejiang_whole_diagnosed_data, linewidth='1.5', label='zhejiang whole new diagnosed')
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_part_data\\province_data\\'):
        os.makedirs('visulation_result\\covid19_part_data\\province_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_part_data\\province_data\\',
                             '3_province_part_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()

    # 2 province visualization(jiangsu zhejiang)
    # инициализировать
    plt.figure(figsize=(20, 10))
    plt.subplot(111)
    # Преобразование формата данных
    # Визуализация данных
    plt.plot(jiangsu_whole_date, jiangsu_whole_diagnosed_data, linewidth='1.5', label='jiangsu whole new diagnosed')
    plt.plot(zhejiang_whole_date, zhejiang_whole_diagnosed_data, linewidth='1.5', label='zhejiang whole new diagnosed')
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_part_data\\province_data\\'):
        os.makedirs('visulation_result\\covid19_part_data\\province_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_part_data\\province_data\\',
                             '2_province_part_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()

    # visualization of 16 districts covid19 data
    file_position = 'raw excel data'
    filePath = 'district covid-19 data'
    name_list = os.listdir(file_position + '\\' + filePath)
    part_newly_diagnosed_data = []
    part_date_data = []
    part_district_name = []
    for i in range(len(name_list)):
        if '.xlsx' in name_list:
            district_name = name_list[i][:-5]
        else:
            district_name = name_list[i][:-4]
        district_covid19_data = get_all_db_data(6380, i)
        # # visualization of 16 districts covid19 the whole data
        # district_visualization(district_covid19_data, district_name, str(i))
        # visualization of 16 districts covid19 part data(include the date we want)
        district_part_visualization(district_covid19_data, district_name, str(i),
                                    'visulation_result\\covid19_part_data\\district_data\\' +
                                    str(i+1) + '.' + district_name + '\\')
        # Выберите необходимое время
        part_date, part_diagnosed_data = select_desired_time(district_covid19_data['时间'],
                                                             district_covid19_data['本土新增'])
        part_date_data.append(part_date)
        part_district_name.append(district_name)
        part_newly_diagnosed_data.append(part_diagnosed_data)
        # инициализировать
        plt.figure(figsize=(20, 10))
        plt.subplot(111)
        # Преобразование формата данных
    for i in range(len(part_district_name)):
        x_axis_data = data_type_transform(part_date_data[i], 'date')
        y_axis_data = data_type_transform(part_newly_diagnosed_data[i], 'number')
        # Визуализация данных
        plt.plot(x_axis_data, y_axis_data, linewidth='1', label=part_district_name[i])
        # plt.plot(part_date_data[i], part_newly_diagnosed_data[i], linewidth='1', label=part_district_name[i])
    # Завершите процесс визуализации
    plt.legend()
    if not os.path.exists('visulation_result\\covid19_part_data\\district_data\\'):
        os.makedirs('visulation_result\\covid19_part_data\\district_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\covid19_part_data\\district_data\\',
                             '16_district_newly_diagnosed_data_compare.png'))
    # plt.savefig(savefig_name)
    plt.cla()
    plt.close()
