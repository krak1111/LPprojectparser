import os
import json
from . import parser


def load_file(filepath):
    """
    Загрузка состояния из файла
    """
    with open(filepath) as file:
        content = json.loads(file.read())
    return content

def file_continue_lines(file_path):
    """
    Продолжение записи
    """
    filepath = os.path.join(os.getcwd(), 'parserfolder', 'statement', 'articles')
    if os.path.exists(filepath):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    return None

def load_articles(load_status, journal, issue):
    """
    Загрузка состояния обхода статей
    """
    filepath = os.path.join(os.getcwd(), 'parserfolder', 'statement', 'articles')
    if os.path.exists(filepath):
        article_titles = load_file(filepath)
    else:
        article_titles = parser.articles_list(journal['url'], issue['url'])

    load_status['articles'] = False
    return article_titles

def load_issues(load_status, journal):
    """
    Загрузка состояния обхода выпусков
    """
    filepath = os.path.join(os.getcwd(), 'parserfolder', 'statement', 'issues')
    if os.path.exists(filepath):
        issues_info = load_file(filepath)
    else:
        issues_info = parser.issues_dict(journal['url'])
    load_status['issues'] = False
    return issues_info

def load_journals(load_status, subdomain):
    """
    загрузка состояния обхода журналов
    """
    filepath = os.path.join(os.getcwd(), 'parserfolder', 'statement', 'journals')
    if os.path.exists(filepath):
        journal_names = load_file(filepath)
    else:
        journal_names = parser.journal_names_list(subdomain['url'])
    load_status['journals'] = False
    return journal_names

def mkdir_for_subdomain(subdomain):
    dirpath = os.path.join(os.getcwd(), 'journals')
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    dirpath = os.path.join(dirpath, subdomain['primary'])
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    dirpath = os.path.join(dirpath, subdomain['domain'])
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    dirpath = os.path.join(dirpath, subdomain['subdomain'])
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return True
