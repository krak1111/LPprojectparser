import re
import time
import json


from requests_html import *

from settings import *



JOURNAL_URL = f'{BASE_URL}/journal/advances-in-climate-change-research/issues'


def issn_search(page):
    selector = 'p.js-issn'
    issn_pattern = re.compile(r'([0-9]+)-([0-9]+)')

    issn_text = page.find(selector, first = True).text
    issn = issn_pattern.search(issn_text).group().replace('-','')

    return issn

def years(page):
    year_pattern = re.compile(r'^([0-9]+)')
    selector = 'span.accordion-title'

    volumes = page.find(selector)
    years = []

    for volume in volumes:
        year = year_pattern.search(volume.text).group() #Find the year from title accordint to the pattern
        years.append(year)
        
    return years

def last_year_parsing(page, year):
    selector = 'div.issue-item > a.anchor' 

    volume = page.find(selector)

    issue_list = []

    for issue in volume:
        issue_dict = {'name': f'{issue.text}', 'url' : f'{issue.links.pop()}'}
        issue_list.append(issue_dict)
        
    return issue_list


def others_years_parsing(issn, years):
    session = HTMLSession()
    volume_data = []
    for year in years:
        year_url = f'{BASE_URL}/journal/{issn}/year/{year}/issues'
        print(year_url)
        request = session.get(year_url, headers = HEADERS) #reply will be a JSON object
        
        volume_json = request.text #get json format text
       
        json_object = json.loads(volume_json) #read json
        
        issue_data = []

        for data in json_object["data"]:
            issue_name = data["volIssueSupplementText"]
            issue_url = data["uriLookup"]
            issue_data.append({'name' : issue_name, 'url' : issue_url})
            
        
        volume_data.append({f'{year}' : issue_data})
        time.sleep(30) # I don't want to ban

    return volume_data        


def main(url):
    session = HTMLSession()

    try:
        request = session.get(url, headers = HEADERS)
    
    except requests.exceptions.ConnectionError:
        print('Lost connection')

    page = request.html
    issn = issn_search(page)
    print(issn)
    
    publication_years = years(page) 

    last_year = publication_years.pop(0) # Last year already render on the page, parse below

    issues = [{f'{last_year}': last_year_parsing(page, last_year)}]

    issues.append(others_years_parsing(issn, publication_years))
    

if __name__ == '__main__':
    main(JOURNAL_URL)
