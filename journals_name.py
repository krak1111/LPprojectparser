from requests_html import *

DISCIPLINES = [
    'physics-and-astronomy',
    'chemical-engineering',
    'chemistry',
    'computer-science',
    'earth-and-planetary-sciences',
    'energy',
    'engineering',
    'material-science',
    'mathematics',
]

BASE_URL = 'https://www.sciencedirect.com/'
HEADERS = {'user-agent': 'Mozilla/5.0'}

def journals_titles(disciplines, headers, base_url):
    parse_result = []
    for discipline in disciplines:
        parse_result.append({f'{discipline}' : parse(discipline, headers, base_url)})

    for title in parse_result:
        print(title)

def parse(discipline, headers, base_url):
    session = HTMLSession()
    k = 1
    last_page_num = 5
    i = 1
    titles = []

    #Pagination cycle k < 5 for garanty uninfinity cycle
    while k < 5 and i <= last_page_num:

        url = f'{base_url}browse/journals-and-books?page={i}&contentType=JL&subject={discipline}'
        request = session.get(url, headers = headers)
        html = request.html
        selector = 'a.js-publication-title > span.anchor-text' # css class anchor-text not unique for journal title

        title_elements = html.find(selector) #find all elements

        #parse titles
        for title_element in title_elements:
            title_url_form = title_element.text.lower().replace(' ', '-') #For examle: Physics and Astronomy bring to form "physics-and-astronomy"
            titles.append(title_url_form)

        #pagination check only on first iteration
        if i == 1 :
            try:
                last_page_num_str = html.find('.pagination-pages-label', first = True).text[-1]
                last_page_num = int(last_page_num_str)
            except IndexError: # if only one page we have not a pagination element
                break
        i+=1
        k+=1

    return titles

if __name__ == '__main__':
    journals_titles(DISCIPLINES, HEADERS, BASE_URL)
