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

BASE_URL = 'https://www.sciencedirect.com'
HEADERS = {'user-agent': 'Mozilla/5.0'}

def journals_titles(disciplines, headers, base_url):
    parse_pesult = []

    for discipline in disciplines:
        parse_pesult.append({f'{discipline}' : parse(discipline, headers, base_url)})

    print(parse_pesult)

def parse(discipline, headers, base_url):
    session = HTMLSession()
    k = 1
    last_page_num = 5
    i = 1
    
    journals_info = []

    #Pagination cycle k < 5 for garanty uninfinity cycle
    while i <= last_page_num:

        url = f'{base_url}/browse/journals-and-books?page={i}&contentType=JL&subject={discipline}'
        request = session.get(url, headers = headers)
        html = request.html
        selector = 'a.js-publication-title' # css class anchor-text not unique for journal title

        journal_elements = html.find(selector) #find all elements

        #parse titles
        for journal_element in journal_elements:            
            journals_info.append({'Journal title' :journal_element.text, 'Journal url' : f'{base_url}{journal_element.links.pop()}'})

        #pagination check only on first iteration
        if i == 1 :
            try:
                last_page_num_str = html.find('.pagination-pages-label', first = True).text[-1]
                last_page_num = int(last_page_num_str)
            except IndexError: # if only one page we have not a pagination element
                break
        i+=1
    

    return journals_info




if __name__ == '__main__':
    journals_titles(DISCIPLINES, HEADERS, BASE_URL)
