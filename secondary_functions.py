import json
import re

from settings import BASE_URL, DATE_DICT
from connection import get_request, change_vpn
"""
Здесь вспомогательные функции, которые используются основными функциями парсера
"""

def get_issue_info(issn, year) -> list:
    """
    Функция делает запрос по году выпуска и получает json
    с информацией по выпускам этого года
    """
    absolute_url = f'{BASE_URL}/journal/{issn}/year/{year}/issues'

    request = get_request(url=absolute_url)  # reply will be a JSON object

    volume_json = request.text  # get json format text

    json_object = json.loads(volume_json)  # read json

    issue_data = []

    for data in json_object["data"]:
        issue_data.append({'date': to_date_format(data["coverDateText"]),
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

def get_volumes_year(journal_page, url) -> list:
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
        absolute_url = f'{url}?page={page_num}'
        (volume_titles, _) = finder(absolute_url, selector)

        for volume_title in volume_titles:
            years.append(year_pattern.search(volume_title.text).group())
    return years

def pagination_search(page, selector='.pagination-pages-label'):
    """
    Обработка пагинации и возвращает сколько страниц
    в поисковом запросе
    """
    last_page_num_str = page.find(selector, first=True).text[-1]
    return int(last_page_num_str)

def finder(url, selector, first=False):
    """
    Выводит кортеж из искомого элента/ов и страницу
    При отстутсвии делает еще запрос и так 6 раз,
    2 и 5 раз меняет VPN
    """
    i = 0
    while i <= 6:
        request = get_request(url)
        html = request.html
        output_elements = html.find(selector, first=first)
        if output_elements:
            return (output_elements, html)
        print(f'selector {selector} problems')
        if i%3 == 2:
            change_vpn()
        i += 1
    print(f'{html}')


def to_date_format(date):
    """
    Функция переводит дату в форматЖ Month_ID-Year
    из форматов Date Month Year, Year, Season Year
    """
    month_pattern = re.compile(r"([A-Za-z]+) $")

    year = date[-4:]
    
    month_group = month_pattern.findall(date[:-4])
    if month_group:
        month = DATE_DICT[month_group[0]]

        return f'{month}-{year}'
    else:
        return f'01-{year}'
