import pickle


class DomainsContainer(object):
    """
    Класс на входе принимает словарь с данными о названиях
    основных разделов науки их разделов и
    названиях подразделов с ссылками на них
    Эти данные разбиваются на "уровни":
        1. Основные разделы науки (primary domains)
        2. Разделы (domains)
        3. Подразделы (subdomains)
    Вид входимого словаря:
    {'primary name 1':{
        'domain name 1.1':[
            {'name': 'subdomain name 1.1.1', 'url'}
        ]
        }
    }
    Каждый из этих уровней представлен в виде словаря:
        1. {'ID': 'Name of primary domain'}, где ID - числа начиная с 1
        2. {'ID': 'Name of domain'}, где ID представляют собой форму ID_primary.ID_domain(внутри основного раздела)
        3. {'ID': ('Name of subdomain', 'url of subdomain')}, где ID редставляют собой форму 
                                                              ID_primary.ID_domain(внутри основного раздела).ID_subdomain(внутри раздела)

    """
    def __init__(self, general_domain_dict):
        self.primary_domain_id = 1
        self.primary_domain_level = {}
        self.domain_level = {}
        self.subdomain_level = {}

        for self.primary_domain_name in general_domain_dict.keys():
            self.primary_domain_level[f'{self.primary_domain_id}'] = self.primary_domain_name
            self.domain_id = 1

            self.primary_domain_dict = general_domain_dict[self.primary_domain_name]

            for self.domain_name in self.primary_domain_dict.keys():
                self.domain_level[f'{self.primary_domain_id}.{self.domain_id}'] = self.domain_name
                self.subdomain_id = 1
                self.domain_list = self.primary_domain_dict[self.domain_name]

                for self.subdomain_dict in self.domain_list:
                    self.subdomain_level[f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id}'] = (self.subdomain_dict['name'], self.subdomain_dict['url'])
                    self.subdomain_id += 1

                self.domain_id += 1

            self.primary_domain_id += 1

    def print_all(self):
        """
        Печатает в виде:
        1 Основной раздел 1
            1.1 Раздел 1.1
                1.1.1 Подраздел 1.1.1: Ссылка на подраздел 1.1.1
                1.1.2 Подраздел 1.1.2: Ссылка на подраздел 1.1.2
                ...
            1.2 Раздел 1.2
            ...
        2 Основной раздел 2
        ...
        """
        for self.primary_domain_id in self.primary_domain_level.keys():  # Цикл по всем основным разделам
            self.current_id_str = f'{self.primary_domain_id}'  # Текущий индентификатор
            self.current_name = self.primary_domain_level[self.current_id_str]  #Текущее название
            print(f'{self.current_id_str}: {self.current_name}')  #Вывод на экран

            self.domain_id = 1

            while self.domain_level.get(f'{self.primary_domain_id}.{self.domain_id}', False): #Цикл до тех пор пока существует элемент с таким ID
                self.current_id_str = f'{self.primary_domain_id}.{self.domain_id}'
                self.current_name = self.domain_level[self.current_id_str]
                print(f'{" "*4}{self.current_id_str}: {self.current_name}')

                self.subdomain_id = 1

                while self.subdomain_level.get(f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id}', False): #Цикл до тех пор пока существует элемент с таким ID
                    self.current_id_str = f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id}'
                    self.current_name = self.subdomain_level[self.current_id_str]
                    print(f'{" "*8}{self.current_id_str}: {self.current_name}')

                    self.subdomain_id += 1

                self.domain_id += 1

        return True

    def __iter__(self):
        self.primary_domain_id = 1
        self.domain_id = 1
        self.subdomain_id = 1
        self.flag_stop_iteration = False
        return self

    def __next__(self):
        """
        Вывод подраздела в виде кортежа :
        (название основной раздела, название раздела,
        название подраздела, ссылка подраздела)
        """
        if self.flag_stop_iteration:  # Если
            raise StopIteration

        self.output = (self.primary_domain_level[f'{self.primary_domain_id}'],
                       self.domain_level[f'{self.primary_domain_id}.{self.domain_id}'],
                       self.subdomain_level[f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id}'][0],
                       self.subdomain_level[f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id}'][1])

        if self.subdomain_level.get(f'{self.primary_domain_id}.{self.domain_id}.{self.subdomain_id + 1}', False):  # проверка существование следующего подраздела
            self.subdomain_id += 1
        elif self.domain_level.get(f'{self.primary_domain_id}.{self.domain_id+1}', False):  # проверка существования следующего раздела
            self.domain_id += 1
            self.subdomain_id = 1
        elif self.primary_domain_level.get(f'{self.primary_domain_id + 1}', False):  # проверка существования следующего основного раздела
            self.primary_domain_id += 1
            self.subdomain_id = 1
            self.domain_id = 1
        else:  # Данный элемент последний
            self.flag_stop_iteration = True

        return self.output

    def save(self, file_path):
        """
        серилизация и сохранение объекта
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)
