import csv
import json
import re
import time

from requests_html import *

from settings import *
from journals_name import pagination_search

# JOURNAL_URL = f'{BASE_URL}/journal/advances-in-climate-change-research/issues'


def issn_search(page):
    selector = 'p.js-issn'
    issn_pattern = re.compile(r'([0-9]+)-([0-9]+)')

    issn_text = page.find(selector, first = True).text
    issn = issn_pattern.search(issn_text).group().replace('-', '')

    return issn


def years(page, url, session):
    year_pattern = re.compile(r'^([0-9]+)')
    try:
        last_page_num = pagination_search(page)
    except IndexError: # if only one page we have not a pagination element
        last_page_num = 1

    all_years = []
    selector = 'span.accordion-title'
    volumes = page.find(selector)

    for volume in volumes:
        year = year_pattern.search(volume.text).group() #Find the year from title accordint to the pattern
        all_years.append(year)

    for page_num in range(2, last_page_num + 1):
        time.sleep(3)
        new_page = session.get(url=f'{url}?page={page_num}', headers=HEADERS).html
        volumes = page.find(selector)

        for volume in volumes:
            year = year_pattern.search(volume.text).group()  # Find the year from title accordint to the pattern
            all_years.append(year)

    return all_years


def year_parsing(issn, year, session):

    year_url = f'{BASE_URL}/journal/{issn}/year/{year}/issues'

    request = session.get(url=year_url, headers=HEADERS)  # reply will be a JSON object

    volume_json = request.text  # get json format text

    json_object = json.loads(volume_json)  # read json

    issue_data = []

    for data in json_object["data"]:
        issue_name = data["volIssueSupplementText"]
        issue_url = data["uriLookup"]
        issue_data.append({'name': issue_name, 'url': issue_url})

    return issue_data


def main():
    session = HTMLSession()
    with open(f'{DISCIPLINES[0]}.csv', 'r', encoding='utf-8', newline="") as f_read:
        reader_csv = csv.DictReader(f_read, delimiter=';')
        i = 0
        for line in reader_csv:
            print(line)
            url = f"{line['Url']}/issues"
            try:
                request = session.get(url=url, headers=HEADERS)

            except requests.exceptions.ConnectionError:
                print('Lost connection')

            page = request.html
            issn = issn_search(page)
            print(issn)

            publication_years = years(page=page, url=f"{line['Url']}/issues", session=session)
            print(publication_years)

            with open(f'{line["Title"]}.csv', 'w', encoding='utf-8', newline='') as f_write:
                f_write = csv.writer(f_write, delimiter = ";")
                f_write.writerow(["Issue","Url"])
                for year in publication_years:
                    year_issues = year_parsing(issn = issn, year = year, session = session)
                    for issue in year_issues:
                        f_write.writerow([f"{year} {issue['name']}", f"{issue['url']}"])
                        print(f"{year} {issue['name']} :   {issue['url']}")
                        time.sleep(2) # I don't want to ban

            if i == 2:
                break
            else:
                i += 1


if __name__ == '__main__':
    main()
