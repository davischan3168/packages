#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys
import PyPDF2
import PythonMagick
import ghostscript
from PyPDF2 import PdfFileReader, PdfFileWriter



def pdf2jpeg(inputf,outdir,ds=512):
    """
    :param i_file: (str) input pdf file (eg: "/home/file.pdf")
    :param o_dire: (str) output image directory (eg: "/home/")
    split pdf file
    :param ds: (int) set ds = 1024 ~= 1MB output under my test
    :return: splited PNG image file
    """
    flag=True
    ds=str(ds)
    pdf_i = PyPDF2.PdfFileReader(open(inputf, "rb"))
    pages=pdf_i.getNumPages()
    print('Totally get ***{0:^4}*** pages from "{1}", playpdf start......'.format(pages,inputf))
    try:
        image=PythonMagick.Image()
        image.desity(ds)
        for i in range(pages):
            #image = PythonMagick.Image(inputf + '[' + str(i) + ']')
            #image.density(str(ds))
            image.read(inputf + '[' + str(i) + ']')
            image.magick("jpeg")
            image.write(outdir + str(i + 1) + ".jpeg")
            print("{0:>5} page OK......".format(i + 1))
    except Exception as e:
        print(e)
        flag=False
    return flag

def addBlankpage(readFile,outFile):
    #readFile = 'C:/Users/Administrator/Desktop/RxJava 完全解析.pdf'
    #outFile = 'C:/Users/Administrator/Desktop/copy.pdf'
    pdfFileWriter = PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    numPages = pdfFileReader.getNumPages()

    for index in range(0, numPages):
        pageObj = pdfFileReader.getPage(index)
        pdfFileWriter.addPage(pageObj)  # 根据每页返回的 PageObject,写入到文件
        pdfFileWriter.write(open(outFile, 'wb'))

    pdfFileWriter.addBlankPage()   # 在文件的最后一页写入一个空白页,保存至文件中
    pdfFileWriter.write(open(outFile,'wb'))
    return

def splitPdf(readFile,outFile):
    #readFile = 'C:/Users/Administrator/Desktop/RxJava 完全解析.pdf'
    #outFile = 'C:/Users/Administrator/Desktop/copy.pdf'
    pdfFileWriter = PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()

    if numPages > 5:
        # 从第五页之后的页面，输出到一个新的文件中，即分割文档
        for index in range(5, numPages):
            pageObj = pdfFileReader.getPage(index)
            pdfFileWriter.addPage(pageObj)
        # 添加完每页，再一起保存至文件中
        pdfFileWriter.write(open(outFile, 'wb'))
    return

def mergePdf(inFileList, outFile):
    '''
    合并文档
    :param inFileList: 要合并的文档的 list
    :param outFile:    合并后的输出文件
    :return:
    '''
    pdfFileWriter = PdfFileWriter()
    for inFile in inFileList:
        # 依次循环打开要合并文件
        pdfReader = PdfFileReader(open(inFile, 'rb'))
        numPages = pdfReader.getNumPages()
        for index in range(0, numPages):
            pageObj = pdfReader.getPage(index)
            pdfFileWriter.addPage(pageObj)

        # 最后,统一写入到输出文件中
        pdfFileWriter.write(open(outFile, 'wb'))
    return

def getPdfContent(filename):
    pdf = PdfFileReader(open(filename, "rb"))
    content = ""
    for i in range(0, pdf.getNumPages()):
        pageObj = pdf.getPage(i)

        extractedText = pageObj.extractText()
        content += extractedText + "\n"
        # return content.encode("ascii", "ignore")
    return content

if __name__=="__main__":
    i_file = sys.argv[1]  
    o_dire = sys.argv[2]  
    ds = sys.argv[3]  
    if i_file[-4:] == ".pdf":  
        class_image.ManImage(i_file=i_file, o_dire=o_dire).playpdf(ds=ds)  
    else:  
        sys.exit()  
