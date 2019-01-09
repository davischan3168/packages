# -*- coding:utf-8 -*- 
"""

"""
import sys
import os
import PyPDF2
import PythonMagick
import ghostscript
from webdata.AI.ocr import jsonTtext

def Pdf2Pic(pdffilename,ds=2048,start=0,end=None):
    """
    param pdffilename: (str) input pdf file (eg: "/home/file.pdf") 
    param ds: (int) set ds = 1024 ~= 1MB output under my test
    """
    
    pdf_im = PyPDF2.PdfFileReader(pdffilename)
    npage = pdf_im.getNumPages()

    df=os.path.splitext(pdffilename)
    dn=df[0].split('/')[-1]
    if not os.path.exists(dn):
        dirs=os.mkdir(dn)
    abspf=os.path.abspath(pdffilename)

    os.chdir(dn)
    if start is None:
        start=0
    if end is None or end > npage:
        end=npage
        
    print('Converting %d pages.' % npage)
    atext=[]
    for p in range(start,end):
        im = PythonMagick.Image(abspf + '[' + str(p) +']')
        im.density(str(ds))
        im.magick("PNG")
        path='file_out-' + str(p)+ '.png'
        im.write(path)
        atext.append(jsonTtext(path))
    os.chdir('../')
    d='\n'.join(atext)
    f=open('temp.txt','w',encoding='utf8')
    f.write(d)
    f.close()
    return d



if __name__=="__main__":
    d=Pdf2Pic(sys.argv[1])
