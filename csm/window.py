'''
Created on 2020/07/23

@author: CSM
'''

import PySimpleGUI as sg
import subprocess
import platform
import pkg.csm.button_action as ba

class Window(object):
    '''
    classdocs
    '''


    def __init__(self, root):
        '''
        Constructor
        '''
        s = self
        s.__root = root

        #テーマ設定
        s._setWindowTheme('Dark Blue 3')
        s._setResourcesPath(s.__root +"Resources\\")
        s._setFilename("list")
        s._setDefaultTargetPath()
        s._setInputRulePath(s.__resources+"inputrule.json")
        s._setOutputRulePath(s.__resources+"outputrule.json")
        s._setProgressBarMax(1000)
        s._setProgressPhase( [ 0.5, 0.49, 0.01 ] )
        s._setBuildedFilename()
        s._setLayout([
            [
                sg.Text('')
            ],[
                sg.Text("MOD Directory", size=(15, 1)),
                sg.InputText(s.__defaultPath_Target,key="target"),
                sg.FolderBrowse(key='browse_target'),
                sg.Submit(button_text='Default',key="btn_target")
            ],[
                sg.Text('InputRule', size=(15, 1)),
                sg.InputText(s.__defaultPath_Input,key="inputrule"),
                sg.FileBrowse(key='browse_input'),
                sg.Submit(button_text='Default',key="btn_iprl")
            ],[
                sg.Text('OutputRule', size=(15, 1)),
                sg.InputText(s.__defaultPath_Output ,key="outputrule"),
                sg.FileBrowse(key='browse_output'),
                sg.Submit(button_text='Default',key="btn_oprl")
            ],[
                sg.Text('FileName', size=(15, 1)),
                sg.InputText(s.__defaultFilename ,key="filename"),
                sg.Submit(button_text='Default',key="btn_filename")
            ],[
                sg.Submit(button_text='Start',key="btn_run"),
                sg.Submit(button_text='Open',key="btn_open",disabled=True )
            ],[
                sg.ProgressBar(s.__progMax, orientation="h", size=(60, 20), key="progbar")
            ]
        ])

        s._bootSgWindow(
            'Vomit Vortex',
            s.__layout,
            s.__resources + 'icon.ico'
        )
        return

    def _setWindowTheme(self,s): sg.theme(s)
    def _setResourcesPath(self,s): self.__resources = s
    def _setInputRulePath(self,s): self.__defaultPath_Input = s
    def _setOutputRulePath(self,s): self.__defaultPath_Output = s
    def _setFilename(self,s): self.__defaultFilename = s
    def _setProgressBarMax(self,n): self.__progMax = n
    def _setProgressPhase(self,ls): self.__progPhase = ls
    def _setBuildedFilename(self,s=''): self.__buildedFileName = s
    def _setLayout(self,layout): self.__layout = layout
    #実行環境に対応するMODディレクトリの標準的な値を設定
    def _setDefaultTargetPath(self):
        #32bitOSに対応したくないが対応
        is64bit = platform.machine().endswith("64")
        fix = " (x86)" if is64bit else ""
        s = "C:\\Program Files"+fix+"\\Steam\\steamapps\\workshop\\content\\294100"
        self.__defaultPath_Target = s
        return
    #このウィンドウの全ボタンの有効状態を変更
    def _setAllButtonInvalid(self,valid):
        key = ["target","inputrule","outputrule","filename","browse_target","browse_input","browse_output","btn_target","btn_iprl","btn_oprl","btn_filename","btn_open","btn_run"]
        for k in key:self.__window[k].update(disabled=valid)

    def getResourcesPath(self):return self.__resources



    def _bootSgWindow(self,title, layout, ic):
        self.__window = sg.Window(title, layout, icon=ic)
        self._eventLoop()

    def _eventLoop(self):
        def getBuildFilePath(): return self.__root + self.__buildedFileName +'.html'
        w = self.__window
        live = True
        while live:
            e, v = w.read()
            if e == 'btn_target'  : w["target"].Update(self.__defaultPath_Target)
            if e == 'btn_iprl'    : w["inputrule"].Update(self.__defaultPath_Input)
            if e == 'btn_oprl'    : w["outputrule"].Update(self.__defaultPath_Output)
            if e == 'btn_filename': w["filename"].Update(self.__defaultFilename)
            if e == 'btn_open'    : subprocess.Popen(['start', getBuildFilePath()], shell=True)
            if e == 'btn_run'     : self._btnRun(v)
            if e is None          : live = False
        w.close()
        return

    def _btnRun(self,v):
        self._setAllButtonInvalid(True)
        self._setBuildedFilename(v["filename"])
        ba.ButtonAction(self.__root, self, v["target"], v["inputrule"], v["outputrule"], v["filename"])
        return

    def btnEnd(self):
        self.updateProgressBar(2,1)
        self._setAllButtonInvalid(False)
        return

    #プログレスバーの長さを更新する
    #対象フェーズ・フェーズ進行度を指定
    def updateProgressBar(self, currentPhase, rate):
        totalRate = 0
        phaseList = self.__progPhase
        gaugeMax = self.__progMax
        if( currentPhase > len(phaseList) ) : raise
        for i, value in enumerate( phaseList ):
            if( i >= currentPhase ) : break
            totalRate += value
        totalRate += phaseList[ currentPhase ] * rate
        result = gaugeMax * totalRate
        self.__window["progbar"].update_bar(result)


