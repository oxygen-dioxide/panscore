__version__="0.0.2"

import os
import sys
import importlib
from typing import List,Tuple,Dict,Union,Type

defaultlyric=""

def getlibfromfiletype(filetype:str):
    """
    输入文件类型，返回对应的读写库
    """
    return importlib.import_module("panscore.filetypes."+filetype.lower())

class Note():
    '''
    音符类    
    start:起点，480为一拍，int
    length:长度，480为一拍，int
    notenum:音高，与midi相同，即C4为60，音高越高，数值越大，int
    lyric:歌词，str
    '''
    def __init__(self,
                 start:int,
                 length:int,
                 notenum:int,
                 lyric:str=""):
        self.start=start
        self.length=length
        self.notenum=notenum
        self.lyric=lyric
    pass

class Track():
    '''
    音轨类
    name:音轨名，str
    singer:歌手编号，str
    note:音符列表，List[Svipnote]
    volume:音量，float，[0,2]
    balance:左右声道平衡，float，[-1,1]
    mute:静音，bool
    solo:独奏，bool
    reverb:混响类型，int
    '''
    def __init__(self,
                 name:str="",
                 note:List[Note]=[]):
        if(note==[]):
            note=[]
        self.name=name
        self.note=note
    pass

class Score():
    '''
    文件类
    track:音轨列表
    '''
    def __init__(self,
                 track:List[Track]=[]):
        self.track=track

    def save(self,filename:str,filetype=None,**kwargs):
        """
        将panscore.Score对象保存为文件
        filetype:文件类型，可以是字符串，如"ust"，也可以panscore.filetypes下的库，如panscore.filetypes.ust。默认按照文件后缀名。
        """
        if(filetype in ("",None)):
            filetype=filename.split(".")[-1]
            lib=getlibfromfiletype(filetype)
        if(type(filetype)==str):
            lib=getlibfromfiletype(filetype)
        else:
            lib=filetype
        return lib.save(self,filename,**kwargs)
        pass

def load(filename:str,filetype=None,**kwargs)->Score:
    """
    打开文件，返回panscore.Score对象
    filetype:文件类型，可以是字符串，如"ust"，也可以panscore.filetypes下的库，如panscore.filetypes.ust。默认按照文件后缀名。
    """
    if(filetype in ("",None)):
        filetype=filename.split(".")[-1]
        lib=getlibfromfiletype(filetype)
    elif(type(filetype)==str):  
        lib=getlibfromfiletype(filetype)
    else:
        lib=filetype
    return lib.load(filename,**kwargs)

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='argparse')
    parser.add_argument("files",help="输入文件名")
    parser.add_argument("-f","--from", help="输入文件格式")
    parser.add_argument("-t","--to", help="输出文件格式")
    parser.add_argument("-o","--output", help="输出文件名")
    parser.add_argument("-v","--version",action='store_true',help="显示程序版本")
    #parser.add_argument("--list-input-formats",action='store_true',help="显示支持的输入文件格式")
    #parser.add_argument("--list-output-formats",action='store_true',help="显示支持的输出文件格式")
    args = parser.parse_args().__dict__
    if(args["version"]):
        print(__version__)
    else:
        #import ipdb
        #ipdb.set_trace()
        file=args["files"]
        load(file,filetype=args["from"]).save(args["output"],filetype=args["to"])
        #TODO

if(__name__=="__main__"):
    main()