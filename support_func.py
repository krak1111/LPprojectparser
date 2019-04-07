import json



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
    file.write(f'"subdomain": "{subdomain["subdomain"]}",\n')
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

