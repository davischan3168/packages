#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import lxml.html
from io import  StringIO

def Get_Pic(url):
    r=requests.get(url)
    html=lxml.html.parse(StringIO(r.text))
    d=html.xpath('//div[@id="js_content"]//img/@data-src')
    for i in range(len(d)):
        if 'fmt=png?' in d[i]:
            r=requests.get(d[i])
            with open(str(i).zfill(2)+'.png','wb') as f:
                f.write(r.content)

    return

import os
import docx
from docx import Document
from docx.shared import Inches
document = Document()
ll=range(1,13)
lll=[str(i).zfill(2) for i in ll]
lll
lll=[str(i).zfill(2)+'.png' for i in ll]
lll
ii=[]
for i in lll:
    if os.path.exists(i):
        ii.append(i)
ii
for i in ii:
    document.add_picture(i)
document.save('tu.doc')

if__name__==" __main__":
    url='https://mp.weixin.qq.com/s/87kQM5JpGm8UK2067IeBRQ'
