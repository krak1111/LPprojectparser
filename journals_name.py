import json
import os

from requests_html import *

from settings import *

def pagination_search(page, selector = '.pagination-pages-label'):

    last_page_num_str = page.find(selector, first = True).text[-1]
    return int(last_page_num_str)


def parse(discipline, session):
    last_page_num = 5
    current_page_count = 1 
    
    journals_info = []
 
    while current_page_count <= last_page_num:

        url = f'{BASE_URL}/browse/journals-and-books?page={current_page_count}&contentType=JL&subject={discipline}'
        
        try:
            request = session.get(url, headers = HEADERS)
        except requests.exceptions.ConnectionError:
            print("No connection!")
            return False

        html = request.html
        selector = 'a.js-publication-title' # Journal title in a > span

        journal_elements = html.find(selector) #find all elements

        #parse titles
        for journal_element in journal_elements:            
            journals_info.append({'Journal title' :journal_element.text, 'Journal url' : f'{BASE_URL}{journal_element.links.pop()}'})
            # if discipline == 'computer-science':
            #     print(f'Journal title :{journal_element.text}, Journal url : {BASE_URL}{journal_element.links.pop()}')
        #pagination check only on first iteration
        if current_page_count == 1 :
            try:                
                last_page_num = pagination_search(html)
            except IndexError: # if only one page we have not a pagination element
                break
        current_page_count += 1
    

    return journals_info

def main():
    parse_pesult = []
    session = HTMLSession()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for discipline in DISCIPLINES:
        result = parse(discipline, session)
        if result:
            parse_pesult.append({f'{discipline}' : result})

            with open(f'{discipline}.csv', 'w' , encoding = 'utf-8') as f:
                f.write('Title;Url\n')
                for journal in result:
                    f.write(f'{journal["Journal title"]};{journal["Journal url"]}\n')

        else:
            break
    

    return parse_pesult


if __name__ == '__main__':
    main()
