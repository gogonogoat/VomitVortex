'''
Created on 2020/07/06

@author: CSM
'''

import os
import pathlib as pl
import pkg.csm.raw as raw

class Directories(object):
    '''
    classdocs
    '''

    def __init__(self, root, caller, path):
        '''
        Constructor
        '''
        self.__root = root
        self.__caller = caller
        self.__window = caller.getCaller()
        self._setCurrentDirectory(path)
        self._setEncloseDirectoryList()

    def _setCurrentDirectory(self,path):
        #Pathがディレクトリでなければ無効である
        if(os.path.isdir(path)==False):raise
        self.__path = path if pl.Path(path).is_absolute() else str(pl.Path(path).resolve())
        return

    #ディレクトリ内のディレクトリ一覧を設定
    def _setEncloseDirectoryList(self):
        #相対パスで取得
        files = os.listdir(self.__path)
        files_dir = [f for f in files if os.path.isdir(os.path.join(self.__path, f))]
        self.__encloseDir_Rel = files_dir

        #相対パス一覧から絶対パス変換したリストを取得
        self.__encloseDir_Abs = [0]*len(self.__encloseDir_Rel)
        self.__note = [0]*len(self.__encloseDir_Rel)
        for i in range(len(self.__encloseDir_Rel)):
            self.__encloseDir_Abs[i] = self.__path +"\\" + self.__encloseDir_Rel[i]


    def _setNote(self,i,note): self.__note[i] = note

    def setRows(self,rule):
        length = len(self.__encloseDir_Abs)
        for i,_ in enumerate(self.__encloseDir_Abs):
            self.__window.updateProgressBar(0,i/length)
            r = raw.Raw( self.__root, self, i, rule )
            self._setNote( i, r.factor)


    def getNoteAll(self): return self.__note
    def getPath(self):return self.__path

    #インデックスで指定したディレクトリに対する相対パスの解決結果を取得
    def getPathResolve(self,i,path):
        os.chdir(self.__encloseDir_Abs[i])
        result = pl.Path(path).resolve()
        return result

