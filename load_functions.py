import os
import json
import parser


def load_file(kind: str):
    """
    Загрузка состояния из файла
    """
    with open(f'statement/{kind}') as file:
        content = json.loads(file.read())
    return content

def file_continue_lines(file_path):
    try:
        with open('statement/articles', 'r') as file:  # проверка наличия файла
            pass
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        return None

def load_articles(load_status, journal, issue):
    try:
        article_titles = load_file('articles')
    except FileNotFoundError:
        article_titles = parser.articles_list(journal['url'], issue['url'])

    load_status['articles'] = False
    return article_titles

def load_issues(load_status, journal):
    try:
        issues_info = load_file('issues')
    except FileNotFoundError:
        issues_info = parser.issues_dict(journal['url'])
    load_status['issues'] = False
    return issues_info

def load_journals(load_status, subdomain):
    try:
        journal_names = load_file('journals')
    except FileNotFoundError:
        journal_names = parser.journal_names_list(subdomain['url'])
    load_status['journals'] = False
    return journal_names

def mkdir_for_subdomain(subdomain):
    try:
        os.mkdir(f"{subdomain['subdomain']}")
    except OSError:
        pass
