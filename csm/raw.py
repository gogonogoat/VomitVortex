'''
Created on 2020/07/06

@author: CSM
'''
import copy
import os
import pkg.csm.xml as cx
import re
import pathlib
import datetime
import pkg.csm.urlinspector as uisp
import glob
import xml.etree.ElementTree as ET

class Raw(object):
    '''
    classdocs
    callerにdirectoriesを持つ
    '''


    def __init__(self, root, caller, index, json ):
        '''
        Constructor
        '''

        #明らかに過度な肥大化をしているクラス
        #Thenコマンドの定義ここから＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
        def isExist(i):
            if(self.factor[i]["isExist"]==False):
                self.factor[i]["then"] = "This File was NotFound."
                return False
            return True

        def birthtime(i):
            if(isExist(i)==False):
                return
            time = os.stat(self.factor[i]["absFilepath"]).st_ctime
            result = datetime.datetime.fromtimestamp(time).strftime("%Y/%m/%d %H:%M")
            self.factor[i]["then"] = result
            return ""

        def currentRelPath(i):
            if(isExist(i)==False):
                return
            p_abs = pathlib.Path(self.factor[i]["absFilepath"])
            result =p_abs.relative_to(self.__directoryRoot)
            self.factor[i]["then"] = result

        def currentAbsPath(i):
            if(isExist(i)==False):
                return
            self.factor[i]["then"] = self.factor[i]["absFilepath"]

        def xpath_GetValue(i,path):
            if(isExist(i)==False):
                return
            file_str = str(self.factor[i]["absFilepath"])
            try:
                tree = cx.CsmXml.getXmlTree(file_str)
                root = cx.CsmXml.getXmlRoot(tree)
                states = cx.CsmXml.getState(root, path)
                result = cx.CsmXml.getResult(states)
                self.factor[i]["then"] = result
            except:
                raise Exception

        def xpath_GetValueToButton( i, path, btn_classA, btn_classB, btn_classS ):
            result = None
            if(isExist(i)):
                file_str = str(self.factor[i]["absFilepath"])
                tree = cx.CsmXml.getXmlTree(file_str)
                root = cx.CsmXml.getXmlRoot(tree)
                states = cx.CsmXml.getState(root, path)
                try:
                    result = cx.CsmXml.getResult(states)
                except:
                    result = None

            parsed = uisp.UrlInspector(str(result))
            if( parsed.getEnable() ):
                self.factor[i]["then"] = "<a class='"+ btn_classA +"' href='"+ parsed.getFixUrl() +"' target='_blank'><span class='"+ btn_classS +"'></span></a>"
            else:
                self.factor[i]["then"] = "<span class='"+ btn_classB +"'><span class='"+ btn_classS +"'></span></span>"

        def getModalButtonForUnityUiXml( i, path, btn_classA, btn_classB, btn_classS ):
            result = None
            if(isExist(i)):
                file_str = str(self.factor[i]["absFilepath"])
                tree = cx.CsmXml.getXmlTree(file_str)
                root = cx.CsmXml.getXmlRoot(tree)
                states = cx.CsmXml.getState(root, path)
                try:
                    result = cx.CsmXml.getResult(states)
                except:
                    result = None


            content = ""
            if( result!=None ):
                content = "<div>" + str(result) + "</div>"
                content = getRichTextFromUnityUiXml(content)
                self.factor[i]["then"] = "<span class="+ btn_classA +"><span class="+ btn_classS +"></span></span><div class='modal_back modal_hide'><div class='modal_box'><div class='modal_content'>"+ content +"</div></div></div>"
            else:
                self.factor[i]["then"] = "<span class="+ btn_classB +"><span class="+ btn_classS +"></span></span><div class='modal_back modal_hide'><div class='modal_box'><div class='modal_content'>"+"</div></div></div>"

        def getRichTextFromUnityUiXml(s):
            s = re.sub('<([a-zA-z]+)=(.+?)>',r'<\1 value="\2">',s)

            s = re.sub('&',r'&amp;',s)
            root = ET.fromstring(s)

            def getInstantCss(atr,val):
                others = {"material","quad"}
                if   atr == "color": result = atr + ":" + val + ";"
                elif atr == "size" : result = atr + ":" + str(val/16) +"rem;"
                elif atr == "b"    : result = "font-weight:bold;"
                elif atr == "i"    : result = "font-style:italic;"
                elif atr in others : result = ""
                else               : result = ""
                return result

            for elm in root.iter():
                tag = elm.tag
                try:
                    val = str(elm.get('value'))
                    state = getInstantCss(tag,val)
                    elm.tag = "span"
                    elm.set("style",state)
                    elm.attrib.pop("value", None)
                except:
                    continue
            result = ET.tostring(root,encoding='unicode').replace('<span style=\"\">','',1)
            result = re.sub('</span>$','',result).replace('\n', '<br>').replace('\\n', '<br>')


            return result

        def getSuffixButton( i, urlA, urlB, btn_classA, btn_classB, btn_classS ):
            if(isExist(i)==False):
                return
            p_abs = pathlib.Path(self.factor[i]["absFilepath"])
            p_rel =str(p_abs.relative_to(self.__directoryRoot))
            if( p_rel.isdecimal() ):
                self.factor[i]["then"] = "<a class='"+ btn_classA +"' href='"+ urlA + str(p_rel) + urlB + "' target='_blank'><span class='"+ btn_classS +"'></span></a>"
            else:
                self.factor[i]["then"] = "<span class='"+ btn_classB +"'><span class='"+ btn_classS +"'></span></span>"



        def isExistFileFromExt( i, recursive, *exts ):
            os.chdir( str( self.factor[i]["absFilepath"] ) )
            for ext in exts :
                path = '**/*.' + ext
                matchPaths = glob.glob(
                    path,
                    recursive = recursive
                )
                if(len(matchPaths)!=0):
                    self.factor[i]["then"] = 1
                    return
            self.factor[i]["then"] = 0

        def isExistFileFromXpath( i, recursive, roottag, xpath, *exts ):
            os.chdir( str( self.factor[i]["absFilepath"] ) )
            for ext in exts :
                path = '**/*.' + ext
                matchPaths = glob.glob(
                    path,
                    recursive = recursive
                )
                for matchPath in matchPaths :
                    try:
                        file_str = matchPath
                        tree = cx.CsmXml.getXmlTree(file_str)
                        root = cx.CsmXml.getXmlRoot(tree)
                        if( str(root.tag)==roottag ):
                            if( xpath!='' ):
                                states = cx.CsmXml.getState(root, xpath)
                                if(states!=None):
                                    self.factor[i]["then"] = 1
                                    return
                            else:
                                self.factor[i]["then"] = 1
                                return
                    except:
                        None
                self.factor[i]["then"] = 0
        #Thenコマンドの定義ここまで＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


        self.__caller = caller
        self.__directoryRoot = caller.getPath()
        self.__root = root

        #インプットルール初期値
        dict_tmp = {
            "absFilepath":None,
            "isExist":False,
            "then":None,
            }



        #要素数設定（JSONの長さから要素数を取得）
        self.factor = [0]*len(json)

        #インプットルールの初期化・代入
        for i,_ in enumerate(self.factor):
            self.factor[i] = copy.deepcopy(dict_tmp)
            cFact = json[i]
            content = cFact["Path"]

            #相対To絶対の解決を得る
            p = self.__caller.getPathResolve(index,content)
            p_sumple = str(p).replace('/','').replace('\\','').replace('.','')
            c_result = str(content).replace('/','').replace('\\','').replace('.','')
            if(c_result==p_sumple):
                self.factor[i]["absFilepath"] = self.__directoryRoot + " ( "+content+" )"
            else:
                self.factor[i]["absFilepath"] = p
            if(os.path.isfile(p) or os.path.isdir(p)):
                self.factor[i]["isExist"] = True
            try:
                exec(cFact["Then"])
            except:
                if("Else" in cFact):
                    try:
                        exec(cFact["Else"])
                    except:
                        self.factor[i]["then"] = cFact["Else"]
                else:
                    self.factor[i]["then"] = cFact["Then"]





