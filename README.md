# big-data
## redis
Файл redis содержит все порты 6379, 6380, 6381, 6382 и 6383 redis на главной стороне.Вы можете напрямую открыть соответствующий порт, нажав на файл bat.Например, дважды щелкните redis_run_6379 в первый раз.bat откроет базу данных портов 6379.После повторного двойного щелчка откроется командное окно, и база данных может быть обработана по мере необходимости.Например, введите "flushall", чтобы очистить все содержимое базы данных.

## python code
### raw excel data
Все исходные данные для анализа и визуализации данных об эпидемии в Шанхае.

### Web spider data
Информация, ежедневно получаемая с веб-сайта Baidu, предоставляющего отчеты об эпидемии больших данных в режиме реального времени.И мы сохранили файл Excel с необходимой нам информацией.

### visulation_result
Где сохранить все визуальные образы
#### covid19_part_data
Мы отбираем данные за часть периода времени. Здесь мы выбираем все данные с января по июль 2022 года.
#### covid19_whole_data
Визуализация всех эпидемических данных
#### district_data
Визуализация информации, связанной с Шанхаем (население, экономика, площадь земли и т.д.)
#### web spider data visualization
После получения ежедневных данных об эпидемии визуализируются данные по каждому региону.

### Тема 1
#### translation.xlsx
Вся информация о переводе, необходимая для темы 1.Предоставьте переводы на китайский, английский и русский языки для тех частей, которые мы хотим перевести.

#### 1.1.	redis_data_read.py
Сохраните данные из файла Excel в базе данных redis.
Сначала нам нужно открыть порты базы данных redis 6379 и 6380.
Мы считываем данные в разных местах файла raw excel data отдельно и сохраняем их в разных местах на разных портах.
Среди них в DB1-DB15 порта 6379 сначала хранятся данные об эпидемии в провинциях Шанхай, Чжэцзян и Цзянсу.После этого были сохранены соответствующие данные из различных регионов Шанхая.
Порт 6380 хранит все данные, связанные с эпидемией, в 16 регионах Шанхая.
Местоположение, имя, перевод имени и другая информация из этих таблиц хранятся в db0 на порту 6379.И эта информация также сохраняется в виде excel в локальном файле "0.file_all_информация.xlsx" внутри.

#### 1.2.redis_covid_data_analysis.py
Мы визуализируем все данные, связанные с эпидемией. Включая все эпидемиологические данные из Цзянсу, Чжэцзяна,  Шанхая и 16 регионов Шанхая.

#### 1.3.redis_related_data_analysis.py
Мы визуализируем соответствующие данные по 16 регионам, включая рейтинг по количеству инфекций, населению, экономике, площади земель, плотности населения и т.д.

### Тема 2
#### 2.1.covid_data_web_spider.py
Мы получаем все данные об эпидемии за день на веб-сайте epidemic real-time big data report(https://voice.baidu.com/act/newpneumonia/newpneumonia) и сохраняем данные в формате json в txt-файл.

#### 2.2.web spider data txt to excel.py
просматриваем файл txt, сохраненный в файле, выбираем часть данных, которую мы хотим проанализировать, и сохраняем ее в соответствующем excel.

#### 2.3.web spider data excel to redis.py
Открываем порты 6381, 6382 и 6383.Считываем все данные из excel в базу данных redis.Сохраняйте данные в провинциях или муниципалитетах, непосредственно подчиненных центральному правительству.Сохраните данные провинции или муниципалитета непосредственно под управлением центрального правительства в рамках DB.Каждый день все соответствующие данные по региону будут сохраняться в виде списка, и каждый дополнительный день будет добавляться новый список.

#### 2.4.redis_web spider data analysis and visualization.py
Визуализация данных.Мы считываем и визуализируем эпидемические данные по всем провинциям и городам, хранящиеся в базе данных.
Получите все данные о провинции или городе из базы данных, прочитайте ежедневные данные и нарисуйте картинку.И сохраните его локально.

#### 2.5.covid_data_api_web_spider.py
Мы получаем данные об эпидемии через URL-адрес API
(https://voice.baidu.com/api/newpneumonia?from=page&callback=jsonp_1670318227608_76048 ). Этот метод занимает в два раза больше времени для получения данных json, чем метод 2.1, описанный выше..

#### 2.6.web spider api data txt to excel.py
Мы извлекаем нужный нам контент из данных формата json, полученных через URL API, и сохраняем его в excel.Форма сохранения в провинциях, городах и регионах такая же, как и выше.Разница в том, что приведенные выше данные отображаются непосредственно на китайском языке. Здесь китайские данные необходимо преобразовать в кодировку unicode с помощью encode. (например：‘<?>xe8<?>xa5<?>xbf<?>xe8<?>x97<?>x8f’ ‘西藏’).


spider data translation.xlsx
Вся информация о переводе, необходимая для темы 2.Предоставьте переводы на китайский, английский и русский языки для тех частей, которые мы хотим перевести.
