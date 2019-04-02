import json
import os
import time

from langdetect import detect_langs

from connection import get_recommend_vpn_list, get_all_vpn_list
import containers
import settings
from domains_parser import format_to_json, json_handling
import parser
import support_func as support



def journal_runner(journal, issues, file, load_status):
    """
    Проход по журналу и запись в json файл
    """

    for issue in issues:  # проход по выпускам журнала
        last = False
        if load_status['articles']:
            try:
                with open('statement/articles', 'r') as f:
                    content = f.read()
                articles = containers.SimpleContainer(json.loads(content))
            except FileNotFoundError:
                article_titles = parser.articles_list(journal['url'], issue['url'])
                articles = containers.SimpleContainer(article_titles)
            finally:
                load_status['articles'] = False
        else:
            article_titles = parser.articles_list(journal['url'], issue['url'])
            articles = containers.SimpleContainer(article_titles)
        print(f'{" "*8}{issue}\n\n')

        for article in articles:  # проход по статьям выпуска            
            article_info = parser.article_info_dict(article['url'])
            if article_info is None:
                continue
            article_output = {'article_name': article['name']}
            article_output.update(article_info)
            support.pretty_dict_print(indent=" "*12, ugly_dict=article_output)
            if articles.is_last() and issues.is_last():
                last = True
            support.write_article(issue, article_output, file, last)
            articles.save_statement()
        issues.save_statement()

    return article_output


def main():
    """
    Обработка json'а
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Смена текущей директории на директории где расположен main.py
    load_status = {'journals': True, 'issues': True, 'articles': True}
    try:
        with open('statement/subdomains', 'r') as file:
            content = file.read()        
        subdomains = containers.DomainsContainer(json.loads(content))
    except FileNotFoundError:
        json_form = format_to_json(settings.FILE_PATH)
        json_loader = json.loads(json_form)
        domain_dict = json_handling(json_loader)        
        subdomains = containers.DomainsContainer(domain_dict)

    # Иницилизация vpn
    get_recommend_vpn_list()
    get_all_vpn_list()


    for subdomain in subdomains:  # проход по сабдомейнам
        if load_status['journals']:
            try:
                with open('statement/journals', 'r') as file:
                    content = file.read()
                journals = containers.SimpleContainer(json.loads(content), is_journals=True)
            except FileNotFoundError:
                journal_names = parser.journal_names_list(subdomain['url'])
                journals = containers.SimpleContainer(journal_names, is_journals=True)
            finally:
                load_status['journals'] = False
        else:
            journal_names = parser.journal_names_list(subdomain['url'])
            journals = containers.SimpleContainer(journal_names, is_journals=True)
        print(f"{subdomain}")
        

        for journal in journals:
            detect = detect_langs(journal['name'])
            if detect[0].lang != 'en' or detect[0].prob < 0.85:
                print('lang: ', detect)
                print('Not English')  # пропускаем не английский журнал
                continue
            if load_status['issues']:
                try:
                    with open('statement/issues', 'r') as file:
                        content = file.read()
                    content = json.loads(content)
                    # print(content)
                    # print(type(content))
                    issues = containers.IssuesContainer(content)
                except FileNotFoundError:
                    issues_info = parser.issues_dict(journal['url'])
                    if issues_info == []:  # если нет выпусков позже 2009 года
                        continue
                    issues = containers.IssuesContainer(issues_info)
                finally:
                    load_status['issues'] = False
            else:
                issues_info = parser.issues_dict(journal['url'])
                if issues_info == []:  # если нет выпусков позже 2009 года
                    continue
                issues = containers.IssuesContainer(issues_info)

            print(f'{" "*4}{"{"}"journal_name": "{journal["name"]}"{"}"}\n\n')
            try:
                os.mkdir(f"{subdomain['subdomain']}")
            except OSError:
                pass
            if load_status['articles']:
                try:
                    with open('statement/articles', 'r') as f:
                        pass
                    with open(f"{subdomain['subdomain']}/{journal['name'].replace(' ','')}.json", 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    with open(f"{subdomain['subdomain']}/{journal['name'].replace(' ','')}.json", 'w', encoding='utf-8') as file:
                        for line in lines:
                            file.write(line)
                        journal_runner(journal, issues, file, load_status)
                        support.write_end(file)
                except FileNotFoundError:
                    with open(f"{subdomain['subdomain']}/{journal['name'].replace(' ','')}.json", 'w', encoding='utf-8') as file:
                        support.write_info(subdomain, journal, file)
                        journal_runner(journal, issues, file, load_status)
                        support.write_end(file)
            else:
                with open(f"{subdomain['subdomain']}/{journal['name'].replace(' ','')}.json", 'w', encoding='utf-8') as file:
                    support.write_info(subdomain, journal, file)
                    journal_runner(journal, issues, file, load_status)
                    support.write_end(file)
            journals.save_statement()
        subdomains.save_statement()



if __name__ == '__main__':
    support.init_headers()  # иницилизация браузеров
    main()
