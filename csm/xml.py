'''
Created on 2020/07/07

@author: CSM
'''
import xml.etree.ElementTree as ET

class CsmXml(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    @staticmethod
    def getXmlTree(path):
        tree =""
        with open(path,'r', encoding="utf-8") as f:
            tree += f.read()
        return tree

    @staticmethod
    def getXmlRoot(tree):
        root = ET.fromstring(tree)
        return root

    @staticmethod
    def getState(root,xp):
        states = root.find(xp)
        return states

    @staticmethod
    def getResult(state):
        result = str(state.text)
        return result
