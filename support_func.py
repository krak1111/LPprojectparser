import pickle
def output_form(subdomain, journal, issue, article, article_info) -> dict:
    pass


def load(subdomain='domain', journal='journal', issue='issue', article='article'):
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
