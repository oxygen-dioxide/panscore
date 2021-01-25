import panscore
def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象
    #由于编码不确定，先用二进制打开文件
    with open(filename,'rb') as f:
        file=f.read()

    #读取编码
    if(b"Charset=UTF-8" in file):
        encoding="utf-8"
    else:
        encoding="shift-JIS"
    #分块
    blocks=[]
    block=[]
    for line in file.split(b"\n"):
        line=line.strip(b"\r")
        #逐行解码
        try:
            linestr=str(line,encoding=encoding)
        except UnicodeDecodeError:
            #如果某行编码与其他行不同，则尝试用各种编码解析
            for i in ["gbk","utf-8","shift-JIS"]:
                try:
                    linestr=str(line,encoding=i)
                    break
                except UnicodeDecodeError:
                    pass
            else:
                linestr=""
        if(linestr.startswith("[")):
            blocks.append(block)
            block=[]
        block.append(linestr)
    #读文件头
    """
    fileproperties={}
    for line in blocks[2]:
        if("=" in line):
            [key,value]=line.split("=")
            if(value!=""):
                fileproperties[key]=ustvaluetyper(key,value)
    tempo=fileproperties.pop("Tempo",120.0)
    """
    #读音符
    notes=[]
    time=0
    for block in blocks[3:]:
        noteproperties={}
        length=0
        notenum=60
        lyric="R"
        for line in block:    
            if("=" in line):
                [key,value]=line.split("=")
                if(key=="Length"):
                    length=int(value)
                elif(key=="NoteNum"):
                    notenum=int(value)
                elif(key=="Lyric"):
                    lyric=value.strip(" \n")
        if(not (lyric in {"R","r"})):
            notes.append(panscore.Note(start=time,
                                       length=length,
                                       notenum=notenum,
                                       lyric=lyric))
        time+=length
    return panscore.Score(track=[panscore.Track(note=notes)])
    #TODO
    pass

notetemplate="[#{:0>4}]\nLength={}\nNoteNum={}\nLyric={}\n"

def save(score:panscore.Score,filename:str):
    #将panscore.Score对象保存为文件
    #s='[#VERSION]\nUST Version1.2\nCharset=UTF-8\n[#SETTING]\n'
    #i=0#音符序号
    #TODO
    pass