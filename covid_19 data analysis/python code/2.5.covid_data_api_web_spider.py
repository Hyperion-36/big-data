"""
Мы получаем все данные об эпидемии за день на веб-сайте epidemic real-time big data report
и сохраняем данные в формате json в txt-файл.
"""
# coding:utf-8
import re
import sys
import datetime as dt
import urllib.request as urlrequest
import json
import time
import binascii
from lxml import etree
import requests


def loads_str(data_str):
    try:
        result = json.loads(data_str)
        return result
    except Exception as e:
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = data_str[int(error_index[0])]
            data_str = data_str.replace(error_str, "<?>")
            # 该处将处理结果继续递归处理
            return loads_str(data_str)


sys.setrecursionlimit(1000000)

if __name__ == '__main__':
    time_start = time.time()
    url_visit = 'https://voice.baidu.com/api/newpneumonia?from=page&callback=jsonp_1670318227608_76048'
    crawl_content = urlrequest.urlopen(url_visit).read()
    filename = str(dt.date.today()) + '_api.txt'
    file_position = "web spider data\\api txt\\"
    fn = open(file_position + filename, 'w', encoding='utf-8')
    crawl_content_str = str(crawl_content)
    fn.write(crawl_content_str)
    time_end = time.time()
    print(time_end - time_start)
    status_position = crawl_content_str.index("status")-2
    crawl_conten_new = crawl_content_str[status_position:-3]
    a = loads_str(data_str=crawl_conten_new)
    b = a['data']
    c = b['caseList']
    d = c[0]['area']
    e = d.replace('<?>', '\\')
    f = eval(repr(e).replace("\\\\", "\\"))
    g = f.encode('raw_unicode_escape').decode()
    print(g)



