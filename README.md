Парсер сайта [sciencedirect](https://www.sciencedirect.com/) для web приложения [scienceforecast](http://scienceforecast.ru)
============================================================================================================================

Технологии, использующиеся в парсере:
-------------------------------------

1. [requests-html](https://github.com/kennethreitz/requests-html) -  модуль, созданный разработчиком модуля requests и включающий в себя часть функционала Beatufulsoup;
2. [Expressvpn](https://www.expressvpn.com/) - VPN сервис для предотвращения блокировки;
3. subprocess - для вызова команд expressvpn, часть кода взято с [данного репозитория](https://github.com/philipperemy/expressvpn-python), а так же для автоматического перезапуска скрипта парсера;
4. [langdetect](https://github.com/Mimino666/langdetect) - для определения лингвистической принадлежности журнала.

Структура добываемой информации:
-------------------------------

### Разделы наук имеют следующую древовидную структуру:
1. имеется четыре основных раздела науки (**primary domain**);
2. каждый из основных разделов делится разделы науки (**domain**);
3. каждый их разделов делится на подразделы (**subdomain**).

Данная информация содержится в "недрах" js кода сайта (данная часть js кода хранится в domains.json)

### Журналы так-же имеют древовидную структуру:
1. каждый журнал имеет определенную частоту "печати" - выхода выпусков (volumes);
2. в каждом выпуске публикуются статьи в полностью-открытом, частично-открытом, ограниченном доступе.

Необходимая информация
----------------------

#### Для последующей обработки, хранения, доступа к статьям неоюходимо получить следующую информацию:

1. разделы науки, к которым относится журнал;
2. название журнала;
3. данные о статьях журнала:
   - название статьи
   - doi статьи;
   - абстракт статьи;
   - дата публикации (на основе выпуска);
   - ключевые слова.

#### Промежуточная информация:

1. Ссылки для перехода на новую страницу (журнала, выпуска, статьи, поиска по поддразделу)
2. ISSN журнала (для выполния AJAX запросов и получения JSON'ов с данными о выпусках журнала)


Структура парсера
-----------------

#### Парсинг сайта производится четырьмя вложенными циклами:
1. цикл прохода по подразделам науки;
2. цикл прохода по журналам, входящим в данный подраздел;
3. цикл прохода по выпускам данного журнала (с 2010 года);
4. цикл прохода по статьям выпуска.

#### Запрос осуществляется следующим образом:
1. вызов функции поиска необходмого элемента на странице;
2. функция поиска вызывает функцию формирующую запрос, и выполняет проверку наличия данного тега (при отсутствии вызывает еще раз функцию для запроса);
3. функция формирующая запрос выполняет запрос, выполняет слудующие действия:
   - выполняет запрос на сервис (каждый запрос использует случайный user-agent);
   - производит первичную обработку ответа на предмет блокировки, если IP заблокирован - вызывает функцию смены VPN;
   - при отсутствии соединения (долгого ожидания) - вызывает функцию смены VPN;
   - каждые 400 запросов с одного VPN вызывает функцию смены VPN.

Для удобства работы с данными в циклах используются классы-контейнеры в качестве итераторов.

В связи с большим объемом информации необходимо сохранять состояние парсера, для быстрого восстановления процесса добычи информации при выключении процесса.
Данные хранятся в json формате для каждого из циклов отдельно. При первом запуске проверяется наличие данных файлов и, при их наличии, загружается состояние. При завершения итерации цикла данные обновляются.

Запись данных производится в json файл построчно с принудительной записью из буфера.