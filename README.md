# Panscore
[Github](https://github.com/oxygen-dioxide/panscore) [Gitee](https://gitee.com/oxygendioxide/panscore) [BitBucket](https://bitbucket.org/oxygendioxide/panscore/src/main/)

## 介绍
Panscore是支持多种文件格式的数字乐谱转换器，基于python开发，可扩展。

Panscore为多种乐谱格式提供了一种通用的python对象。Panscore不支持参数等引擎专有功能，无法完美表达乐谱文件中的所有信息，但换来了简洁性、通用性。

## 功能
Panscore乐谱对象支持以下属性：
- 音符属性：音高，起始时间，持续时间，歌词

Panscore支持输入以下文件格式：
|文件格式|说明|备注|
|-|-|-|
|nn|[袅袅虚拟歌手](http://dsoundsoft.com/)|不支持汉字拼音双重歌词|
|ust|[UTAU](http://utau2008.xrea.jp/)||

Panscore支持输出以下文件格式：
|文件格式|说明|备注|
|-|-|-|
|nn|[袅袅虚拟歌手](http://dsoundsoft.com/)|单轨，音符量化为60（32分音符）|
|ust|[UTAU](http://utau2008.xrea.jp/)|单轨，音符重叠的工程目前会出现错误|

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

如果你想让Panscore支持一种新的文件格式，请实现以下函数：
```py
import panscore
def load(filename:str)->panscore.Score:
    #打开文件，返回panscore.Score对象

def save(score:panscore.Score,filename:str):
    #将panscore.Score对象保存为文件
```
将文件命名为"<文件格式后缀名>.py"（例如mid.py），放置在panscore\filetypes文件夹下。