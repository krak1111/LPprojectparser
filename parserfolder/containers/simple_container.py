import json
import os


class SimpleContainer(object):

    def __init__(self, input_list, is_journals=False):
        self.storage_dict = {}
        self.current_id = 1
        self.is_journals = is_journals
        for entity in input_list:
            self.single_entity_dict = {'name': entity['name'], 'url': entity['url']}
            self.storage_dict[self.current_id] = self.single_entity_dict
            del self.single_entity_dict 
            self.current_id += 1
        if self.is_journals:
            self.f_name = 'journals'
        else:
            self.f_name = 'articles'
        self.current_id = 1
        self.file_path = os.path.join(os.getcwd(), 'parserfolder', 'statement', self.f_name)
        self.save_statement()


    def save_statement(self):
        self.writen_list = []
        self.id = self.current_id
        while self.storage_dict.get(self.id, False):
            self.writen_list.append(self.storage_dict[self.id])
            self.id += 1
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(self.writen_list))

    def reset_statement(self):
        os.remove(self.file_path)


    def __iter__(self):
        self.current_id = 1
        self.flag_stop_iteration = False
        return self

    def __next__(self):
                
        if self.flag_stop_iteration:
            self.reset_statement()
            raise StopIteration
        self.save_statement()
        self.output = self.storage_dict[self.current_id]

        if self.storage_dict.get(self.current_id+1, False):
            self.current_id += 1
        else:
            self.flag_stop_iteration = True

        return self.output


    def is_last(self):
        return self.flag_stop_iteration