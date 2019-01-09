#!/usr/bin/env python3
# -*-coding:utf-8-*-
import json
import os
import sys
from textwrap import wrap
import time
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

class Translator:
    def __init__(self, to_lang='en', from_lang='zh'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        if self.from_lang == self.to_lang:
            return source
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        #print(self.source_list)
        return ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        data = json.loads(json5)
        translation = data['responseData']['translatedText']
        if not isinstance(translation, bool):
            return translation
        else:
            matches = data['matches']
            for match in matches:
                if not isinstance(match['translation'], bool):
                    next_best_match = match['translation']
                    break
            return next_best_match

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19\
                   (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        api_url = "http://mymemory.translated.net/api/get?q=%s&langpair=%s|%s"
        req = request.Request(url=api_url % (escaped_source, self.from_lang, self.to_lang),
                              headers=headers)

        # url="http://translate.google.com/translate_a/t?clien#t=p&ie=UTF-8&oe=UTF-8"
        # +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
        # , headers = headers)
        #print(api_url % (escaped_source, self.from_lang, self.to_lang))
        r = request.urlopen(req)
        return r.read().decode('utf-8')


def google_trans(text,scr,dest,WR=True,nwords=500,splitword=True):
    """
    text:需要翻译的文本，最长的字节不超过500个。
    src:输入文本的语言
    dest：输出的翻译后的文本
    WR:是否输出在文件中，类型是bool
    """
    
    source=_get_text(text=text,nwords=nwords,splitword=splitword)
    translator= Translator(to_lang=dest,from_lang=scr)
    if WR:
        f=open('file_trans_%s.txt'%str(int(time.time()*10000)),'w')
        for text in source:
            text=text.replace('\n','').replace('-','')
            f.write(text+'\n\n')
            try:
                trans=translator.translate(text)
                f.write(trans)
            except:
                f.write("Translated Failed ......")
            f.write('\n\n')
            f.flush()
            time.sleep(0.5)
        f.close()
    else:
        dlist=[]
        for text in source:
            text=text.replace('\n','').replace('-','')
            trans=translator.translate(text)
            dlist.append(trans)
            time.sleep(0.5)
        return dlist

def _get_text(text,nwords=500,splitword=True):
    """
    text:为txt类型file或者是str字符。
    nwords:对字符进行分割，每个单元为500个字符，为int
    splitword：为bool类型，为True时则以句号"。"作为分割字符。
    """
    #source=[]
    if isinstance(text,str):
        if os.path.isfile(text):
            try:
                f=open(text,'r',encoding='utf8')
                cnt=f.read()
                f.close()
            except:
                f=open(text,'r',encoding='gbk')
                cnt=f.read()
                f.close()
        else:
            cnt=text
    elif isinstance(text,list):
        cnt=''.join(text)
    else:
        sys.argv[1]
        
    if splitword:
        source=cnt.split('。')
    else:
        source=[cnt[i:i+nwords] for i in range(0,len(cnt),nwords)]
    return source
    
def Toen(text):
    translator= Translator(to_lang="en",from_lang='zh')
    translation = translator.translate(text)
    #print(translation)
    
    return translation

def Tozh(text):
    translator= Translator(to_lang="zh",from_lang='en')
    translation = translator.translate(text)
    #print(translation)
    
    return translation

def tomp3():
    #https://translate.google.cn/translate_tts?ie=UTF-8&q=How%20are%20you%3F%20I%27m%20very%20good.%20How%20old%20are%20you%3F&tl=en&total=1&idx=0&textlen=44&tk=388671.237525&client=t&ttsspeed=0.24
    return 

    
if __name__=="__main__":
    #pass
    translator= Translator()
    translation = translator.translate("My wife will go to bed.")
    print(translation)
