import json
import os
from operator import itemgetter


class JSONManager():
    def __init__(self):
        self.filename = 'data.json'
        self.data = []
        if not os.path.exists(self.filename):
            self.__save()
        self.__load()


    def __save(self):
        '''Write JSON data to file.'''
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)
    
    
    def __load(self):
        '''Read data from file.'''
        with open(self.filename, 'r') as f:
            self.data = json.load(f)

    def getAll(self):
        '''Return the data file.'''
        self.__load()
        return self.data
    
    
    def get(self, data_id):
        '''
        Get data with the received id.
        Return data or None.
        
        data_id -- int, the id of the data
        '''
        self.__load()
        found = [index for (index, d) in enumerate(self.data) if d.get('id') == data_id]
        if len(found) == 0:
            return None
        index = found[0]
        return self.data[index]
        
        
    def add(self, data):
        '''
        Add data.
        Return the data id.
        
        data -- dict, with the data to add
        '''
        self.__load()
        new_data = {"data": data}
        self.data = sorted(self.data, key=itemgetter('id'))
        if len(self.data) == 0:
            new_id = 1
        else:
            new_id = self.data[-1]['id'] + 1
        
        new_data['id'] = new_id
        self.data.append(new_data)
        self.__save()
        return new_id
    
    
    def edit(self, data_id, new_data):
        '''
        Edit data with the received id.
        Return True if edited successfully.
        
        data_id -- int, the id of the data
        new_data -- dict, with the data to add
        '''
        self.__load()
        found = [index for (index, d) in enumerate(self.data) if d.get('id') == data_id]
        if len(found) == 0:
            return False
        index = found[0]
        self.data[index] = new_data
        self.__save()
        return True
    
    
    def delete(self, data_id):
        '''
        Delete data with the received id.
        Return True if deleted successfully.
        
        data_id -- int, the id of the data
        '''
        self.__load()
        found = [d for d in self.data if d.get('id') == data_id]
        if len(found) == 0:
            return False
        self.data[:] = [d for d in self.data if d.get('id') != data_id]
        self.__save()
        return True


if __name__ == '__main__':
    jsm = JSONManager()
    id_1 = jsm.add({'data': 'Hello my friend, how are you?'})
    id_2 = jsm.add({'data': 'Can I help you?'})
    id_3 = jsm.add({'data': 'Sorry, can\'t do that.'})
    data_1 = jsm.get(id_1)
    data_2 = jsm.get(id_2)
    print(data_1)
    print(data_2)
    print(jsm.getAll())
    data_1['data'] = 'This is new'
    print('Edited --->', jsm.edit(id_1, data_1))
    data_1 = jsm.get(id_1)
    print(data_1)
    print(jsm.getAll())
    data_2 = jsm.delete(id_2)
    print('Deleted --->', data_2)
    print(jsm.getAll())