'''
Created on 2020/07/03

@author: CSM
'''

import os
import pathlib
import pkg.csm.window as csm_w



def getAbsolutePath(s):
    path    = pathlib.Path(os.path.dirname(s))
    abspath = path if path.is_absolute() else path.resolve()
    result  = str(abspath)
    return result

#実行ファイルのディレクトリの絶対パスを取得
root = getAbsolutePath(__file__)+'\\'

#ウィンドウクラス生成
w = csm_w.Window(root)


