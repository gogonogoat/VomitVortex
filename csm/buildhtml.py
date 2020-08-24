'''
Created on 2020/07/27

@author: CSM
'''
import PySimpleGUI as sg
import re
import copy
class BuildHtml(object):
    '''
    classdocs
    '''


    def __init__(self, root, caller):
        '''
        Constructor
        '''
        self._root = root
        self._caller = caller
        self._window = caller.getCaller()
        self._head =''
        self._body =''
        self._foot =''



    def _addTableRow( self, rule, escapeA, escapeB, vList):
        def getTableRow( rule, escapeA, escapeB, vList):
            def escapeFix(s):
                if(re.search(r"\d",s)):
                    sg.popup_error('JSON Error (OutputRule)')
                    raise
                return re.sub("([\\\*\+\.\?\{\}\(\)\[\]\^\$\-\|\/])",r"\\\1",s)
            row = ''.join(copy.deepcopy(rule))
            vListMax = len(vList)-1
            escapeA_fix = escapeFix(escapeA)
            escapeB_fix = escapeFix(escapeB)
            p = escapeA_fix + "(\d+)" + escapeB_fix
            itr = re.finditer( p, row )
            for i in reversed(list(itr)):
                n = int(re.sub(r'.(\d+).',r"\1", i.group()))
                if ( 0 <= n <= vListMax ) :
                    t = escapeA + str(n) + escapeB
                    row = row.replace(t, str(vList[n]["then"]))
            return row
        self.addBody(getTableRow(rule, escapeA, escapeB, vList))

    def addTableRows( self, rule, escapeA, escapeB, inputRows):
        length = len(inputRows)
        for i,v in enumerate(inputRows):
            self._window.updateProgressBar(1,i/length)
            self._addTableRow(rule, escapeA, escapeB, v)


    def _addElement(self,target,value):
        #追加対象が文字列ならばそのまま通してリストなら一次元結合
        add_str = ''
        if(isinstance(value,str))   : add_str = value
        elif(isinstance(value,list)): add_str = ''.join(value)
        else:raise Exception("異物混入です")
        #追加先を選択 (ヽ´ω`)変数アドレスへの参照を使いたい…
        if(target==1)  : self._head += add_str
        elif(target==2): self._body += add_str
        elif(target==3): self._foot += add_str
        else:raise Exception("宛先不明です")
        return add_str


    def addHead(self,s):return self._addElement(1,s)
    def addBody(self,s):return self._addElement(2,s)
    def addFoot(self,s):return self._addElement(3,s)

    def writeFile(self,dirc,filename):
        html = self._head+self._body+self._foot
        filepath = dirc+'\\'+filename+'.html'
        with open(filepath, mode='w', encoding="utf_8") as f:f.write(html)
        return