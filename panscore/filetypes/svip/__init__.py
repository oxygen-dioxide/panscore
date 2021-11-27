import os
import json
import panscore

import clr
import System

#导入.net基础库
from System.IO import FileStream,FileMode,FileAccess,FileShare
from System.Runtime.Serialization.Formatters.Binary import BinaryFormatter
#导入xs相关dll
clr.AddReference(os.path.split(os.path.abspath(__file__))[0]+"\\SingingTool.Model.dll")

def parsenote(noteobject)->panscore.Note:
    #解析音符对象
    return panscore.Note(start=noteobject.StartPos,
                    length=noteobject.WidthPos,
                    notenum=noteobject.KeyIndex-12,
                    lyric=noteobject.Lyric)

def parsetrack(trackobject)->panscore.Track:
    #解析音轨对象
    return panscore.Track(name=trackobject.Name,
                     note=[parsenote(i) for i in trackobject.NoteList.GetEnumerator()])

def parsefile(fileobject)->panscore.Score:
    #解析文件对象
    track=[]
    for i in fileobject.TrackList:
        if(i.ToString()=="SingingTool.Model.SingingTrack"):#过滤伴奏音轨，保留合成音轨
            track.append(parsetrack(i))
    #ipdb.set_trace()
    return panscore.Score(track=track)

def load(filename:str)->panscore.Score:
    """
    打开svip文件，返回panscore.Score对象
    """
    serializer = BinaryFormatter()
    reader = FileStream(filename, FileMode.Open, FileAccess.Read)
    for i in range(11):
        reader.ReadByte()
    data = serializer.Deserialize(reader)
    reader.Close()
    return parsefile(data)

def dumpnote(note:panscore.Note)->dict:
    return {"Start":note.start,"Width":note.length,"NoteNumber":note.notenum+12,"Lyric":note.lyric,"HeadTag":0}

def dumptrack(track:panscore.Track)->dict:
    return {"Type":"Singing","AISingerId":"XiaoIce","NoteList":[dumpnote(n) for n in track.note],"PhoneList":[],"RefreshPhone":True,"Pitch":"AgAAAAAS/f+c////////P5z///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==","ReverbPreset":7,"Volume":0.3,"Pan":0.0,"Mute":False}
    pass

def dumpscore(score:panscore.Score)->dict:
    return {"VersionNum":0,"TempoList":[{"Position":0,"BPM":9000}],"BeatList":[{"BarIndex":0,"TimeSignature":{"Numerator":4,"Denominator":4}}],"TrackList":[dumptrack(tr) for tr in score.track],"Quantize":8,"IsNumericalPitchName":True,"FirstNumericalPitchIndex":0}
    pass

def save(score:panscore.Score,filename:str):
    """
    将panscore.Score对象保存为svip文件
    """
    with open(filename,"w",encoding="utf8") as file:
        json.dump(dumpscore(score),file)