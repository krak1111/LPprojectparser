import json
import re
import time

from settings import HEADERS, BASE_URL

def journal_names_list(url, session) -> list:
    """
    Эта функция парсит url сабдомейна 
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
    
    absolute_url = f'{url}/issues'
    
    request = session.get(absolute_url, headers=HEADERS)
    journal_page = request.html
    issn = get_issn(journal_page)
    volume_years = search_volumes_year(journal_page,absolute_url, session)

    output_dict = {}
    for volume_year in volume_years:
        
        output_dict[f'{volume_year}'] = get_issue_info(issn,
                                                       volume_year,
                                                       session)
    return output_dict


def get_issue_info(issn, year, session) -> list:
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
    selector = 'p.js-issn'

    issn_text = page.find(selector, first=True).text[-9:]
    issn = issn_text.replace('-', '')

    return issn

def search_volumes_year(journal_page, url, session) -> list:
    
    try:
        last_page_num = pagination_search(journal_page)
    except AttributeError: # if only one page we have not a pagination element
        last_page_num = 1
    
    year_pattern = re.compile(r'^([0-9]+)')
    selector = 'span.accordion-title'
    volume_titles = journal_page.find(selector)
    years = []

    #
    for volume_title in volume_titles:
        years.append(year_pattern.search(volume_title.text).group())

    for page_num in range(2, last_page_num + 1):
        time.sleep(2)
        journal_page = session.get(url=f'{url}?page={page_num}', headers=HEADERS).html
        volume_titles = journal_page.find(selector)

        for volume_title in volume_titles:
            years.append(year_pattern.search(volume_title.text).group())
    

    return years

def pagination_search(page, selector='.pagination-pages-label'):

    last_page_num_str = page.find(selector, first=True).text[-1]
    return int(last_page_num_str)
