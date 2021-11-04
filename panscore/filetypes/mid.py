import mido
from typing import Dict,Tuple,List
import panscore

def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象
    mf=mido.MidiFile(filename)
    tracks=[]
    for mtr in mf.tracks:
        notes=[]
        tick=0
        lyric=panscore.defaultlyric
        note:Dict[int,Tuple[str,int]]={}#{音高:(歌词,开始时间)}
        for signal in mtr:
            tick+=signal.time
            if(signal.type=="note_on"):#音符开始事件
                #将新音符注册到键位-音符字典中
                note[signal.note]=(lyric,tick)
            elif(signal.type=="note_off"):
                #从键位-音符字典中找到音符，并弹出
                if(signal.note in note):#音符结束事件
                    n=note.pop(signal.note)
                    notes.append(panscore.Note(start=int(n[1]*480/mf.ticks_per_beat),
                                length=int((tick-n[1])*480/mf.ticks_per_beat),
                                notenum=signal.note,
                                lyric=n[0]))
                    lyric=panscore.defaultlyric
            elif(signal.type=="lyrics"):#歌词事件
                lyric=signal.text
        tracks.append(panscore.Track(name=mtr.name,note=notes))
    return panscore.Score(track=tracks)

def save(score:panscore.Score,filename:str):
    #将panscore.Score对象保存为文件
    mid = mido.MidiFile()
    for tr in score.track:
        messages:List[Tuple[int,mido.Message]]=[]#[(绝对时间，midi事件)]
        #把音符转换为midi事件序列
        for n in tr.note:
            messages.append((n.start,mido.MetaMessage('lyrics',text=n.lyric,time=0)))
            messages.append((n.start,mido.Message('note_on',note=n.notenum,velocity=64,time=0)))
            messages.append((n.start+n.length,mido.Message('note_off',note=n.notenum,velocity=64,time=0)))
        #按时间排序
        message=sorted(messages,key=lambda x:x[0])
        #把时间差写入midi事件，并写入MidiTrack对象
        time=0
        mtr=mido.MidiTrack()
        #mtr.append(mido.MetaMessage("track_name",name=tr.name,time=0))
        for m in messages:
            m[1].time=m[0]-time
            mtr.append(m[1])
            time=m[0]
        mid.tracks.append(mtr)
    mid.save(filename)
