"""
Открываем порты 6381, 6382 и 6383.
Считываем все данные из excel в базу данных redis. Сохраняйте данные в провинциях или муниципалитетах,
непосредственно подчиненных центральному правительству. Сохраните данные провинции
или муниципалитета непосредственно под управлением центрального правительства в рамках BD.
Каждый день все соответствующие данные по региону будут сохраняться в виде списка,
и каждый дополнительный день будет добавляться новый список.
"""
import pandas as pd
import redis
import ast
import os


def port_data_visualization(r, element):
    """
    Выделим в таблице каждую отдельную провинцию или муниципалитет,
    непосредственно подчиняющиеся центральному правительству, и сохраните их в соответствующей базе данных
    :param r: Подключенная база данных
    :param element: Название одного региона при распространении названий 34 провинций или муниципалитетов,
                    непосредственно подчиняющихся центральному правительству
    """
    part_dataframe = dataframe_file.loc[
        dataframe_file['Province or municipality directly under the Central Government'] == element]
    area_name = part_dataframe['English name'].unique()
    for area_name_number in range(len(area_name)):
        key = area_name[area_name_number]
        new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
        old_value = r.get(str(key))
        if old_value:
            raw_value = ast.literal_eval(old_value)
            raw_value.append(new_value)
            r.set(str(key), str(raw_value))
        else:
            value = new_value
            r.set(str(key), str(value))


if __name__ == '__main__':
    translation_form = pd.read_excel('translation.xlsx', sheet_name=0)

    excel_file_position = "web spider data\\excel\\"
    nameList = os.listdir(excel_file_position)
    for i in range(len(nameList)):
        excel_file_name = nameList[i]
        excel_name = excel_file_position + excel_file_name
        dataframe_file = pd.read_excel(excel_name, sheet_name=0)
        elements = dataframe_file['Province or municipality directly under the Central Government'].unique()
        i = 0
        for number in range(0, 16):
            element_name = elements[number]
            rs = redis.Redis(host='127.0.0.1', port=6381, db=number, decode_responses=True)
            port_data_visualization(rs, element_name)

        for number in range(16, 32):
            element_name = elements[number]
            rs = redis.Redis(host='127.0.0.1', port=6382, db=number-16, decode_responses=True)
            port_data_visualization(rs, element_name)

        for number in range(32, 34):
            element_name = elements[number]
            rs = redis.Redis(host='127.0.0.1', port=6383, db=number-32, decode_responses=True)
            port_data_visualization(rs, element_name)

        # for number in range(0, 16):
        #     element_name = elements[number]
        #     rs = redis.Redis(host='127.0.0.1', port=6381, db=number, decode_responses=True)
        #     part_dataframe = dataframe_file.loc[
        #         dataframe_file['Province or municipality directly under the Central Government'] == element_name]
        #     area_name = part_dataframe['English name'].unique()
        #     for area_name_number in range(len(area_name)):
        #         key = area_name[area_name_number]
        #         new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
        #         old_value = rs.get(str(key))
        #         if old_value:
        #             raw_value = ast.literal_eval(old_value)
        #             raw_value.append(new_value)
        #             rs.set(str(key), str(raw_value))
        #         else:
        #             value = new_value
        #             rs.set(str(key), str(value))
        #
        # for number in range(16, 32):
        #     element_name = elements[number]
        #     rs = redis.Redis(host='127.0.0.1', port=6382, db=number-16, decode_responses=True)
        #     part_dataframe = dataframe_file.loc[
        #         dataframe_file['Province or municipality directly under the Central Government'] == element_name]
        #     area_name = part_dataframe['English name'].unique()
        #     for area_name_number in range(len(area_name)):
        #         key = area_name[area_name_number]
        #         new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
        #         old_value = rs.get(str(key))
        #         if old_value:
        #             raw_value = ast.literal_eval(old_value)
        #             raw_value.append(new_value)
        #             rs.set(str(key), str(raw_value))
        #         else:
        #             value = new_value
        #             rs.set(str(key), str(value))
        #
        # for number in range(32, 34):
        #     element_name = elements[number]
        #     rs = redis.Redis(host='127.0.0.1', port=6383, db=number-32, decode_responses=True)
        #     part_dataframe = dataframe_file.loc[
        #         dataframe_file['Province or municipality directly under the Central Government'] == element_name]
        #     area_name = part_dataframe['English name'].unique()
        #     for area_name_number in range(len(area_name)):
        #         key = area_name[area_name_number]
        #         new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
        #         old_value = rs.get(str(key))
        #         if old_value:
        #             raw_value = ast.literal_eval(old_value)
        #             raw_value.append(new_value)
        #             rs.set(str(key), str(raw_value))
        #         else:
        #             value = new_value
        #             rs.set(str(key), str(value))

    # for element in range(0, 15):
    #     element_name = elements[element]
    #     if element < 15:
    #         for number in range(0, 15):
    #             rs = rd = redis.Redis(host='127.0.0.1', port=6381, db=number, decode_responses=True)
    #             part_dataframe = dataframe_file.loc[
    #             dataframe_file['Province or municipality directly under the Central Government'] == element_name]
    #             area_name = part_dataframe['English name'].unique()
    #             for area_name_number in range(len(area_name)-1):
    #                 key = area_name[area_name_number]
    #                 new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
    #                 old_value = rs.get(str(key))
    #                 if old_value:
    #                     raw_value = ast.literal_eval(old_value)
    #                     raw_value.append(new_value)
    #                     rs.set(str(key), str(raw_value))
    #                 else:
    #                     value = new_value
    #                     rs.set(str(key), str(value))
    #     elif 16 < element < 32:
    #         for number in range(0, 15):
    #             rs = rd = redis.Redis(host='127.0.0.1', port=6382, db=number, decode_responses=True)
    #             part_dataframe = dataframe_file.loc[
    #             dataframe_file['Province or municipality directly under the Central Government'] == element_name]
    #             area_name = part_dataframe['English name'].unique()
    #             for area_name_number in range(len(area_name)-1):
    #                 key = area_name[area_name_number]
    #                 new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
    #                 old_value = rs.get(str(key))
    #                 if old_value:
    #                     raw_value = ast.literal_eval(old_value)
    #                     raw_value.append(new_value)
    #                     rs.set(str(key), str(raw_value))
    #                 else:
    #                     value = new_value
    #                     rs.set(str(key), str(value))
    #     else:
    #         for number in range(0, 1):
    #             rs = rd = redis.Redis(host='127.0.0.1', port=6383, db=number, decode_responses=True)
    #             part_dataframe = dataframe_file.loc[
    #             dataframe_file['Province or municipality directly under the Central Government'] == element_name]
    #             area_name = part_dataframe['English name'].unique()
    #             for area_name_number in range(len(area_name)-1):
    #                 key = area_name[area_name_number]
    #                 new_value = part_dataframe.loc[part_dataframe['English name'] == key].values.tolist()
    #                 old_value = rs.get(str(key))
    #                 if old_value:
    #                     raw_value = ast.literal_eval(old_value)
    #                     raw_value.append(new_value)
    #                     rs.set(str(key), str(raw_value))
    #                 else:
    #                     value = new_value
    #                     rs.set(str(key), str(value))

    # # df_bytes = pickle.dumps(dataframe_file)
    # import pyarrow as pa
    # context = pa.default_serialization_context()
    # rs.set("test_df1", context.serialize(dataframe_file).to_buffer().to_pybytes())

    # rs.set('test_df', df_bytes)
    # df_bytes_from_redis = rs.get('test_df')
    # df_from_redis = pickle.loads(df_bytes_from_redis)

    # # district data(population,age, area...)
    # filePath = 'district data'
    # nameList = os.listdir(file_position + '\\' + filePath)
    # for i in range(len(nameList)):
    #     xls_name = file_position + '\\' + filePath + '\\' + nameList[i]
    #     redis_data_save(nameList[i], xls_name, '127.0.0.1', 6379, i+4)
    #     # print('the file ' + nameList[i] + 'is in db' + str(i+4))
    #
    # # district covid19 data(16 district) data read in redis port 6380
    # print('Start read data of district covid19 data')
    # filePath = 'district covid-19 data'
    # nameList = os.listdir(file_position + '\\' + filePath)
    # for i in range(len(nameList)):
    #     xls_name = file_position + '\\' + filePath + '\\' + nameList[i]
    #     redis_data_save(nameList[i], xls_name, '127.0.0.1', 6380, i)
    #
    # file_all_dict = {'file path': file_list, 'file name': file_name_list,
    #                  'file_chinese_name': file_chinese_name_list,
    #                  'file_english_name': file_english_name_list,
    #                  'file_russian_name': file_russian_name_list,
    #                  'ip name': ip_list, 'port name': port_list, 'db name': db_list}
    # file_all_dataframe = pd.DataFrame(file_all_dict)
    # file_all_dataframe.to_excel('0.file_all_information.xlsx')
    # redis_data_save('-', '0.file_all_information.xlsx', '127.0.0.1', 6379, 0)
