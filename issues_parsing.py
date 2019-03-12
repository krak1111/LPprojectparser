import re
from requests_html import *

from settings import *


JOURNAL_URL = f'{BASE_URL}/journal/advances-in-climate-change-research/issues'


def issn_search(page):
    selector = 'p.js-issn'
    issn = page.find(selector, first = True).text.replace('-','')

    return issn

def years(page):
    year_pattern = re.compile(r'^([0-9]+)')
    selector = 'span.accordion-title'

    volumes = page.find(selector)
    years = []

    for volume in volumes:
        year = year_pattern.search(volume.text).group() #Find the year from title accordint to the pattern
        years.append(year)
        print(year)

    return years



def main(url):
    session = HTMLSession()
    try:
        request = session.get(url, headers = HEADERS)
    
    except requests.exceptions.ConnectionError:
        print('Lost connection')

    page = request.html
    issn = issn_search(page)
    print(issn)
    
    publication_years = years(page)[1:] # Last year already render on the page, parse below

    


    


    

if __name__ == '__main__':
    main(JOURNAL_URL)
