import xml
import panscore
import xmltodict

def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象
    with open(filename,encoding="utf8") as file:
        d=xmltodict.parse(file.read())
    #return d
    d=d["score-partwise"]
    tracks=[]
    #TODO
    pass

if(__name__=="__main__"):
    d=load(r"C:\users\lin\desktop\1.musicxml")
    import json
    with open(r"C:\users\lin\desktop\1.json","w") as file:
        file.write(json.dumps(d,indent=4))
