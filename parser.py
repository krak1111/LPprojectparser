from secondary_functions import *
from settings import HEADERS, BASE_URL


def journal_names_list(url, session) -> list:
    """
    Эта функция парсит страницу сабдомейна
    и выводит список словарей с названиями журналов и их урлами
    """
    current_page_count = 1
    last_page_num = 1
    output_list = []

    while current_page_count <= last_page_num:

        absolute_url = f'{BASE_URL}/browse/journals-and-books?page={current_page_count}&contentType=JL&subject={url}'
        try:
            request = session.get(absolute_url, headers=HEADERS)
        except requests.exceptions.ConnectionError:
            print("No connection!")
            return False

        html = request.html
        selector = 'a.js-publication-title'  # Journal title in a > span

        journal_elements = html.find(selector)  # find all elements

        # parse titles
        for journal_element in journal_elements:
            output_list.append({'name': journal_element.text, 'url': f'{BASE_URL}{journal_element.links.pop()}'})

        # pagination check only on first iteration
        if current_page_count == 1:
            try:
                last_page_num = pagination_search(html)
            except AttributeError:  # if only one page we have not a pagination element
                break        
        current_page_count += 1

    return output_list


def issues_dict(url, session) -> dict:
    """
    Данная функция парсит серию страниц для одного журнала и
    возвращает словарь типа {'date': Дата выпуска, 'url': адресс выпуска}
    """
    absolute_url = f'{url}/issues'
    request = session.get(absolute_url, headers=HEADERS)
    journal_page = request.html
    issn = get_issn(journal_page)
    volume_years = get_volumes_year(journal_page, absolute_url, session)
    output_dict = {}
    for volume_year in volume_years:
        output_dict[f'{volume_year}'] = get_issue_info(issn, volume_year, session)

    return output_dict


def articles_list(journal_url, issue_url, session) -> list:
    """
    Эта функция парсит страницу выпуска
    и выводит список словарей с названиями статей  и url
    """
    absolute_url = f'{journal_url}{issue_url}'
    output_list = []
    request = session.get(absolute_url, headers=HEADERS)
    page = request.html
    selector = 'dl.article-content'
    articles = page.find(selector)  # Получает список экземпляров класса Elemen, удовлетворяющие поиску

    for article in articles:
        article_type = article.find('span.js-article-subtype', first=True)
        if article.find('span.js-article-subtype'):  # если присутствует характер статьи, значит это статья)
            if article_type.text != 'Erratum':
                article_element = article.find('a.article-content-title', first=True)
                output_list.append({'name': article_element.text,
                                    'url': article_element.links.pop()})

    return output_list

def article_info_dict(url, session) -> dict:
    """
    Парсит информацию о статье
    вывод в виде dict
    {'type':'', 'doi': '', 'abstract':}
    """
    absolute_url = f'{BASE_URL}{url}'
    request = session.get(absolute_url, headers=HEADERS)
    page = request.html

    doi = page.find('a.doi', first=True).text
    selector = 'div.abstract.author'
    abstract_elements = page.find(selector)
    if abstract_elements:
        abstract = ''
        for abstract_element in abstract_elements:
            abstract += abstract_element.text
        abstract.replace('\n', '')
    else:
        abstract = None

    output_dict = {'doi': doi, 'abstract': abstract}


    return output_dict
