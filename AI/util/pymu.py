#!/usr/bin/env python3
# -*-coding:utf-8-*-

import fitz
import glob
import os
import sys
import re
from time import time
from AI.BDAI.ocr import BD_jsonTtext as jsontext


def rightinput(desc):
    flag=True
    while(flag):
        instr=input(desc)
        try:
            intnum=eval(instr)
            if type(intnum)==int:
                flag=False
        except:
            print('请输入正整数!')

    return intnum

def pdf2png(pdffile):
    doc = fitz.open(pdffile)
    name=os.path.splitext(os.path.basename(pdffile))[0]
    textc='pdf2png/onall.txt'
    flag = rightinput("输入：1：全部页面；2：选择页面\t")
    if flag == 1:
        strat = 0
        totaling = doc.pageCount
    else:
        strat = rightinput('输入起始页面：') - 1
        totaling = rightinput('输入结束页面：')

    if not os.path.exists('pdf2png'):
        os.mkdir('pdf2png')

    if os.path.exists(textc):
        os.remove(textc)
    ff=open(textc,'a',encoding='utf8')
    for pg in range(strat, totaling):
        page = doc[pg]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG('pdf2png/%s_%s.png' %(name, str(pg+1)))
        ff.write(jsontext('pdf2png/%s_%s.png' %(name, str(pg+1))))

    ff.close()

    return



def pic2pdf(path,cc=None):
    doc=fitz.open()
    dff=[]
    if os.path.isdir(path):
        df=glob.glob('%s/*'%path)
        for img in df:
            tt=os.path.splitext(img)
            if tt[1] in ['.png','.jpg','.jepg']:
                dff.append(img)

    if len(dff)>0:
        path1='allimages_%s.pdf'%int(time()*100)
        if cc is not None:
            dfile={}
            for img in dff:
                num=cc.findall(img)
                if len(num)==1:
                    nm=int(num[0])
                    dfile[nm]=img
                else:
                    print('The number of ',num,'is more than one.')
            dd=sorted(dfile.items(),key=lambda item:item[0])
            
            for img in dd:
                print(img[1],'....1......')
                imgdoc=fitz.open(img[1])
                pdfbytes=imgdoc.convertToPDF()
                imgpdf=fitz.open("pdf", pdfbytes)
                doc.insertPDF(imgpdf)
            if os.path.exists(path1):
                os.remove(path1)
            doc.save(path1)
            doc.close()
                

        else:
            for img in sorted(dff):
                print(img,'....2.....')
                imgdoc=fitz.open(img)
                pdfbytes=imgdoc.convertToPDF()
                imgpdf=fitz.open("pdf", pdfbytes)
                doc.insertPDF(imgpdf)
            if os.path.exists(path1):
                os.remove(path1)
            doc.save(path1)
            doc.close()

    else:
        print('There is not picture file in %s'%path)
        sys.exit()       
        
    return
