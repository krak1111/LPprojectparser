import pickle
class SimpleContainer(object):

    def __init__(self, input_list):
        self.storage_dict = {}
        self.current_id = 1
        
        for entity in input_list:
            self.single_entity_dict = {'name': entity['name'], 'url': entity['url']}
            self.storage_dict[self.current_id] = self.single_entity_dict
            del self.single_entity_dict 
            self.current_id += 1

        self.reset_statement()

    def reset_statement(self):
        self.current_id = 1
        self.statement_current_id = 1
        return True

    def save_statement(self):
        self.statement_current_id = self.current_id
        return True

    def __iter__(self):
        self.current_id_id = self.statement_current_id
        self.flag_stop_iteration = False
        return self

    def __next__(self):
                
        if self.flag_stop_iteration:
            self.reset_statement()
            raise StopIteration

        self.output = self.storage_dict[self.current_id]

        if self.storage_dict.get(self.current_id+1, False):
            self.current_id += 1
        else:
            self.flag_stop_iteration = True

        return self.output

    def current(self):
        self.output = self.storage_dict[self.statement_current_id]
        return self.output

    def save(self, file_path):
        """
        серилизация и сохранение объекта
        """
        self.statement_current_id = self.current_id
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)
