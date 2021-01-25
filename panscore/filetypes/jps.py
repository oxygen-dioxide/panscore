import string
import panscore
from typing import Tuple,List,Dict
keydict={"C":0,
    "D":2,
    "E":4,
    "F":5,
    "G":7,
    "A":9,
    "B":11}
notedict={1:60,
    2:62,
    3:64,
    4:65,
    5:67,
    6:69,
    7:71}
    
def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象
    tempo:float=120.0
    beats:Tuple[int,int]=(4,4)
    key:int=0
    content:list=[]

    def donothing(line:str):
        pass

    def parsekey(line:str):
        global key
        line=line[2:].strip(" \n")
        basickey=keydict[line.strip("#$")[0].upper()]
        if("#" in line):
            key=basickey+1
        elif("$" in line):
            key=basickey-1
    
    def parsetempo(line:str):
        global tempo
        tempo=float(line[2:])
    
    def parselyric(line:str):
        global content
        line=line[2:]
        linesplit=""#用/分割的行
        for char in line:
            if ("a"<=char<="z" or "A"<=char<="Z"):
                #如果是英文，则无需分割
                linesplit+=char
            elif(char in string.punctuation+"！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."):
                #标点直接视为分隔符
                linesplit+="/"
            else:
                #如果不是英文，则前后均需分割
                linesplit+="/"+char+"/"
        linesplit.replace("//","/")
        linesplit.replace("//","/")
        content.append(["lyric"]+linesplit.split("/"))

    def parsenote(line:str):
        line=line[2:]
        notes=[]
        for char in line:
            if(char in "0,1,2,3,4,5,6,7"):
                notes.append([int(char),1])
            #TODO：解析时值
        pass

    with open(filename) as file:
        for line in file.readlines():
            {"D":parsekey,
            "J":parsetempo,
            "C":parselyric,
            "Q":parsenote}.get(line[0],donothing)(line)
    #TODO
    pass
