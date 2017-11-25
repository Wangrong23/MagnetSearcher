import re
import base64
from urllib import parse
from urllib import request

headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

inputKeyWord = input("输入搜索关键词：")
bytesKeyWord = inputKeyWord.encode(encoding="utf-8")
decodeWord = base64.b64encode(bytesKeyWord)
keyCode = decodeWord.decode()
urlPart1 = "http://www.btwhat.info/search/b-"
urlPart2 = keyCode+"/"
urlPart4 = "-3.html"

def strDecode(uriCode):
    a = re.sub('[+"]', '', uriCode)
    b = parse.unquote(a)
    c = re.compile(r'<[^>]+>',re.S)
    str = c.sub('', b)
    return str

for pageNum in range(1,10):

    url = urlPart1+urlPart2+str(pageNum)+urlPart4
    req = request.Request(url=url,headers=headers)
    res = request.urlopen(req)
    ret = res.read().decode("utf-8")

    itemTitleCode = re.findall(r'<div class="item-title">.*?decodeURIComponent\((.*?)\)\);', ret, re.S)
    magnetCode = re.findall(r'<div class="item-title">.*?<a href="/wiki/(.*?).html" target', ret, re.S)
    fileType = re.findall(r'<span class=\"cpill.*?\">(.*?)</span>', ret, re.S)
    fileSize = re.findall(r'<div class="item-bar">.*?File Size.*?<b.*?>(.*?)</b>', ret, re.S)

    titleList = []
    fileTypeList = []
    fileSizeList = []
    magnetList = []

    itemAmount = len(itemTitleCode)

    for m in range(itemAmount):

        itemTitle=strDecode(itemTitleCode[m])
        titleList.append(itemTitle)
        fileTypeList.append(fileType[m])
        fileSizeList.append(fileSize[m])
        magnetPart1 = "magnet:?xt=urn:btih:"
        magnetPart2 = magnetCode[m]
        magnet = magnetPart1+magnetPart2
        magnetList.append(magnet)

        title = "".join(titleList[m])
        magnet = "".join(magnetList[m])
        type = "".join(fileTypeList[m])
        size = "".join(fileSizeList[m])

        print("\r")
        print("资源名称："+title)
        print("资源类型：" + type)
        print("资源大小：" + size)
        print("磁力链接："+magnet)
        print("\r")
