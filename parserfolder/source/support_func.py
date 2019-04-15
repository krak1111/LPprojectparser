import json
import os

def pretty_dict_print(indent, ugly_dict):
    """
    Печатает в хорошем виде входящий словарь
    """
    for key in ugly_dict:
        print(f'{indent}{key}:  {ugly_dict[key]}')
        if key == 'doi':
            break
    print('\n')

def write_info(subdomain, journal, file):
    """
    Запись метаинформации о статье
    """
    lbrace = '{'
    file.write(f'{lbrace}"primary": "{subdomain["primary"]}",\n')
    file.write(f'"domain": "{subdomain["domain"]}",\n')
    file.write(f'"subdomain": ["{subdomain["subdomain"]}"],\n')
    file.write(f'"journal name": {json.dumps(journal["name"])},\n')
    file.write(f'"articles": [\n')
    file.flush()
    return True

def write_article(issue, article, file, last=False):
    """
    Запись статьи в JSON
    """
    lbrace = '{'
    rbrace = '}'
    ident = ' '*4

    file.write(f'{ident}{lbrace}"article name": {json.dumps(article["article_name"])},\n')
    file.write(f'{ident} "doi": {json.dumps(article["doi"])},\n')
    file.write(f'{ident} "publication date": {json.dumps(issue["date"])},\n')
    file.write(f'{ident} "abstract": {json.dumps(article["abstract"])},\n')
    keywords = json.dumps(article["keywords"])
    if last:
        end = '\n'
    else:
        end = ',\n'
    file.write(f'{ident} "keywords": {keywords}{rbrace}{end}')
    file.flush()
    print('Записано')

def write_end(file):
    """
    Конечная запись в JSON
    """
    file.write(f"{' '*4}]\n")
    file.write('}')

def copy_processing(journal_name, subdomain_name):
    walking_path = os.path.join(os.getcwd(), 'journals')
    journal_name.replace('/', ' ')
    file = f'{journal_name}.json'
    for root, _, files in os.walk(walking_path):
        if file in files:
            file_path = os.path.join(os.getcwd(), root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            subdomains = json.loads('{'+lines[2][:-2]+'}')
            subdomains['subdomain'].append(subdomain_name)
            lines[2] = json.dumps(subdomains).replace('{','').replace('}','')+',\n'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
    return False

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
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'headers')
    with open(path, 'r') as file:
        for line in file:
            output_list.append({'user-agent': line.replace('\n', '')})

    return output_list

