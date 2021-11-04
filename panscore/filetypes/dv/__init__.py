import struct
import panscore

def skreadint(file)->int:
    return struct.unpack("l",file.read(4))[0]

def skreadbytes(file)->bytes:
    return file.read(skreadint(file))

def skreadstr(file)->str:
    try:
        return str(skreadbytes(file),encoding="utf8")
    except UnicodeDecodeError:#如果字符串不能用unicode解码，则返回空字符串，而不会导致程序直接退出
        return ""

def skwritebool(n:bool)->bytes:
    return bytes([int(n)])

def skwriteint(n:int)->bytes:
    return struct.pack("l",n)

def skwritebytes(s:bytes)->bytes:
    return skwriteint(len(s))+s

def skwritestr(s:str)->bytes:
    return skwritebytes(bytes(s,"utf8"))

def skwritelist(l:list)->bytes:
    return skwritebytes(skwriteint(len(l))+b"".join([bytes(n) for n in l]))

def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象
    with open(filename,"rb") as file:
        #文件头
        file.read(48)
        #读曲速标记
        tempo=[]
        for i in range(0,skreadint(file)):
            tempo+=[(skreadint(file),skreadint(file)/100)]
        file.read(4)
        #读节拍标记
        beats=[]
        for i in range(0,skreadint(file)):
            beats+=[(skreadint(file),skreadint(file),skreadint(file))]
        tracks=[]
        for i in range(0,skreadint(file)):#读音轨
            notes=[]
            tracktype=skreadint(file)#合成音轨0，伴奏1
            if(tracktype==0):#合成音轨
                trackname=skreadstr(file)
                mute=(file.read(1)==b'\x01')
                solo=(file.read(1)==b'\x01')
                volume=skreadint(file)
                file.read(4)#左右声道平衡
                file.read(4)#区段占用空间
                for i in range(0,skreadint(file)):#读区段
                    segstart=skreadint(file)
                    seglength=skreadint(file)
                    segname=skreadstr(file)
                    singer=skreadstr(file)
                    file.read(4)#音符占用空间
                    for i in range(0,skreadint(file)):#读音符
                        start=skreadint(file)
                        length=skreadint(file)
                        notenum=115-skreadint(file)
                        skreadint(file)#颤音长度
                        pinyin=skreadstr(file)
                        hanzi=skreadstr(file)
                        file.read(1)
                        skreadbytes(file)#数据块1,包含颤音幅度线和颤音速度线
                        skreadbytes(file)#未知数据块2
                        file.read(18)#音素
                        skreadint(file)#弯曲深度
                        skreadint(file)#弯曲长度
                        skreadint(file)#尾部滑音长度
                        skreadint(file)#头部滑音长度
                        skreadint(file)#音阶
                        skreadstr(file)#交叉拼音
                        skreadint(file)#交叉音阶
                        notes.append(panscore.Note(start=start+segstart,
                                             length=length,
                                             notenum=notenum,
                                             lyric=pinyin))
                    #TODO:支持选择汉字还是拼音
                    #以下是区段参数
                    skreadbytes(file)#音量Volume，取值范围[0,256]
                    skreadbytes(file)#音调Pitch，以音分为单位，转换成midi标准的100倍，0表示按默认音调
                    skreadbytes(file)
                    skreadbytes(file)#气声Breathness，取值范围[0,256]
                    skreadbytes(file)#声线（性别）Gender，取值范围[0,256]
                    skreadbytes(file)
                    skreadbytes(file)
                tracks.append(panscore.Track(name=trackname,note=notes))
        #TODO
    #TODO
    return panscore.Score(track=tracks)
    pass

def dumpnote(note:panscore.Note)->bytes:
    from .data import data2
    b=(skwriteint(note.start)
        +skwriteint(note.length)
        +skwriteint(115-note.notenum)
        +skwriteint(0)
        +skwritestr(note.lyric)
        +skwritestr(note.lyric)
        +b'\x00'
        +skwritebytes(b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xa1\x86\x01\x00\x00\x00\x00\x00'*2
                    +b'\x0c\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        +data2
        +b'\x00\x00\x00\x80?\x00\x00\x00\x80?\x00\x00\x80?\x00\x00\x80?'#音素
        +skwriteint(0)
        +skwriteint(0)
        +skwriteint(20)
        +skwriteint(0)
        +skwriteint(-1)
        +skwritestr("")
        +skwriteint(-1))
    return b

def dumptrack(track:panscore.Track)->bytes:
    tracklen=track.note[-1].start+track.note[-1].length
    b_segment=(skwriteint(7680)
        +skwriteint(tracklen)
        +skwritestr(track.name)
        +skwritestr("")
        +skwritelist([dumpnote(n) for n in track.note])
        
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00'+skwriteint(tracklen+1)+b'\x80\x00\x00\x00'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'+skwriteint(tracklen+1)+b'\xff\xff\xff\xff'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00'+skwriteint(tracklen+1)+b'\x80\x00\x00\x00'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00'+skwriteint(tracklen+1)+b'\x80\x00\x00\x00'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00'+skwriteint(tracklen+1)+b'\x80\x00\x00\x00'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x80\x00\x00\x00'+skwriteint(tracklen+1)+b'\x80\x00\x00\x00'
        +b'\x14\x00\x00\x00\x02\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00'+skwriteint(tracklen+1)+b'\x00\x00\x00\x00'
        )
    b=(b"\0\0\0\0"#tracktype
        +skwritestr(track.name)
        +b"\0\0"
        +skwriteint(30)
        +b"\0\0\0\0"
        +skwritelist([b_segment])
        )
    return b
    pass

def save(score:panscore.Score,filename:str):
    #将panscore.Score对象保存为文件
    #btempo=[skwriteint(i[0])+skwriteint(int(i[1]*100)) for i in self.tempo]
    #bbeats=[numpy.array(i) for i in self.beats]
    b=(b'ext1ext2ext3ext4ext5ext6ext7'
        +b'\x0c\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xe0.\x00\x00'#tempo
        +b'\x10\x00\x00\x00\x01\x00\x00\x00\xfd\xff\xff\xff\x04\x00\x00\x00\x04\x00\x00\x00'#beats
        +skwritelist([dumptrack(tr) for tr in score.track])[4:]
        )
    b=b'SHARPKEY\x05\x00\x00\x00'+skwritebytes(b)
    with open(filename,"wb") as file:
        file.write(b)
    #TODO
    pass