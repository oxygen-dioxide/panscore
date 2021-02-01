import panscore

def load(filename:str)->panscore.Score:
    with open(filename,"r",encoding="utf8") as file:
        line=file.readline().split(" ")
        tempo=float(line[0])
        beats=(int(line[1]),int(line[2]))
        file.readline()
        note=[]
        for i in file.readlines():
            line=i.strip(" \n").split(" ")
            hanzi=line[0]
            pinyin=line[1]
            start=int(line[2])*60
            length=int(line[3])*60
            notenum=83-int(line[4])
            note+=[panscore.Note(start=start,
                                 length=length,
                                 notenum=notenum,
                                 lyric=pinyin)]
    return panscore.Score(track=[panscore.Track(note=note)])
    pass

def dumpnote(note:panscore.Note)->str:
    s=" ".join(["",note.lyric,
            note.lyric,
            str(note.start//60),
            str(note.length//60),
            str(83-note.notenum),
            "50",
            "50",
            "0",
            "0",
            "0",
            "0",
            ",".join(["100"]+["50"]*100),
            ",".join(["100"]+["50"]*100),
            "0"])+"\n"
    return s

def save(score:panscore.Score,filename:str,track:int=0):
    tr=score.track[track]
    tempo=120
    beats=(4,4)
    nbars=int((tr.note[-1].start+tr.note[-1].length)/(1920*beats[0]/beats[1]))+1
    s="{:.1f} {} {} {} 19 0 0 0 0 0\n{}\n".format(
        tempo,
        beats[0],
        beats[1],
        nbars,
        len(tr.note))
    for i in tr.note:
        s+=dumpnote(i)
    with open(filename,encoding="utf8",mode="w") as file:
            file.write(s)