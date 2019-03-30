import pickle
import json


def load(subdomain='domain', journal='journal', issue='issue', article='article'):
    """
    Предполагалось сохранения состояния, это загрузчик
    """
    try:
        with open(article, 'rb') as file:
            article_object = pickle.loads(file.read())
    except FileNotFoundError:
        return (None, None, None, None)

    try:
        with open(issue, 'rb') as file:
            issue_object = pickle.loads(file.read())
    except FileNotFoundError:
        return (article_object, None, None, None)

    try:
        with open(journal, 'rb') as file:
            journal_object = pickle.loads(file.read())
    except FileNotFoundError:
        return (article_object, issue_object, None, None)

    try:
        with open(subdomain, 'rb') as file:
            subdomain_object = pickle.loads(file.read())
            return (article_object, issue_object, journal_object, subdomain_object)
    except FileNotFoundError:
        return (article_object, issue_object, journal_object, None)


def pretty_dict_print(indent, ugly_dict):
    """
    Печатает в хорошем виде входящий словарь
    """
    for key in ugly_dict:
        print(f'{indent}{key}:  {ugly_dict[key]}')
    print('\n')

def write_info(subdomain, journal, file):
    """
    Запись метаинформации о статье
    """
    lbrace = '{'
    file.write(f'{lbrace}"primary": "{subdomain["primary"]}",\n')
    file.write(f'"domain": "{subdomain["domain"]}",\n')
    file.write(f'"subdomain": "{subdomain["subdomain"]}",\n')
    file.write(f'"journal name": "{journal["name"]}",\n')
    file.write(f'"articles": [\n')
    return True

def write_article(issue, article, file):
    """
    Запись статьи в JSON
    """
    lbrace = '{'
    rbrace = '}'
    ident = ' '*4
    file.write(f'{ident}{lbrace}"article name": "{article["article_name"]}",\n')
    file.write(f'{ident} "doi": "{article["doi"]}",\n')
    file.write(f'{ident} "publication date": "{issue["date"]}",\n')
    file.write(f'{ident} "abstract": "{article["abstract"]}",\n')
    keywords = json.dumps(article["keywords"])
    file.write(f'{ident} "keywords": {keywords}{rbrace},\n')

def write_end(file):
    """
    Конечная запись в JSON
    """
    file.write(f"{' '*4}]\n")
    file.write('}')

def counter_deco(func):
    """
    Счетчик вызовов функций
    """
    def _counted(*largs, **kargs):
        _counted.numerator += 1
        return func(*largs, **kargs)
    _counted.numerator = 0
    return _counted


def memorize(func):
    """
    Хранилище списка вывода функции для удобного обращения к нему
    """
    def _l(*largs, **kargs):
        _l.itemlist = func(*largs, **kargs)
        return _l.itemlist
    _l.itemlist = []
    return _l

@counter_deco
def give_header():    
    if give_header.numerator > 25:
        give_header.numerator = 1
    return init_headers.itemlist[give_header.numerator-1]


@memorize
def init_headers():
    output_list = []
    with open('headers', 'r') as file:
        for line in file:
            output_list.append({'user-agent': line.replace('\n', '')})

    return output_list
