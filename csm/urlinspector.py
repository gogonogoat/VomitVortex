'''
Created on 2020/07/17

@author: CSM
'''

from urllib.parse import urlparse
import socket
import ipaddress

class UrlInspector(object):
    __known_loc = []
#     {
#         str:
#         ip:
#         enable:
#      }

    #Constructor
    def __init__(self, s):
        #元々の文字列
        self.__baseString = s
        #URL化する為に調整した文字列
        self.__fixUrl = s

        #URLとして有効であるかのフラグ
        self.__enable = True
        try:
            #スキーム補完＆URLパース
            self.__parsed = self._getParsedURL(self.__fixUrl)

            #不正なスキームを除去
            self.__scheme = self._disableDenyScheme(self.__parsed.scheme)

            #名前解決できるロケーションを取得
            self.__netloc = self._getVerificatedNetloc(self.__parsed.netloc)
        except:
            None

    def getFixUrl(self):return self.__fixUrl
    def getEnable(self):return self.__enable


    def _getVerificatedNetloc(self,s):
        #リスト内から発見したフラグOFF
        is_known = False
        #IPアドレス
        ip = ""
        #既知のリスト内を対象にループ
        for target in UrlInspector.__known_loc:
            #if リスト対象は対象ロケーションに一致する
            if( target["str"] == s ):
                #リスト対象からURL有効性を反映
                self.__enable = target["enable"]
                #リストから発見したフラグON
                is_known = True
                #ループ離脱
                break
        #if リストから発見したフラグがOFFである
        if( is_known == False ):
            #if そのロケーションはIPアドレス文字列か？
            if( self._isIpAddress(s) ):
                #IPアドレス = ロケーション
                ip = s
            #else
            else:
                #IPアドレス = ロケーションの名前解決結果
                try:
                    ip = socket.gethostbyname(s)
                except:
                    ip = False
                #if IPアドレスの取得に失敗している
                if( ip == False ):
                    #URLは無効である
                    self.__enable = False
                    #無効なロケーションとしてリストに追加する
                    self._setKnownLocate(s,"",False)
                #else
                else:
                    #有効なロケーションとしてリストに追加する
                    self._setKnownLocate(s,ip,True)
        #return if s URLは有効であるか else ""
        return s if self.__enable else ""

    #対象の文字列がIPアドレスとして成立するかを取得
    def _isIpAddress(self,s):
        result = True
        try   : ipaddress.ip_address(s)
        except: result = False
        return result

    def _setKnownLocate(self,s,ip,enable):
        UrlInspector.__known_loc.append({"str":s,"ip":ip,"enable":enable})
        return


    #URL文字列をパース
    def _getParsedURL(self,s):
        #まずは普通にパース
        try:
            parsed = urlparse(self.__fixUrl)
        except:
            #パース不可能なら空文字列のパース結果で返す
            return urlparse("")
        #スキーム未指定である場合は仮定値与えて再パース
        if(parsed.scheme == ''):
            self.__fixUrl = "http://" + self.__fixUrl
            parsed = urlparse(self.__fixUrl)
        #パース結果を返す
        return parsed

    #不正なスキームを除去する
    def _disableDenyScheme(self,s):
        #有効なスキーム
        allow = ["http","https"]
        #一致した値を返す
        for scheme in allow:
            if( s == scheme ):
                return s
        #不正なスキーム検出したので有効なURLと見なさない
        self.__enable = False
        #スキームは空として返す
        return ""