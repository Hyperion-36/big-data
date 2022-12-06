"""
Мы получаем все данные об эпидемии за день на веб-сайте epidemic real-time big data report
и сохраняем данные в формате json в txt-файл.
"""
# coding:utf-8
import sys
import datetime as dt
from lxml import etree
import requests


sys.setrecursionlimit(1000000)

if __name__ == '__main__':
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url=url, headers=headers).text
    # Генерировать данные стандартного веб-формата (生成标准网页格式数据)
    html = etree.HTML(response)
    # Использовать xpath для получения данных страницы в формате json
    json_text = html.xpath('//script[@type="application/json"]/text()')
    json_text = json_text[0]
    # Получить сегодняшнюю дату, сохранить полученные нами данные в формате json в текстовый файл
    filename = str(dt.date.today()) + '.txt'
    file_position = "web spider data\\json in txt\\"
    fn = open(file_position + filename, 'w', encoding='utf-8')
    fn.write(json_text)
    fn.close()

