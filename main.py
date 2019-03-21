import json
import time

import requests_html as rh

import containers
import settings
from domains_parser import format_to_json, json_handling
from parser import *
from support_func import load



def main():
    session = rh.HTMLSession()
    json_form = format_to_json(settings.file_path)
    json_loader = json.loads(json_form)
    domain_dict = json_handling(json_loader)
    # (subdomains, journals, issues, articles) = load()
    # journals_flag = True
    # issues_flag = True
    # articles_flag = True
    # if not subdomains:
    subdomains = containers.DomainsContainer(domain_dict)



    for subdomain in subdomains:
        journal_names = journal_names_list(subdomain['url'], session)
        journals = containers.SimpleContainer(journal_names)
        #print(subdomain)
        time.sleep(1)
        print(f"{subdomain}")
        for journal in journals:
            #print(journal)
            issues_info = issues_dict(journal['url'], session)
            issues = containers.IssuesContainer(issues_info)
            print(f'{" "*4}{"{"}"journal_name": "{journal["name"]}"{"}"}')
            for issue in issues:
                article_titles = articles_list(journal['url'], issue['url'], session)
                articles = containers.SimpleContainer(article_titles)
                print(f'{" "*8}{issue}')
                for article in articles:
                    article_info = article_info_dict(article['url'], session)                   
                    article_output = {'article_name': article['name']}
                    article_output.update(article_info)                    
                    print(f'{" "*12}{article_output}')                 
                    time.sleep(1)



if __name__ == '__main__':
    main()
