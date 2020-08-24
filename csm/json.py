'''
Created on 2020/07/06

@author: CSM
'''
import json
class Json():
    @staticmethod
    def getJsonList(path):
        json_open = open(path, 'r')
        json_load = json.load(json_open)
        return json_load