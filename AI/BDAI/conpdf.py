#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import string
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
import sys
from PyPDF2 import PdfFileReader,PdfFileWriter
import time


 

def file_name(file_dir, suffix =[ ".jpg",'.jpeg','.png']):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in suffix:
                L.append(os.path.join(root, file))
    return L

 


def picsTpdf(f_pdf , filedir, suffix):
    #f_pdf pdf file path ,include filename
    #filedir pic file path
    #suffix pic file suffix examples: .jpg
    (w, h) = landscape(A4)
    #print('w:%s,h:%s'%(w,h))
    #c = canvas.Canvas(f_pdf, pagesize = landscape(A4))
    c = canvas.Canvas(f_pdf, pagesize = (21*cm,29*cm))
    fileList = file_name(filedir, suffix)

    for f in fileList:
        (xsize, ysize) = Image.open(f).size

        ratx = xsize / w
        raty = ysize / h
        ratxy = xsize / (1.0 * ysize)
        if ratx > 1:
            ratx = 0.99
        if raty > 1:
            raty = 0.99

        rat = ratx

        if ratx < raty:
            rat = raty
        widthx = w * rat
        widthy = h * rat
        widthx = widthy * ratxy
        posx = (w - widthx) / 2
        if posx < 0:
            posx = 0
        posy = (h - widthy) / 2
        if posy < 0:
            posy = 0

        mw=widthx-2*posx
        mh=widthy
        #print('posx:%s,posy:%s,widthx:%s,widthy:%s'%(posx, posy, widthx, widthy))
        #c.drawImage(f, posx, posy, widthx, widthy)
        c.drawImage(f, 0, 0, 21*cm, 29*cm)
        #c.drawImage(f,posx,posy, widthx, mh)
        #c.drawImage(f, posx, posy, posx, posy)
        c.showPage()
        #c.drawImage(f, posx, posy, widthx-2*cm, widthy)
        #c.showPage()
    c.save()
    #print("Image to pdf success!")
    return

def MergePDFs(filepath,outfile='outpdf.pdf'):
    output=PdfFileWriter()
    outputPages=0
    pdf_fileName=file_name(filepath, suffix =[".pdf"])
    for each in pdf_fileName:
        print(each)
        # 读取源pdf文件
        input = PdfFileReader(open(each, "rb"))

        # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
        if input.isEncrypted == True:
            input.decrypt("map")

        # 获得源pdf文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        print(pageCount)

        # 分别将page添加到输出output中
        for iPage in range(0, pageCount):
            output.addPage(input.getPage(iPage))


    print("All Pages Number:"+str(outputPages))
    # 最后写pdf文件
    outputStream=open(filepath+outfile,"wb")
    output.write(outputStream)
    outputStream.close()
    print("finished")
    return

if __name__=="__main__":
    #conpdf('test1.pdf','audio','.jpeg')
    pass#drawImage
