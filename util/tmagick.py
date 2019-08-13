#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys
import os
import PyPDF2
from PIL import Image
from PIL import Image as image
import ghostscript
from PyPDF2 import PdfFileReader, PdfFileWriter
if sys.platform.startswith('win'):
    import PythonMagick
elif sys.platform in ['linux']:
    import pgmagick as PythonMagick


def Pdf2Jpeg(inputf,outdir=None,start='',end='',ds=128,mtype='jpeg'):
    """
    :param i_file: (str) input pdf file (eg: "/home/file.pdf")
    :param o_dire: (str) output image directory (eg: "/home/")
    split pdf file
    :param ds: (int) set ds = 1024 ~= 1MB output under my test
    mtype='jpeg'
    :return: splited PNG image file
    将pdf文件转化为jpg的图片文件
    """
    pdf_i = PyPDF2.PdfFileReader(open(inputf, "rb"))
    pages=pdf_i.getNumPages()
    lp=len(str(pages))
    oput=os.path.splitext(os.path.abspath(inputf))[0]
    if outdir is None:
        outdir=oput
    print('Totally get ***{0:^4}*** pages from "{1}", playpdf start......'.format(pages,inputf))

    if start=='':
        start=0
    elif int(start)>0:
        start=int(start)-1
    else:
        #start=int(start)
        pass
    if end=='':
        end=pages
    else:
        end=int(end)+1
        
    try:
        image=PythonMagick.Image()
        image.density(str(ds))
        for i in range(start,end):
            pagepath=outdir +'第'+ str(i + 1).zfill(lp)+'页' + ".jpeg"
            if not os.path.exists(pagepath):
                #image = PythonMagick.Image(inputf + '[' + str(i) + ']')
                #image.density(str(ds))
                image.read(inputf + '[' + str(i) + ']')
                image.magick(mtype)
                image.write(outdir +'_页面_'+ str(i + 1).zfill(lp)+ ".jpeg")
                print("{0:>5} page OK......".format(i + 1))
    
    except Exception as e:
        print(e)
        #flag=False
    return

def addBlankpage(readFile,outFile):
    #readFile = 'C:/Users/Administrator/Desktop/RxJava 完全解析.pdf'
    #outFile = 'C:/Users/Administrator/Desktop/copy.pdf'
    """
    在文件后增加一页空白页
    """
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

def draw_pdf(readFile,outFile,*getpages):
    """
    提取pdf文件中的某些页面，具体体现在getpages之中。
    
    """
    #readFile = 'C:/Users/Administrator/Desktop/RxJava 完全解析.pdf'
    #outFile = 'C:/Users/Administrator/Desktop/copy.pdf'
    pdfFileWriter = PdfFileWriter()

    # 获取 PdfFileReader 对象
    pdfFileReader = PdfFileReader(readFile)  # 或者这个方式：pdfFileReader = PdfFileReader(open(readFile, 'rb'))
    # 文档总页数
    numPages = pdfFileReader.getNumPages()

    for index in getpages:
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



def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    print(size/1024)
    return size / 1024

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    mdir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(mdir, suffix)
    return outfile

def compress_image(infile, outfile='', mb=150, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    #print(o_size)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)

def resize_image(infile, outfile='', x_s=1376):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    outfile = get_outfile(infile, outfile)
    out.save(outfile)
    return
    

#等比例压缩图片
'''
  image.ANTIALIAS还有如下值：
  NEAREST: use nearest neighbour
  BILINEAR: linear interpolation in a 2x2 environment
  BICUBIC:cubic spline interpolation in a 4x4 environment
  ANTIALIAS:best down-sizing filter
'''
def resizeImg(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h
        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio
        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])
    return

#裁剪压缩图片
def clipResizeImg(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比
    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)
        x = 0
        y = (ori_h - height) / 3
    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)
        x = (ori_w - width) / 2
        y = 0
    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None
    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])
    return
#水印(这里仅为图片水印)
def waterMark(**args):
    args_key = {'ori_img':'','dst_img':'','mark_img':'','water_opt':''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    mark_im = image.open(arg['mark_img'])
    mark_w,mark_h = mark_im.size
    option ={'leftup':(0,0),'rightup':(ori_w-mark_w,0),'leftlow':(0,ori_h-mark_h),'rightlow':(ori_w-mark_w,ori_h-mark_h)}
    im.paste(mark_im,option[arg['water_opt']],mark_im.convert('RGBA'))
    im.save(arg['dst_img'])
    return
    

if __name__=="__main__":
    pass
    """
    i_file = sys.argv[1]  
    o_dire = sys.argv[2]  
    ds = sys.argv[3]  
    if i_file[-4:] == ".pdf":  
        class_image.ManImage(i_file=i_file, o_dire=o_dire).playpdf(ds=ds)  
    else:  
        sys.exit()  
    """
