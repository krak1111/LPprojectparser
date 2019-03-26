import json
import os
import time

import requests_html as rh


import containers
import settings
from domains_parser import format_to_json, json_handling
import parser
import support_func as support



def journal_runner(journal, issues, file):
    """
    Проход по журналу и запись в json файл
    """
    for issue in issues:  # проход по выпускам журнала
        article_titles = parser.articles_list(journal['url'], issue['url'])
        articles = containers.SimpleContainer(article_titles)
        print(f'{" "*8}{issue}\n\n')

        for article in articles:  # проход по статьям выпуска
            article_info = parser.article_info_dict(article['url'])
            article_output = {'article_name': article['name']}
            article_output.update(article_info)
            support.pretty_dict_print(indent=" "*12, ugly_dict=article_output)
            support.write_article(issue, article_output, file)

    return article_output


def main():


    """
    Обработка json'а
    """
    json_form = format_to_json(settings.file_path)
    json_loader = json.loads(json_form)
    domain_dict = json_handling(json_loader)

    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Смена текущей директории на директории где расположен main.py
    # (subdomains, journals, issues, articles) = load()
    # journals_flag = True
    # issues_flag = True
    # articles_flag = True
    # if not subdomains:
    subdomains = containers.DomainsContainer(domain_dict)


    for subdomain in subdomains:  # проход по сабдомейнам
        journal_names = parser.journal_names_list(subdomain['url'])
        journals = containers.SimpleContainer(journal_names)
        #print(subdomain)
        print(f"{subdomain}")
        for journal in journals:
            issues_info = parser.issues_dict(journal['url'])
            issues = containers.IssuesContainer(issues_info)
            print(f'{" "*4}{"{"}"journal_name": "{journal["name"]}"{"}"}\n\n')
            try:
                os.mkdir(f"{subdomain['subdomain']}")
            except OSError:
                pass
            with open(f"{subdomain['subdomain']}/{journal['name'].replace(' ','')}.json", 'w', encoding='utf-8') as file:
                support.write_info(subdomain, journal, file)
                out = journal_runner(journal, issues, file)
                support.write_end(file)


if __name__ == '__main__':
    main()
