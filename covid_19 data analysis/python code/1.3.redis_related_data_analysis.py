"""
Мы визуализируем соответствующие данные по 16 регионам,
включая рейтинг по количеству инфекций, населению, экономике, площади земель, плотности населения и т.д.
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

    # compare 16 districts covid19 data in histogram
    # Отсортируем общее количество инфекций в каждом регионе с 15 января по 1 июля и отобразите его в виде гистограммы
    # получить данные
    file_position = 'raw excel data'
    filePath = 'district covid-19 data'
    name_list = os.listdir(file_position + '\\' + filePath)
    district_name_list = []
    diagnosis_data_list = []
    for i in range(len(name_list)):
        if '.xlsx' in name_list:
            district_name = name_list[i][:-5]
        else:
            district_name = name_list[i][:-4]
        district_covid19_data = get_all_db_data(6380, i)
        # Мы отбираем данные в течение требуемого времени
        x, y = select_desired_time(district_covid19_data['时间'], district_covid19_data['本土累计确诊'])
        district_name_list.append(district_name)
        diagnosis_data_list.append(y[-1] - y[0])
    # После сохранения данных в dataframe отсортируйте их по размеру количества заражений
    whole_diagnosis_dict = {'district_name': district_name_list, 'diagnosis_data': diagnosis_data_list}
    district_diagnosis_data = pd.DataFrame(whole_diagnosis_dict)
    district_diagnosis_data_arrange = district_diagnosis_data.sort_values(by=['diagnosis_data'], ascending=[True])
    # Сохранить отсортированный список названий регионов
    # (важные данные-необходимо использовать при анализе других данных, чтобы облегчить сравнение с данными об эпидемии)
    district_name_arrange_list = list((district_diagnosis_data_arrange['district_name']))
    # Отображение данных в виде гистограммы
    histogram_visualization(district_diagnosis_data_arrange['district_name'],
                            district_diagnosis_data_arrange['diagnosis_data'],
                            "district analysis 1.compare 16 districts.png", 'Количество подтвержденных случаев',
                            "Анализ эпидемической ситуации в различных регионах с февраля по июнь",
                            "Название района", 'visulation_result\\district_data\\')

    # анализ данные 2.2 Площадь земель, постоянное население и плотность населения каждого района (2020 год)
    # Сбор и инициализация данных
    number_22_list = []
    district_data = get_all_db_data(6379, 9)
    district_number_list = []
    district_data = dataframe_replace(district_data, '\xa0', '')
    district_name_22_list = district_data['地区']
    permanent_population_22_list = district_data['年末常住人口（万人）']
    foreign_population_22_list = district_data['外来人口']
    density_population_22_list = district_data['人口密度（人/平方公里）']
    land_area_22_list = district_data['行政区划面积（平方公里）']
    # Найди английский язык, соответствующий названию региона в переводе
    # И найдите соответствующую позицию в таблице ранжирования по количеству инфекций（district_name_arrange_list）
    for district_name_22_number in range(len(district_name_22_list) - 1):
        if district_name_22_list[district_name_22_number] != '全市':
            district_dict = data_translation(district_name_22_list[district_name_22_number])
            district_22_position = district_name_arrange_list.index(district_dict['english_name'])
            number_22_list.append(district_22_position)
    # Сохранить данные в dataframe
    district_22_dict = {'district_name_22_list': district_name_22_list[1:-1],
                        'permanent_population_22_list': permanent_population_22_list[1:-1],
                        'foreign_population_22_list': foreign_population_22_list[1:-1],
                        'density_population_22_list': density_population_22_list[1:-1],
                        'land_area_22_list': land_area_22_list[1:-1],
                        'number_22_list': number_22_list}
    district_22_dataframe_raw = pd.DataFrame(district_22_dict)
    # Измените порядок этих данных в зависимости от количества инфекций в ходе эпидемии
    district_22_dataframe = district_22_dataframe_raw.sort_values(by=['number_22_list'], ascending=[True])
    data_float_list_22 = ['permanent_population_22_list', 'foreign_population_22_list',
                          'density_population_22_list', 'land_area_22_list']
    list_final_22 = data_float(district_22_dataframe, data_float_list_22)
    (permanent_population_22_list_final, foreign_population_22_list_final, density_population_22_list_final,
     land_area_22_list_final) = (list_final_22[0], list_final_22[1], list_final_22[2], list_final_22[3])
    whole_population_22_list_final = []
    # Рассчитайте общие данные о постоянном населении плюс иностранное население
    for population_number in range(len(permanent_population_22_list_final)):
        whole_population_22 = (permanent_population_22_list_final[population_number] +
                               foreign_population_22_list_final[population_number])
        whole_population_22_list_final.append(whole_population_22)
    # Визуализация постоянного населения каждого района 各区常住人口可视化
    histogram_visualization(district_name_arrange_list,
                            permanent_population_22_list_final,
                            "district analysis 2.compare 16 districts permanent population.png",
                            'Население (единица измерения: 10000 человек)',
                            "Постоянное население каждого района",
                            "Название района", 'visulation_result\\district_data\\')

    # Визуализация иностранного населения в каждом районе 各区外来人口可视化
    histogram_visualization(district_name_arrange_list,
                            foreign_population_22_list_final,
                            "district analysis 3.compare 16 districts foreign population.png",
                            'Население (единица измерения: 10000 человек)',
                            "Иностранное население каждого района",
                            "Название района", 'visulation_result\\district_data\\')

    # Визуализация общей численности населения 总人口可视化
    histogram_visualization(district_name_arrange_list,
                            whole_population_22_list_final,
                            "district analysis 4.compare 16 districts whole population.png",
                            'Население (единица измерения: 10000 человек)',
                            "Общая численность населения каждого района",
                            "Название района", 'visulation_result\\district_data\\')

    # Визуализация плотности населения в каждом районе 各区人口密度可视化
    histogram_visualization(district_name_arrange_list,
                            density_population_22_list_final,
                            "district analysis 5.compare 16 districts density population.png",
                            'Плотность населения (чел./квадратный километр)',
                            "Плотность населения каждого района",
                            "Название района", 'visulation_result\\district_data\\')

    # Площадь земельного участка каждого района 各区土地面积
    histogram_visualization(district_name_arrange_list,
                            land_area_22_list_final,
                            "district analysis 6.compare 16 districts land area.png",
                            '',
                            "Площадь земельного участка каждого района",
                            "Название района", 'visulation_result\\district_data\\')
    # print(district_22_dataframe)

    # анализ данные 2.6 Возрастной состав зарегистрированного населения каждого района (2020 год)
    number_26_list = []
    district_data = get_all_db_data(6379, 13)
    district_number_list = []
    district_data = dataframe_replace(district_data, '\xa0', '')
    whole_population_26_list = district_data['合  计']
    district_name_26_list = district_data['地区']
    age_17_26_list = district_data['17岁及以下(万人)']
    age_34_26_list = district_data['18～34岁(万人)']
    age_59_26_list = district_data['35～59岁(万人)']
    age_60_26_list = district_data['60岁及以上(万人)']
    for district_name_26_number in range(len(district_name_26_list)):
        if district_name_26_list[district_name_26_number] != '全市':
            district_dict = data_translation(district_name_26_list[district_name_26_number])
            district_26_position = district_name_arrange_list.index(district_dict['english_name'])
            number_26_list.append(district_26_position)
    district_26_dict = {'whole_population_26_list': whole_population_26_list[1:],
                        'age_17_26_list': age_17_26_list[1:], 'age_34_26_list': age_34_26_list[1:],
                        'age_59_26_list': age_59_26_list[1:], 'age_60_26_list': age_60_26_list[1:],
                        'number_26_list': number_26_list}
    district_26_dataframe_raw = pd.DataFrame(district_26_dict)
    district_26_dataframe = district_26_dataframe_raw.sort_values(by=['number_26_list'], ascending=[True])

    data_float_list_26 = ['whole_population_26_list', 'age_17_26_list', 'age_34_26_list',
                          'age_59_26_list', 'age_60_26_list', 'number_26_list']
    list_final_26 = data_float(district_26_dataframe, data_float_list_26)
    (whole_population_26_list_final, age_17_26_list_final, age_34_26_list_final, age_59_26_list_final,
     age_60_26_list_final, number_26_list_final) = (list_final_26[0], list_final_26[1], list_final_26[2],
                                                    list_final_26[3], list_final_26[4], list_final_26[5],)
    # 各区常住人口可视化
    histogram_visualization(district_name_arrange_list,
                            whole_population_26_list_final,
                            "district analysis 7.compare 16 districts whole population"
                            "(table 2.6 (over 17 years old)).png",
                            'Население (единица измерения: 10000 человек)',
                            "Общая численность населения каждого района(2020 год(более 17 лет))",
                            "Название района", 'visulation_result\\district_data\\')

    # 图像绘制
    fig, ax = plt.subplots()
    plt.figure(figsize=(10, 10))
    bar_width = 0.2
    x_length = np.arange(16)
    tick_label = district_name_arrange_list
    b1 = plt.barh(x_length, age_17_26_list_final, bar_width, color='c', align='center',
                  label='возраст 17-26(единица измерения: 10000 человек)', alpha=0.5)
    b2 = plt.barh(x_length + bar_width, age_34_26_list_final, bar_width, tick_label=tick_label, color='b',
                  align='center', label='возраст 18-34(единица измерения: 10000 человек)', alpha=0.5)
    b3 = plt.barh(x_length + 2 * bar_width, age_59_26_list_final, bar_width, color='r', align='center',
                  label='возраст 34-59(единица измерения: 10000 человек)', alpha=0.5)
    b4 = plt.barh(x_length + 3 * bar_width, age_60_26_list_final, bar_width, color='orange', align='center',
                  label='возраст более 60(единица измерения: 10000 человек)', alpha=0.5)
    autolabel(b1)
    autolabel(b2)
    autolabel(b3)
    autolabel(b4)
    # bar_label
    plt.xlabel('Население всех возрастов')
    plt.ylabel('Название района')
    plt.xticks(x_length + bar_width / 2, tick_label)
    plt.xticks(np.arange(0, 16, 1))
    plt.title('Население всех возрастов(старше 17 лет)')
    plt.legend()
    if not os.path.exists('visulation_result\\district_data\\'):
        os.makedirs('visulation_result\\district_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\district_data\\',
                             'district analysis 8.compare 16 districts population of all ages (over 17 years old).png'))
    # plt.savefig()
    plt.subplot(111)
    plt.cla()
    plt.close()

    # анализ данные 2.12 Возрастной состав постоянного населения в ходе седьмой переписи в разбивке по регионам
    number_212_list = []
    district_data = get_all_db_data(6379, 7)
    district_number_list = []
    district_data = dataframe_replace(district_data, '\xa0', '')
    whole_population_212_list = district_data['合计']
    district_name_212_list = district_data['地  区']
    age_14_212_list = district_data['0~14岁（万人）']
    age_59_212_list = district_data['15~59岁（万人）']
    age_60_212_list = district_data['60岁及以上（万人）']
    age_65_212_list = district_data['65岁及以上（万人）']
    age_80_212_list = district_data['80岁及以上（万人）']
    for district_name_212_number in range(len(district_name_212_list)):
        if district_name_212_list[district_name_212_number] != '全市':
            district_dict = data_translation(district_name_212_list[district_name_212_number])
            district_212_position = district_name_arrange_list.index(district_dict['english_name'])
            number_212_list.append(district_212_position)
    district_212_dict = {'whole_population_212_list': whole_population_212_list[1:],
                         'age_14_212_list': age_14_212_list[1:], 'age_59_212_list': age_59_212_list[1:],
                         'age_60_212_list': age_60_212_list[1:], 'age_65_212_list': age_65_212_list[1:],
                         'age_80_212_list': age_80_212_list[1:], 'number_212_list': number_212_list}
    district_212_dataframe_raw = pd.DataFrame(district_212_dict)
    district_212_dataframe = district_212_dataframe_raw.sort_values(by=['number_212_list'], ascending=[True])
    data_float_list_212 = ['whole_population_212_list', 'age_14_212_list', 'age_59_212_list',
                           'age_60_212_list', 'age_65_212_list', 'age_80_212_list', 'number_212_list']
    list_final_212 = data_float(district_212_dataframe, data_float_list_212)
    (whole_population_212_list_final, age_14_212_list_final, age_59_212_list_final, age_60_212_list_final,
     age_65_212_list_final, age_80_212_list_final, number_212_list_final
     ) = (list_final_212[0], list_final_212[1], list_final_212[2],
          list_final_212[3], list_final_212[4], list_final_212[5], list_final_212[6])
    # 各区常住人口可视化
    histogram_visualization(district_name_arrange_list,
                            whole_population_212_list_final,
                            "district analysis 9.compare 16 districts seventh Census whole population(table 2.12).png",
                            'Население (единица измерения: 10000 человек)',
                            "Общая численность населения каждого района(Седьмая перепись)",
                            "Название района", 'visulation_result\\district_data\\')

    # 图像绘制
    fig, ax = plt.subplots()
    plt.figure(figsize=(10, 10))
    bar_width = 0.16
    x_length = np.arange(16)
    tick_label = district_name_arrange_list
    b1 = plt.barh(x_length, age_14_212_list_final, bar_width, color='c', align='center',
                  label='возраст 0-14(единица измерения: 10000 человек)', alpha=1)
    b2 = plt.barh(x_length + bar_width, age_59_212_list_final, bar_width, tick_label=tick_label, color='b',
                  align='center', label='возраст 15-59(единица измерения: 10000 человек)', alpha=1)
    b3 = plt.barh(x_length + 2 * bar_width, age_60_212_list_final, bar_width, color='r', align='center',
                  label='возраст более 60(единица измерения: 10000 человек)', alpha=1)
    b4 = plt.barh(x_length + 3 * bar_width, age_65_212_list_final, bar_width, color='orange', align='center',
                  label='возраст более 65(единица измерения: 10000 человек)', alpha=1)
    b5 = plt.barh(x_length + 4 * bar_width, age_80_212_list_final, bar_width, color='pink', align='center',
                  label='возраст более 80(единица измерения: 10000 человек)', alpha=1)
    autolabel(b1)
    autolabel(b2)
    autolabel(b3)
    autolabel(b4)
    autolabel(b5)
    # bar_label
    plt.xlabel('Население всех возрастов')
    plt.ylabel('Название района')
    plt.xticks(x_length + bar_width / 2, tick_label)
    plt.xticks(np.arange(0, 16, 1))
    plt.title('Население всех возрастов')
    plt.legend()
    if not os.path.exists('visulation_result\\district_data\\'):
        os.makedirs('visulation_result\\district_data\\')  # 如果不存在目录figure_save_path，则创建
    plt.savefig(os.path.join('visulation_result\\district_data\\',
                             'district analysis 10.compare 16 districts seventh Census population of all ages.png'))
    # plt.savefig('district analysis 10.compare 16 districts seventh Census population of all ages.png')
    plt.subplot(111)
    plt.cla()
    plt.close()

    # анализ данные 2.8 Рейтинг валового внутреннего продукта каждого округа (2021 год)
    number_28_list = []
    district_data = get_all_db_data(6379, 15)
    district_number_list = []
    district_data = dataframe_replace(district_data, '\xa0', '')
    district_name_28_list = district_data['地  区']
    gdp_list = district_data['GDP(亿元)']
    gdp_increase_list = district_data['比上年增长（%）']
    for district_name_28_number in range(len(district_name_28_list)):
        if district_name_28_list[district_name_28_number] != '全市':
            district_dict = data_translation(district_name_28_list[district_name_28_number])
            district_28_position = district_name_arrange_list.index(district_dict['english_name'])
            number_28_list.append(district_28_position)
    district_28_dict = {'gdp_list': gdp_list[1:],
                        'gdp_increase_list': gdp_increase_list[1:],
                        'number_28_list': number_28_list}
    district_28_dataframe_raw = pd.DataFrame(district_28_dict)
    district_28_dataframe = district_28_dataframe_raw.sort_values(by=['number_28_list'], ascending=[True])
    gdp_list_final = list(float(i) for i in district_28_dataframe['gdp_list'])
    gdp_increase_list_final = list(float(i) for i in district_28_dataframe['gdp_increase_list'])
    # 各区常住人口可视化
    histogram_visualization(district_name_arrange_list,
                            gdp_list_final,
                            "district analysis 11.compare 16 districts GDP.png",
                            'Валовой региональный продукт (млрд юаней)',
                            "Валовой продукт каждого района",
                            "Название района", 'visulation_result\\district_data\\')

    histogram_visualization(district_name_arrange_list,
                            gdp_increase_list_final,
                            "district analysis 12.compare 16 districts GDP increase.png", '',
                            "Темпы роста ВВП каждого района по сравнению с предыдущим годом(%)",
                            "Название района", 'visulation_result\\district_data\\')