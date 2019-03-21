import pickle
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

        for self.issue_year in issues_dict.keys():
            self.years_layer[f'{self.year_id}'] = self.issue_year  # 1 уровень
            self.issue_id = 1
            for self.issue_info in issues_dict[f'{self.issue_year}']: 
                self.issues_info_layer[
                    f'{self.year_id}.{self.issue_id}'] = self.issue_info  # 2 уровень
                self.issue_id += 1
            self.year_id += 1

        self.reset_statement()

    def __iter__(self):
        """
        При иницилизации итератора присваивается последнее сохраненное состояние
        """
        self.year_id = self.statement_year_id
        self.issue_id = self.statement_issue_id
        self.flag_stop_iteration = False
        return self

    def __next__(self):
        if self.flag_stop_iteration:  # Если дошли до конца
            self.reset_statement()
            raise StopIteration

        self.output = self.issues_info_layer[f'{self.year_id}.{self.issue_id}'].copy()
        self.output['year'] = self.years_layer[f'{self.year_id}']

        if self.issues_info_layer.get(self.issue_id+1, False):
            self.issue_id += 1
        elif self.years_layer.get(self.year_id+1, False):
            self.year_id += 1
            self.issue_id = 1
        else:
            self.flag_stop_iteration = True

        return self.output

    def reset_statement(self):
        """
        Сброс состояния и итератора
        """
        self.year_id = 1
        self.issue_id = 1
        self.statement_year_id = 1
        self.statement_issue_id = 1
        return True

    def save_statement(self):
        """
        Сохранение состояние вызывается после сохранения данных после парсинга
        """
        self.statement_year_id = self.year_id
        self.statement_issue_id = self.issue_id
        return True

    def save(self, file_path='issue'):
        """
        серилизация и сохранение объекта
        """
        self.statement_year_id = self.year_id
        self.statement_issue_id = self.issue_id
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)