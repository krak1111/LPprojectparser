import json
import re
import time

from settings import HEADERS, BASE_URL
"""
Здесь вспомогательные функции, которые используются основными функциями парсера
"""

def get_issue_info(issn, year, session) -> list:
    """
    Функция делает запрос по году выпуска и получает json
    с информацией по выпускам этого года
    """
    year_url = f'{BASE_URL}/journal/{issn}/year/{year}/issues'

    request = session.get(year_url, headers=HEADERS)  # reply will be a JSON object

    volume_json = request.text  # get json format text

    json_object = json.loads(volume_json)  # read json

    issue_data = []

    for data in json_object["data"]:
        issue_data.append({'date': data["coverDateText"],
                           'url': data["uriLookup"]})


    return issue_data


def get_issn(page) -> str:
    """
    Функция выдает issn журнала, небходим для
    составление запроса по годам выпуска
    """
    selector = 'p.js-issn'
    issn_text = page.find(selector, first=True).text[-9:]
    issn = issn_text.replace('-', '')
    return issn

def get_volumes_year(journal_page, url, session) -> list:
    """
    Выдает список годов, когда были выпуски
    """
    try:
        last_page_num = pagination_search(journal_page)
    except AttributeError: # if only one page we have not a pagination element
        last_page_num = 1

    year_pattern = re.compile(r'^([0-9]+)')
    selector = 'span.accordion-title'
    volume_titles = journal_page.find(selector)
    years = []
    # первая страница обрабытывается как есть, что бы не делать лишних запросов
    for volume_title in volume_titles:
        years.append(year_pattern.search(volume_title.text).group())

    for page_num in range(2, last_page_num + 1):
        time.sleep(1)  # временное решение, что бы не получить бан
        journal_page = session.get(url=f'{url}?page={page_num}', headers=HEADERS).html
        volume_titles = journal_page.find(selector)

        for volume_title in volume_titles:
            years.append(year_pattern.search(volume_title.text).group())
    return years

def pagination_search(page, selector='.pagination-pages-label'):
    """
    Обработка пагинации и возвращает сколько страниц
    в пагинации
    """
    last_page_num_str = page.find(selector, first=True).text[-1]
    return int(last_page_num_str)