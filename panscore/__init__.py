import typing
import argparse
import importlib
from typing import List,Tuple,Dict,Union,Type

def getlib(filetype:str):
    """
    输入文件类型，返回对应的读写库
    """
    return importlib.import_module("panscore."+filetype.lower())

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

    def save(self,filename:str,filetype="",**kwargs):
        if(type(filetype)==str):
            if(filetype==""):
                filetype=filename.split(".")[-1]
            lib=getlib(filetype)
        else:
            lib=filetype
        return lib.save(self,filename,**kwargs)
        pass

def load(filename:str,filetype="",**kwargs)->Score:
    """
    打开文件，返回panscore.Score对象
    """
    if(type(filetype)==str):
        if(filetype==""):
            filetype=filename.split(".")[-1]
        lib=getlib(filetype)
    else:
        lib=filetype
    return lib.load(filename,**kwargs)

def main():
    pass

if(__name__=="__main__"):
    main()