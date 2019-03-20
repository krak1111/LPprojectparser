import json
import requests_html as rh
import time

import containers
import settings
from domains_parser import format_to_json, json_handling
from parser import journal_names_list, issues_dict


def main():
    session = rh.HTMLSession()
    json_form = format_to_json(settings.file_path)
    json_loader = json.loads(json_form)
    domain_dict = json_handling(json_loader)
    subdomains = containers.DomainsContainer(domain_dict)

    for subdomain in subdomains:        
        journal_names = journal_names_list(subdomain['url'], session)
        journals = containers.SimpleContainer(journal_names)
        #print(subdomain)
        time.sleep(1)

        for journal in journals:
            #print(journal)
            issues_info = issues_dict(journal['url'],session)
            issues = containers.IssuesContainer(issues_info)

            for issue in issues:
                print(f"{subdomain}")
                print(f'{" "*4}{journal}')
                print(f'{" "*8}{issue}')


if __name__ == '__main__':
    main()