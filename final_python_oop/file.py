import json
from exceptions import FileError

class File:
    def __init__(self, directory):
        self.directory = directory
        

    def create_id(self, class_name):
        try:
            file_dir = self.directory + f"{class_name.lower()}s.json"
            ## read the id_count associated with the class_name:
            with open(file_dir, "r") as r_file:
                data_dict = json.load(r_file)
                ## create id : first letter of the class name concatenated with id_count
                id = class_name[0] + str(data_dict["id_count"])
            ## updating id_count in file:
            with open(file_dir, "w") as w_file:
                data_dict["id_count"] += 1
                json.dump(data_dict, w_file, indent= 4)
            return id
        except Exception as e:
            raise FileError(e.__str__())


    def save_data(self, class_name, data_dict):
        try:
            file_dir = self.directory + f"{class_name.lower()}s.json"
            ## read json file associated with class_name
            with open(file_dir, "r") as r_file:
                data = json.load(r_file)
            ## update the json file's dictionary 
            data_key = class_name.lower() + "_id" # such as `user_id`, `show_id` and ...
            data["data"][data_dict[data_key]] = data_dict
            ## save updated dictionary to the associated file
            with open(file_dir, "w") as w_file:
                json.dump(data, w_file, indent= 4)
        except Exception as e:
            raise FileError(e.__str__())


    def load_data(self, class_name):
        try:
            file_dir = self.directory + f"{class_name.lower()}s.json"
            with open(file_dir, "r") as r_file:
                data_dict = json.load(r_file)
            data = data_dict["data"]
            return data
        except Exception as e:
            raise FileError(e.__str__())


    def is_id(self, class_name, id_):
        try:
            file_dir = self.directory + f"{class_name.lower()}s.json"
            ## read json file associated with class_name
            with open(file_dir, "r") as r_file:
                data = json.load(r_file)
            if data["data"].get(id_, None): ## if id_ does not exists, returns None
                return True
            return False
        except Exception as e:
            raise FileError(e.__str__())
        

    def set_attributes(self, class_name, id_, attr_value): # attr_value: a dictionary
        file_dir = self.directory + f"{class_name.lower()}s.json"
        try:
            with open(file_dir, "r") as r_file:
                data_dict = json.load(r_file)
            ## updating new values in file:
            with open(file_dir, "w") as w_file:
                for attr, new_value in attr_value.items():
                    data_dict["data"][id_][attr] = new_value
                json.dump(data_dict, w_file, indent= 4)
        except Exception as e:
            raise FileError(e.__str__())


    def get_attributes(self, class_name, id_, attrs): # attrs: a list of requested attributes
        try:
            file_dir = self.directory + f"{class_name.lower()}s.json"
            with open(file_dir, "r") as r_file:
                data_dict = json.load(r_file)
            data_dict = data_dict["data"]
            
            result = {}
            for atrr in attrs:
                result[atrr] = data_dict[id_][atrr]         
            return result
        except KeyError as e:
            raise FileError(e.__str__())
        except Exception as e:
            raise FileError(e.__str__())
        

    def select_data(self, class_name, coloumns, where): 
        ## coloumns is a list of reuired fields in select
        # where is a dictionary representing `attr:value` conditions
        try:
            data = self.load_data(class_name)
            results = []
            for data_dict in data.values():
                matched = True
                for attr, value in where.items():
                    if data_dict[attr] != value:
                        matched = False
                if matched:
                    results.append({key:data_dict[key] for key in coloumns}) 
            return results
        except FileError as e:
            raise e
