import re
import json

from containers import DomainsContainer


def format_to_json(file_path) -> dict:
    """
    Парсинг JSON'а со списком областей наук и подобластей

        Вид:
            primary : {
1 - уровень     "Primary url_form_name" :{
2 - уровень         name : 'primary name',
                    secondary : {
3 - уровень             "Domain_url_form":{ или одно слово без кавычек если domain в одно слово :{
4 - уровень                 name : "Domain name" или domain (если одно слово),
                            tertiary : {
5 - уровень                     "Subdomain_url_form" или одно слово без кавычек если domain в одно слово :{
6 - уровень                         name : "Domain name" или domain (если одно слово),
                                    sid : 12345
                                },
                            },
                        },
                    },
                },
                etc...
            }
    Функция добавляет кавычки к ключам, которые их не имеют
    """
    to_json_pattern = re.compile(r'\"{0}(?P<word>[a-zA-Z0-9]+):', re.S)

    with open(f'{file_path}', 'r', encoding='utf-8') as file:
        domain_json = ''
        for line in file:
            p = to_json_pattern.sub(r'"\g<word>":', line)
            domain_json += p

    return domain_json


def json_handling(file_path) -> dict:
    json_dict = json.loads(format_to_json(file_path))
    """
    Преобразовывается в вид:
        {'primary domain 1':{
            'Domain 1.1':[
                {'name': 'Subdomain 1.1.1', 'url': 'Subdomain url 1.1.1'},
                {'name': 'Subdomain 1.1.2', 'url': 'Subdomain url 1.1.2'},
                ]
            }
        }
    """
    primary_domain_dict = json_dict['primary']  # переход на 2 уровень
    output_all_domain_dict = {}  # создание словаря верхнего уровня
    """
    1. Верхний цикл проходится по ключам, соответствующим названиям основных
    разделов науки.
    2. Следующий цикл проходится по ключам, соответствующим названиям разделов
    науки
    """
    for current_primary_domain_dict_key in primary_domain_dict:  # проход по ключам 'Primary domain name'
        domain_dict = primary_domain_dict[
            f'{current_primary_domain_dict_key}']['secondary']  # словарь с данными про domain

        output_primary_domain_name = primary_domain_dict[
            f'{current_primary_domain_dict_key}']['name']  # ключ 'Primary domain name'
        output_domain_dict = {}  # данный словарь - значение для ключа 'Primary domain name' в обработанном виде

        for current_domain_dict_key in domain_dict:  # проход по ключам 'domain url form'
            subdomain_dict = domain_dict[
                f'{current_domain_dict_key}']['tertiary']  # переход на 5 уровень

            output_domain_name = domain_dict[current_domain_dict_key]['name']  # ключ 'Domain name'
            output_subdomain_list = []  # данный список - значение для ключа 'Domain name'

            for current_subdomain_dict_key in subdomain_dict:  # проход по ключам 'supdomain url form'
                output_subdomain_dict = {}  # словарь для хранения данных в виде {'name': name, 'url': url}
                output_subdomain_dict['name'] = subdomain_dict[
                    current_subdomain_dict_key]['name']  # значение name

                output_subdomain_dict['url'] = current_subdomain_dict_key  # значение url

                output_subdomain_list.append(output_subdomain_dict)  # добавление к списку
            output_domain_dict[output_domain_name] = output_subdomain_list  # добавление значения к ключу 'domain name'
        output_all_domain_dict[output_primary_domain_name] = output_domain_dict  # добавление значения к ключу 'primary domain name'

    return output_all_domain_dict


def main():
    file_path = 'domains.json'
    json_loader = json.loads(format_to_json(file_path))  # Православый json
    output = json_handling(json_loader)
    domain = DomainsContainer(output)  # экземпляр класса контейнера для хранения и работы с даннми об областях науки
    # domain.print_all()
    #d.save('container')  # серилизация класса с сохранением этих данных


if __name__ == '__main__':
    main()
