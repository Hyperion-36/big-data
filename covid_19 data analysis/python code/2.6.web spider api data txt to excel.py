"""
Просматриваем файл txt, сохраненный в файле,
выбираем часть данных, которую мы хотим проанализировать, и сохраняем ее в соответствующем excel.
"""
# coding:utf-8
import pandas as pd
import sys
import openpyxl
import json
import os
import re

sys.setrecursionlimit(1000000)

# txt_file_position = "web spider data\\json in txt\\"
# txt_file_name = '2022-11-25'
# f = open(txt_file_position + txt_file_name + ".txt", encoding="utf-8")


def encoding_conversion(content):
    if '<?>' in content:
        content = content.replace('<?>', '\\')
    content_new = eval(repr(content).replace("\\\\", "\\"))
    content_final = content_new.encode('raw_unicode_escape').decode()
    return content_final


def loads_str(data_str):
    try:
        result = json.loads(data_str)
        return result
    except Exception as e:
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = data_str[int(error_index[0])]
            data_str = data_str.replace(error_str, "<?>")
            return loads_str(data_str)


if __name__ == '__main__':
    print('start to read txt data and save in excel')

# инициализировать
translation_form = pd.read_excel('spider data translation.xlsx', sheet_name=0)
txt_file_position = "web spider data\\api txt\\"
nameList = os.listdir(txt_file_position)
for i in range(len(nameList)):
    if ".txt" in nameList[i]:
        txt_file_name = nameList[i][:-4]
    else:
        txt_file_name = nameList[i]
    f = open(txt_file_position + txt_file_name + ".txt", encoding="utf-8")
    json_text = f.read()
    status_position = json_text.index("status") - 2
    crawl_conten_new = json_text[status_position:-3]
    result = loads_str(data_str=crawl_conten_new)
    # Получить все данные об эпидемии внутри страны
    result = result['data']
    result = result['caseList']

    # Мы создаем рабочую книгу
    wb = openpyxl.Workbook()
    # Создаем рабочую книгу ws = wb.active
    ws = wb.active
    # Мы задаем заголовок таблицы
    wb.title = "Epidemic in China"
    # Заголовок записи
    ws.append(["Chinese name", "English name", "Russian name",
               "Province or municipality directly under the Central Government",
               "grade", "Newly diagnosis", "Newly death", "Cumulative diagnosis",
               "Cumulative death", "Cumulative cure", "date"])
    # Получите данные из различных провинций и муниципалитетов,
    # непосредственно подчиняющихся центральному правительству, и напишите
    for province in result:
        name_province = encoding_conversion(province["area"])
        if name_province in list(translation_form.Chinese):
            file_position = translation_form[translation_form.Chinese == name_province].index.tolist()[0]
            chinese_name = translation_form['Chinese'][file_position:file_position + 1].values[0]
            english_name = translation_form['English'][file_position:file_position + 1].values[0]
            russian_name = translation_form['Russian'][file_position:file_position + 1].values[0]
            province_name = [chinese_name, english_name, russian_name, name_province,
                             'Province or municipality directly under the Central Government',
                             province["confirmedRelative"], province["diedRelative"],
                             province["confirmed"], province["died"], province["crued"], txt_file_name]
            province_name = ['0' if i == '' else i for i in province_name]
            ws.append(province_name)
            # Мы считываем данные по городам или регионам, расположенным ниже провинций и муниципалитетов,
            # непосредственно подчиненных центральному правительству, и пишем
            city_dict = province['subList']
            for city in city_dict:
                name_city = encoding_conversion(city["city"])
                if name_city in list(translation_form.Chinese):
                    file_position = translation_form[translation_form.Chinese == name_city].index.tolist()[0]

                    chinese_name = translation_form['Chinese'][file_position:file_position + 1].values[0]
                    english_name = translation_form['English'][file_position:file_position + 1].values[0]
                    russian_name = translation_form['Russian'][file_position:file_position + 1].values[0]
                    city_name = [chinese_name, english_name, russian_name, name_province, 'City or district',
                                 city["confirmedRelative"], '0',
                                 city["confirmed"], city["died"], city["crued"], txt_file_name]
                    city_name = ['0' if i == '' else i for i in city_name]
                    ws.append(city_name)
                # Предотвратите обновление данных именами, которые не появлялись ранее.
                # Поэтому имена, которые не появлялись, будут распечатаны здесь для добавления.
                else:
                    print('city ' + city["city"] + 'not in translation form,please add.From ' + province["area"])
        # Предотвратите обновление данных именами, которые не появлялись ранее.
        # Поэтому имена, которые не появлялись, будут распечатаны здесь для добавления.
        else:
            print('province ' + province["area"] + 'not in translation form,please add.From ' + province["area"])
    # 保存到excel中
    excel_file_position = "web spider data\\api excel\\"
    excel_name = excel_file_position + txt_file_name + '_data_spider.xlsx'
    # excel_name = txt_file_name + '_data_spider.xlsx'
    wb.save(excel_name)
    print(excel_name + 'saved')

# import pandas as pd
# data = pd.read_excel('2022-11-23_data_spider.xlsx', sheet_name=0)
# # print(data)
