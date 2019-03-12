from requests_html import *

from settings import *

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



def main():
    parse_pesult = []

    for discipline in DISCIPLINES:
        result = parse(discipline)
        if result:
            parse_pesult.append({f'{discipline}' : result})
        else:
            break


    print(parse_pesult)

def parse(discipline):
    session = HTMLSession()
    
    last_page_num = 5
    i = 1 # current page count
    
    journals_info = []

    #Pagination cycle k < 5 for garanty uninfinity cycle
    while i <= last_page_num:

        url = f'{BASE_URL}/browse/journals-and-books?page={i}&contentType=JL&subject={discipline}'
        
        try:
            request = session.get(url, headers = HEADERS)
        except requests.exceptions.ConnectionError:
            print("No connection!")
            return False

        html = request.html
        selector = 'a.js-publication-title' # css class anchor-text not unique for journal title

        journal_elements = html.find(selector) #find all elements

        #parse titles
        for journal_element in journal_elements:            
            journals_info.append({'Journal title' :journal_element.text, 'Journal url' : f'{BASE_URL}{journal_element.links.pop()}'})

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
    main()
