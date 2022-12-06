"""
Визуализация данных.
Мы считываем и визуализируем эпидемические данные по всем провинциям и городам, хранящиеся в базе данных.
Получите все данные о провинции или городе из базы данных, прочитайте ежедневные данные и нарисуйте картинку.
И сохраните их локально.
"""
import matplotlib.pyplot as plt
import pandas as pd
import redis
import ast
import os

# plt.rcParams['font.family'] = 'SimHei'
# plt.rcParams['font.family'] = "Times new roman"
plt.rcParams['font.size'] = 8
plt.rcParams['axes.unicode_minus'] = False
# coding:utf-8

host = '127.0.0.1'


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


def select_desired_time(x_rare, y_rare, start_data='2022-11-15 00:00:00', end_data='2022-11-26 00:00:00',
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
    :return:
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


def district_visualization(data, district_visualization_name, save_path):
    """
    Визуальный анализ данных в каждом регионе (Выберите необходимые данные по названию столбца)
    :param data: Данные в формате Dataframe
    :param district_visualization_name: Название района
    :param number: Регионы сортируются по номерам, и цифры - это числа, представленные расположением регионов
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # visualization of the whole newly diagnosed data
    visualization_date_data(data['date'], data['Newly diagnosis'],
                            district_visualization_name + "Недавно диагностированный",
                            save_path, '1.all_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_date_data(data['date'], data['Cumulative diagnosis'],
                            district_visualization_name + "Совокупный диагноз",
                            save_path, '2.all_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['date'], data['Cumulative death'],
                            district_visualization_name + "Совокупная смертность",
                            save_path, '3.all_cumulative_deaths_line.png')


def province_visualization(data, province_name, save_path):
    """
    Визуализация провинциальных и муниципальных данных (Выберите необходимые данные по названию столбца)
    :param data: Данные в формате Dataframe
    :param province_name: Название провинции
    :param save_path: Чтобы сохранить изображение в указанную папку, необходимо указать путь для его сохранения
    """
    # visualization of the whole Newly diagnosed data
    visualization_date_data(data['date'], data['Newly diagnosis'],
                            province_name + "Недавно диагностированный", save_path, '1.all_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_date_data(data['date'], data['Cumulative diagnosis'],
                            province_name + "Совокупный диагноз", save_path, '2.all_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['date'], data['Newly death'],
                            province_name + "Смерть добавила", save_path, '3.all_death_added_line.png')
    # visualization of the whole cumulative deaths data
    visualization_date_data(data['date'], data['Cumulative death'],
                            province_name + "Совокупная смертность", save_path, '4.all_cumulative_deaths_line.png')


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
    visualization_part_data(data['date'], data['Newly diagnosis'],
                            province_name + "Недавно диагностированный", save_path,
                            'province_' + province_name + '_1.part_newly_diagnosed_line.png')
    # visualization of the whole cumulative diagnosis data
    visualization_part_data(data['date'], data['Cumulative diagnosis'],
                            province_name + "Совокупный диагноз", save_path,
                            'province_' + province_name + '_2.part_cumulative_diagnosis_line.png')
    # visualization of the whole cumulative deaths data
    visualization_part_data(data['date'], data['Newly death'],
                            province_name + "Смерть добавила", save_path,
                            'province_' + province_name + '_3.part_death_added_line.png')
    # visualization of the whole cumulative deaths data
    visualization_part_data(data['date'], data['Cumulative death'],
                            province_name + "Совокупная смертность", save_path,
                            'province_' + province_name + '_4.part_cumulative_deaths_line.png')


def port_data_visualization(db_number, port):
    """
    Берем номер в соответствии с портом и указанным количеством бд, зацикливаем данные провинций, городов,
    муниципалитетов, непосредственно подчиненных центральному правительству, и районов в каждой бд и визуализируем их.
    :param db_number:Всего существует 34 региона, в первых двух портах в общей сложности 32,
                     а в последнем порту только два. Следовательно, нам нужно ограничить количество циклов db
                     (В Китае насчитывается 34 провинции или муниципалитета,
                     непосредственно подчиняющиеся центральному правительству)
    :param port: Порт базы данных, который необходимо подключить
    """
    for db in range(db_number):
        r = redis.Redis(host='127.0.0.1', port=port, db=db, decode_responses=True)
        keys = r.keys()
        print(keys)
        i = 0
        for key in keys:
            i += 1
            dataframe = pd.DataFrame(columns=["Chinese name", "English name", "Russian name",
                                              "Province or municipality directly under the Central Government",
                                              "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
                                              "Cumulative death", "Cumulative cure", "date"])
            old_value = r.get(key)
            raw_value = ast.literal_eval(old_value)
            for value_number in range(len(raw_value)):
                if value_number == 0:
                    dataframe.loc[len(dataframe)] = raw_value[value_number]
                else:
                    dataframe.loc[len(dataframe)] = raw_value[value_number][0]
            # print(dataframe)
            grade = dataframe['grade'].unique()[0]
            province = dataframe['Province or municipality directly under the Central Government'].unique()[0]
            English_name = dataframe['English name'].unique()[0]
            Chinese_name = dataframe['Chinese name'].unique()[0]
            Russian_name = dataframe['Russian name'].unique()[0]
            if grade == 'City or district':
                district_visualization(dataframe, str(Russian_name),
                                       'visulation_result\\web spider data visualization\\province_' +
                                       province + '\\' + grade + '_' + English_name + '_' +
                                       Chinese_name + '_' + Russian_name)
            else:
                province_visualization(dataframe, str(Russian_name),
                                       'visulation_result\\web spider data visualization\\province_' +
                                       province + '\\' + grade + '_' + English_name + '_' +
                                       Chinese_name + '_' + Russian_name)
            # if grade == 'City or district':
            #     grade_print = 'City'
            #     district_visualization(dataframe, str(Russian_name),
            #                            'visulation_result\\web spider data visualization\\province_' +
            #                            province + '\\' + grade + '_' + English_name)
            # else:
            #     grade_print = 'province'
            #     province_visualization(dataframe, str(Russian_name),
            #                            'visulation_result\\web spider data visualization\\province_' +
            #                            province + '\\' + grade + '_' + English_name)


if __name__ == '__main__':
    print('start visualization')
    port_data_visualization(16, 6381)
    port_data_visualization(16, 6382)
    port_data_visualization(2, 6383)

    # for db_number in range(16):
    #     r = rd = redis.Redis(host='127.0.0.1', port=6381, db=db_number, decode_responses=True)
    #     keys = r.keys()
    #     print(keys)
    #     i = 0
    #     for key in keys:
    #         i += 1
    #         dataframe = pd.DataFrame(columns=["Chinese name", "English name", "Russian name",
    #                                           "Province or municipality directly under the Central Government",
    #                                           "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
    #                                           "Cumulative death", "Cumulative cure", "date"])
    #         old_value = r.get(key)
    #         raw_value = ast.literal_eval(old_value)
    #         for value_number in range(len(raw_value)):
    #             if value_number == 0:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number]
    #             else:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number][0]
    #         # print(dataframe)
    #         grade = dataframe['grade'].unique()[0]
    #         province = dataframe['Province or municipality directly under the Central Government'].unique()[0]
    #         English_name = dataframe['English name'].unique()[0]
    #         Chinese_name = dataframe['Chinese name'].unique()[0]
    #         Russian_name = dataframe['Russian name'].unique()[0]
    #         if grade == 'City or district':
    #             province_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)
    #         else:
    #             district_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)
    #
    # for db_number in range(16):
    #     r = rd = redis.Redis(host='127.0.0.1', port=6382, db=db_number, decode_responses=True)
    #     keys = r.keys()
    #     print(keys)
    #     i = 0
    #     for key in keys:
    #         i += 1
    #         dataframe = pd.DataFrame(columns=["Chinese name", "English name", "Russian name",
    #                                           "Province or municipality directly under the Central Government",
    #                                           "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
    #                                           "Cumulative death", "Cumulative cure", "date"])
    #         old_value = r.get(key)
    #         raw_value = ast.literal_eval(old_value)
    #         for value_number in range(len(raw_value)):
    #             if value_number == 0:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number]
    #             else:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number][0]
    #         # print(dataframe)
    #         grade = dataframe['grade'].unique()[0]
    #         province = dataframe['Province or municipality directly under the Central Government'].unique()[0]
    #         English_name = dataframe['English name'].unique()[0]
    #         Chinese_name = dataframe['Chinese name'].unique()[0]
    #         Russian_name = dataframe['Russian name'].unique()[0]
    #         if grade == 'City or district':
    #             province_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)
    #         else:
    #             district_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)
    #
    # for db_number in range(2):
    #     r = rd = redis.Redis(host='127.0.0.1', port=6383, db=db_number, decode_responses=True)
    #     keys = r.keys()
    #     print(keys)
    #     i = 0
    #     for key in keys:
    #         i += 1
    #         dataframe = pd.DataFrame(columns=["Chinese name", "English name", "Russian name",
    #                                           "Province or municipality directly under the Central Government",
    #                                           "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
    #                                           "Cumulative death", "Cumulative cure", "date"])
    #         old_value = r.get(key)
    #         raw_value = ast.literal_eval(old_value)
    #         for value_number in range(len(raw_value)):
    #             if value_number == 0:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number]
    #             else:
    #                 dataframe.loc[len(dataframe)] = raw_value[value_number][0]
    #         # print(dataframe)
    #         grade = dataframe['grade'].unique()[0]
    #         province = dataframe['Province or municipality directly under the Central Government'].unique()[0]
    #         English_name = dataframe['English name'].unique()[0]
    #         Chinese_name = dataframe['Chinese name'].unique()[0]
    #         Russian_name = dataframe['Russian name'].unique()[0]
    #         if grade == 'City or district':
    #             province_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)
    #         else:
    #             district_visualization(dataframe, str(Russian_name),
    #                                    'visulation_result\\web spider data visualization\\province_' +
    #                                    province + '\\' + grade + '_' + English_name + '_' +
    #                                    Chinese_name + '_' + Russian_name)


    # # черновик
    # # инициализировать
    # translation_form = pd.read_excel('translation.xlsx', sheet_name=0)
    #
    # rs = rd = redis.Redis(host='127.0.0.1', port=6381, db=0, decode_responses=True)
    # Tibet_dataframe = pd.DataFrame(columns=["Chinese name", "English name", "Russian name",
    #                                         "Province or municipality directly under the Central Government",
    #                                         "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
    #                                         "Cumulative death", "Cumulative cure", "date"])
    # old_value = rs.get('Tibet')
    # raw_value = ast.literal_eval(old_value)
    # # print(raw_value)
    # for value_number in range(len(raw_value)):
    #     if value_number == 0:
    #         Tibet_dataframe.loc[len(Tibet_dataframe)] = raw_value[value_number]
    #     else:
    #         Tibet_dataframe.loc[len(Tibet_dataframe)] = raw_value[value_number][0]
    #
    # # print(Tibet_dataframe)
    # # visualization of Tibet data
    # # get data
    # Tibet_covid19_data = get_all_db_data(6379, 2)
    # shanghai data visualization
    # visualization_date_data(Tibet_dataframe['date'], Tibet_dataframe['Newly diagnosis'],
    #                         "Tibet Недавно диагностированный", 'visulation_result\\',
    #                         'province_Tibet_1.all_newly_diagnosed_line.png')
    # province_visualization(Tibet_dataframe, 'Tibet',
    #                        'visulation_result\\web spider data visualization\\Tibet')

