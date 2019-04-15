import json
import os
import time

from parserfolder.source import load_functions as load
from parserfolder.source import support_func as support
from parserfolder.source import parser, settings
from parserfolder.source.connection import get_recommend_vpn_list, get_all_vpn_list


from parserfolder import containers

def article_runner(articles, issues, file):
    """
    Проход по статьям
    """
    for article in articles:  # проход по статьям выпуска
        is_last = False
        article_info = parser.article_info_dict(article['url'])
        if not article_info:
            continue
        article_output = {'article_name': article['name']}
        article_output.update(article_info)
        support.pretty_dict_print(indent=" "*12, ugly_dict=article_output)
        if articles.is_last() and issues.is_last():
            is_last = True
        support.write_article(issues.current(), article_output, file, is_last)

def issues_runner(subdomain, journal, issues, file, load_status, is_new=True):
    """
    Проход по выпускам журнала и запись в json файл
    """
    if is_new:
        support.write_info(subdomain, journal, file)
    for issue in issues:  # проход по выпускам журнала
        last = False
        if load_status['articles']:
            article_titles = load.load_articles(load_status, journal, issue)
        else:
            article_titles = parser.articles_list(journal['url'], issue['url'])
        if not article_titles:
            continue
        articles = containers.SimpleContainer(article_titles)
        print(f'{" "*8}{issue}\n\n')
        article_runner(articles, issues, file)
    support.write_end(file)

def journals_runner(subdomain: dict, journals, load_status):
    """
    Проход по журналам
    """
    for journal in journals:
        if support.copy_processing(journal['name'], subdomain['subdomain']):
            continue
        if parser.is_not_english(journal):
            print('Not English')  # пропускаем не английский журнал
            journals.save_statement()
            continue
        dir_path = os.path.join(os.getcwd(), 'journals', subdomain['primary'], subdomain['domain'], subdomain['subdomain'])
        print(os.path.exists(dir_path))
        file_path = os.path.join(dir_path, f"{journal['name'].replace('/',' ')}.json")
        if load_status['issues']:  # первый проход, попытака загрузки состояния
            issues_info = load.load_issues(load_status, journal)
        else:
            issues_info = parser.issues_dict(journal['url'])
        if not issues_info:  # если нет выпусков позже 2009 года
            continue
        issues = containers.IssuesContainer(issues_info)

        print(f'{" "*4}{"{"}"journal_name": "{journal["name"]}"{"}"}\n\n')
        if load_status['articles']:  # Если файл с записями уже есть, его нужно продолжить
            is_new = False
            lines = load.file_continue_lines(file_path)
            with open(file_path, 'w', encoding='utf-8') as file:
                if lines:
                    file.writelines(lines)
                else:
                    is_new = True
                issues_runner(subdomain, journal, issues, file, load_status, is_new=is_new)
        else:
            with open(file_path, 'w', encoding='utf-8') as file:
                issues_runner(subdomain, journal, issues, file, load_status)

def subdomains_runner(subdomains, load_status):
    """
    проход по сабдомейнам
    """
    print(type(subdomains))
    for subdomain in subdomains:
        load.mkdir_for_subdomain(subdomain)
        if load_status['journals']:  # первый проход, попытака загрузки состояния
            journal_names = load.load_journals(load_status, subdomain)
        else:
            journal_names = parser.journal_names_list(subdomain['url'])
        journals = containers.SimpleContainer(journal_names, is_journals=True)
        print(subdomain)
        journals_runner(subdomain, journals, load_status)
        

def initilization():
    """
    Инициализация
        1. Хеадеров запросов
        2. Рекомендованных VPN серверов
        3. Всех VPN серверов 
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Смена текущей директории на директории где расположен main.py
    support.init_headers()
    get_recommend_vpn_list()
    get_all_vpn_list()
    dir_path = os.path.join(os.getcwd(), 'parserfolder', 'statement')
    print(os.path.exists(dir_path))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def main():    
    initilization()
    load_status = {'journals': True, 'issues': True, 'articles': True}
    filepath = os.path.join(os.getcwd(), 'parserfolder', 'statement', 'subdomains')
    if os.path.exists(filepath):  # Загрузка  по поддоменам
        domain_dict = load.load_file(filepath)
    else:
        path_to_start = os.path.join(os.getcwd(), 'parserfolder', 'source', 'input.json')
        with open(path_to_start) as f:
            domain_dict = json.loads(f.read())
    subdomains = containers.DomainsContainer(domain_dict)
    
    subdomains_runner(subdomains, load_status)


if __name__ == '__main__':
      # иницилизация браузеров
    main()
