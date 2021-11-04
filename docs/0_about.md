# 关于panscore

## 命令行工具
panscore提供命令行工具，它能在多种常见的数字乐谱格式间进行转换，类似pandoc。

计算机音乐领域的不同子领域对数字乐谱有不同需求，因此产生了多种格式。例如，编曲软件支持多效果器，打谱软件（如musicxml）支持调号、谱号、音符排版，歌声合成软件（如dv）支持歌词、参数。一般来说，领域内的格式互转已经有成熟的解决方案（如utaformatix），但是在跨领域转换时，常常需要多次格式转换。panscore将为数字乐谱转换提供一站式解决方案。

## python库
panscore是一个python库，为多种乐谱格式提供了一种通用的python对象表示。通过panscore库，开发者可以让自己的乐谱相关python工具支持多种文件格式。

### panscore库的设计思想
1. 轻量简洁。panscore仅支持最基本的乐谱信息，不支持参数等专有信息，也不支持乐理分析等高级功能，无法完美表达乐谱文件中的所有信息。panscore尽量减少对其他库的依赖。（与dvfile不同，dvfile支持dv文件的绝大多数特性，并依赖numpy来处理参数）
2. 通用性。不同文件格式均被表示为统一的对象，以不变应万变。
3. 可扩展性。用户可自行将一种新的文件格式接入panscore。