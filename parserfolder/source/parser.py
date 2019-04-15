import time

from langdetect import detect_langs

from .connection import get_request, change_vpn
from . import secondary_functions as sec
from .settings import BASE_URL


def journal_names_list(url) -> list:
    """
    Эта функция парсит страницу сабдомейна
    и выводит список словарей с названиями журналов и их урлами
    """
    current_page_count = 1
    last_page_num = 1
    output_list = []

    while current_page_count <= last_page_num:
        absolute_url = f'{BASE_URL}/browse/journals-and-books?page={current_page_count}&contentType=JL&accessType=openAccess&accessType=containsOpenAccess&subject={url}'
        selector = 'a.js-publication-title'  # Journal title in a > span

        (journal_elements, html) = sec.finder(absolute_url, selector)  # find all elements

        # parse titles
        for journal_element in journal_elements:
            output_list.append({'name': journal_element.text, 'url': f'{BASE_URL}{journal_element.links.pop()}'})

        # pagination check only on first iteration
        if current_page_count == 1:
            try:
                last_page_num = sec.pagination_search(html)
            except AttributeError:  # if only one page we have not a pagination element
                break
        current_page_count += 1

    return output_list


def issues_dict(url) -> dict:
    """
    Данная функция парсит серию страниц для одного журнала и
    возвращает словарь типа {'date': Дата выпуска, 'url': адресс выпуска}
    """
    absolute_url = f'{url}/issues'
    request = get_request(url=absolute_url)
    journal_page = request.html
    issn = sec.get_issn(journal_page)
    volume_years = sec.get_volumes_year(journal_page, absolute_url)
    output_dict = {}
    for volume_year in volume_years:
        if int(volume_year) >= 2010:
            output_dict[f'{volume_year}'] = sec.get_issue_info(issn, volume_year)
        else:
            break
        #time.sleep(0.5)
    return output_dict


def articles_list(journal_url, issue_url) -> list:
    """
    Эта функция парсит страницу выпуска
    и выводит список словарей с названиями статей  и url
    """
    absolute_url = f'{journal_url}{issue_url}'
    output_list = []
    selector = 'dl.article-content'
    (articles, _) = sec.finder(absolute_url, selector) # Получает список экземпляров класса Element, удовлетворяющие поиску

    for article in articles:
        article_type = article.find('span.js-article-subtype', first=True)
        if article_type:  # если присутствует характер статьи, значит это статья)
            if article_type.text != 'Erratum':
                article_element = article.find('a.article-content-title', first=True)
                output_list.append({'name': article_element.text.replace('\n', ''),
                                    'url': article_element.links.pop()})

    return output_list

def article_info_dict(url) -> dict:
    """
    Парсит информацию о статье
    вывод в виде dict
    {'type':'', 'doi': '', 'abstract':}
    """
    absolute_url = f'{BASE_URL}{url}'

    selector = 'a.doi'
    (doi, page) = sec.finder(absolute_url, selector, first=True)
    doi = doi.text

    selector = 'div.abstract.author>div>p'
    abstract_elements = page.find(selector)
    if abstract_elements:
        abstract = ''
        for abstract_element in abstract_elements:
            abstract += abstract_element.text.replace('\n', ' ')
        abstract.replace('\n', ' ')
        abstract.replace('"', "'")
    else:
        return None

    selector = 'div.keyword'
    keyword_elements = page.find(selector)
    if keyword_elements:
        keywords = []
        for keyword_element in keyword_elements:
            keywords.append(keyword_element.text.replace('\n', ' '))

    else:
        keywords = None
    output_dict = {'doi': doi, 'abstract': abstract, 'keywords': keywords}


    return output_dict

def is_not_english(journal):
    """
    Определение языка определяется по первому названию статьи
    на главной странице журнала
    """
    selector = 'h3.text-m'
    (element, _) = sec.finder(journal['url'], selector, first=True)
    article_name = element.text
    detect = detect_langs(article_name)
    if detect[0].lang != 'en' and detect[0].prob < 0.85:
        return True
    return False
