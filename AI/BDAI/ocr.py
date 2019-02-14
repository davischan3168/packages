#!/usr/bin/env python3
# -*-coding:utf-8-*-

from aip import AipOcr
from urllib import request
import requests
import sys
import os

""" 你的 APPID AK SK """
#http://ai.baidu.com/docs#/OCR-Python-SDK/top
APP_ID = '10947557'
API_KEY = 'KxCS71VeSUFLk00pUvk641Xz'
SECRET_KEY = 'R8cnb80t6CmYXefE7aYzhro1goMLCjyZ'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_token(key,secrect):
    host ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(key,secrect)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    content=response.read()
    if content:
        data=json(content)
        return data['access_token']
    else:
        sys.exit()


    """ 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def BD_picTword(filePath):    
    image = get_file_content(filePath)

    """ 调用通用文字识别, 图片参数为本地图片 """
    #client.basicGeneral(image);

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    d=client.basicGeneral(image, options)#用完500次后可改
    #d = client.basicAccurate(image)

    #url = "https//www.x.com/sample.jpg"

    """ 调用通用文字识别, 图片参数为远程url图片 """
    #client.basicGeneralUrl(url);

    """ 如果有可选参数 """
    #options = {}
    #options["language_type"] = "CHN_ENG"
    #options["detect_direction"] = "true"
    #options["detect_language"] = "true"
    #options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为远程url图片 """
    #client.basicGeneralUrl(url, options)
    return d

def BD_jsonTtext(filePath):
    d=BD_picTword(filePath)
    dd=[]
    for i in d['words_result']:
        dd.append(i['words'])

    text='\n'.join(dd)
    return text

def BD_Pic_Text_dir(filepath):
    text=[]
    for root,dirs,files in os.walk(filepath):
        for f in files:
            paf=os.path.join(root,f)
            try:
                txt=BD_jsonTtext(paf)
                text.append(txt)
                print('page %s is ok'%f)
            except Exception as e:
                print(e)

    dd='\n\n'+'--'*30+'\n\n'
    ds=dd.join(text)
    f=open('%s.txt'%(os.path.dirname(filepath)),'w',encoding='utf8')
    f.write(ds)
    f.close()
    return text

def BD_table_orc(path,mtype='excel'):
    """
    获得一张页面图片的表格文字
    """
    image=get_file_content(path)

    if mtype=='excel':
        options={}
        options["result_type"] = "excel"
        temp=client.tableRecognition(image,options)
        r=requests.get(temp['result']['result_data'])
        #f=open('temp_cxc.xls','wb',encoding='utf8')
        f=open('temp_cxc.xls','wb')
        """
        存放在当前目前下
        """
        f.write(r.content)
        f.close()
        return True

    else:
        options={}
        options["result_type"] = "json"
        temp=client.tableRecognition(image,options)
        s=json.loads(temp['result']['result_data'])
        return s['forms'][0]['body']

        
def BD_ocr1By1dir(dirname):
    for root,dirs,files in os.walk(dirname):
        for f in files:
            if os.path.splitext(f)[1] in ['.jpg','.png''.jpeg']:
                f=os.path.abspath(root+'/'+f)
                try:
                    print(f)
                    op=os.path.splitext(f)[0]+'.txt'
                    if not os.path.exists(op):
                        d=BD_jsonTtext(f)
                        if len(d.strip())>0:
                            with open(op,'w',encoding='utf8') as ff:
                                ff.write(d)
                            os.remove(f)
                            print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    return
def BD_ocrAllIn1dir(dirname):
    Al='output_allinone.txt'
    ff=open(Al,'a',encoding='utf8')
    for root,dirs,files in os.walk(dirname):
        for f in files:
            if os.path.splitext(f)[1] in ['.jpg','.png''.jpeg']:
                f=os.path.abspath(root+'/'+f)
                try:
                    d=BD_jsonTtext(f)
                    print(f)
                    if len(d.strip())>0:
                        ff.write(d+'\n\n')
                        ff.write('----- %s ----\n\n'%f)
                        ff.flush()                        
                        os.remove(f)
                        print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    ff.close()
    return    

if __name__=="__main__":
    text=BD_ocr1By1dir(sys.argv[1])        
