'''
Created on 2020/07/23

@author: CSM
'''
import os
import PySimpleGUI as sg
import pkg.csm.json as cj
import pkg.csm.directories as drs
import threading
import pkg.csm.buildhtml as bh

class ButtonAction(object):
    '''
    classdocs
    '''


    def __init__(self, root, caller, targetPath, inputRulePath, outputRulePath, filename):
        self.__root = root
        self.__caller = caller
        self._setErrorWindowIcon( caller.getResourcesPath() + r'\icon.ico')
        self._setDirectories(targetPath)
        self._loadInputRule(inputRulePath)
        self._loadOutputRule(outputRulePath)
        self.__filename = filename

        thread1 = threading.Thread(target=self._action)
        thread1.start()

    def _action(self):
#         print(self.__inputrule)
        #インプットルールに基づいて入力データ適用
        self.__directories.setRows(self.__inputrule)

        #適用された入力データを取得　★ここpublicメンバにアクセスしているからメソッド経由に変更
        inputRows = self.__directories.getNoteAll()

        #HTML構成クラス生成
        builder = bh.BuildHtml(self.__root,self)

        #ヘッダフッタを先に定義
        builder.addHead(self.__outputrule['head'])
        builder.addFoot(self.__outputrule['foot'])

        #入力データをTable行に変換してBodyに追加
        rule = self.__outputrule['row']
        escapeA = self.__outputrule['escape'][0]
        escapeB = self.__outputrule['escape'][1]
        builder.addTableRows(rule, escapeA, escapeB, inputRows)


        #保存先のディレクトリ取得
        file_dir = os.path.dirname(self.__root)

        #ファイル書出
        builder.writeFile(file_dir, self.__filename)

        #ウィンドウの完了処理を実行
        self.__caller.btnEnd()

        return

    def _setErrorWindowIcon(self,path):self.__icon = path
    def _setDirectories(self,path):self.__directories = drs.Directories( self.__root, self, path)
    def getCaller(self):return self.__caller
    def _loadtRule(self, path, isInput):
        try:
            if(isInput): self.__inputrule = cj.Json.getJsonList(path)
            else: self.__outputrule = cj.Json.getJsonList(path)
        except:
            sg.popup_error('JSON Error',icon=self.__icon)
    def _loadInputRule(self,path):self._loadtRule(path, True)
    def _loadOutputRule(self,path):self._loadtRule(path, False)

