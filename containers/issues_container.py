import json
import os

class IssuesContainer(object):
    """
    Двухуровневый контейнер для хранения текущих выпусков
    1 уровень - года выпуска
    2 уровень - информация о выпуске
    """

    def __init__(self, issues_dict):
        self.years_layer = {}
        self.issues_info_layer = {}
        self.year_id = 1

        for self.issue_year in issues_dict:
            self.years_layer[f'{self.year_id}'] = self.issue_year  # 1 уровень
            self.issue_id = 1

            for self.issue_info in issues_dict[f'{self.issue_year}']:
                self.issues_info_layer[
                    f'{self.year_id}.{self.issue_id}'] = self.issue_info  # 2 уровень
                self.issue_id += 1

            self.year_id += 1
        self.year_id = 1
        self.issue_id = 1
        self.save_statement()

    def __iter__(self):
        """
        При иницилизации итератора присваивается последнее сохраненное состояние
        """
        self.year_id = 1
        self.issue_id = 1
        self.flag_stop_iteration = False
        return self

    def __next__(self):
        if self.flag_stop_iteration:  # Если дошли до конца
            self.reset_statement()
            raise StopIteration
        self.save_statement()
        self.output = self.issues_info_layer[f'{self.year_id}.{self.issue_id}'].copy()
        self.output['year'] = self.years_layer[f'{self.year_id}']

        if self.issues_info_layer.get(f'{self.year_id}.{self.issue_id+1}', False):
            self.issue_id += 1
        elif self.years_layer.get(f'{self.year_id+1}', False):
            self.year_id += 1
            self.issue_id = 1
        else:
            self.flag_stop_iteration = True

        return self.output

    def reset_statement(self):
        """
        Удаление файла с состоянием
        """
        os.remove("statement/issues")

    def save_statement(self):
        """
        Сохранение состояние в файл
        """
        self.yid = self.year_id
        self.iid = self.issue_id
        self.writen_dict = {}
        while self.years_layer.get(f'{self.yid}', False):
            self.year = self.years_layer[f'{self.yid}']
            self.writen_list = []
            while self.issues_info_layer.get(f'{self.yid}.{self.iid}', False):
                self.writen_list.append(self.issues_info_layer[f'{self.yid}.{self.iid}'])
                self.iid += 1
            self.writen_dict[f'{self.year}'] = self.writen_list
            self.yid += 1
            self.iid = 1

        with open('statement/issues', 'w') as file:
            file.write(json.dumps(self.writen_dict))

    def print_all(self):
        
        for self.year_current_id in self.years_layer:
           
            self.current_name = self.years_layer[self.year_current_id]  # Текущее название
            print(f'{self.year_current_id}: {self.current_name}')  # Вывод на экран
            self.issues_current_id = 1

            while self.issues_info_layer.get(
                    f'{self.year_current_id}.{self.issues_current_id}',
                    False):  # Цикл до тех пор пока существует элемент с таким ID
                self.current_id_str = f'{self.year_current_id}.{self.issues_current_id}'
                self.current_name = self.issues_info_layer[self.current_id_str]
                print(f'{" "*4}{self.current_id_str}: {self.current_name}')
                self.issues_current_id += 1

    def is_last(self):
        return self.flag_stop_iteration

    def current(self):
        return self.output