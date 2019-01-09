#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape,portrait
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm

def splitimage2A4(src, dstpath=''):
    """
    将一个长图切割成A4大小的数张图
    """
    img = Image.open(src)
    w,h = img.size
    height=w*297/210 #A4纸比例出的高度
    height_dim=w*297/210# 记录一个固定值，方便后期调用
    num=h/height+1#将分割出的图片数量
    index=0
    print(height)
    s = os.path.split(src)#分割出路径和文件名
    if dstpath == '':
        dstpath = s[0]
    fn = s[1].split('.')
    basename = fn[0]#文件名
    postfix = fn[-1]#后缀名
    img_urls=[]
    #print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
    
    
    while (index < num):
        print ('The index is:', index,"height is ",height)
        #box = (0, height-1527, w, height)
        box = (0, height-height_dim, w, height)
        img.crop(box).save(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix), img.format)
        img_urls.append(os.path.join(dstpath, basename + '_' + str(index) + '.' + postfix))
        #height = height + 1527
        height=height+height_dim
        index = index + 1

    return img_urls

# 零散，大小一致图片，存储为pdf
def imgtopdf(input_paths, outputpath=''):
    """将数张大小一致的图存储为pdf文件"""
    index=0
    # 取一个大小
    if outputpath=='':
        import datetime
        outputpath='combinefiles_%s.pdf'%datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d-%H:%M:%S')
    (maxw, maxh) = Image.open(input_paths[0]).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    for ont_path in input_paths :
        c.drawImage(ont_path, 0, 0, maxw, maxh)
        c.showPage()
        index=index+1
    c.save()
    return

def imgsTpdf(longPicpath):
    """将一张长图切割为A4大小的数张图，并存储为一pdf文件"""
    d=splitimage(longPicpath)
    d.pop(-1)
    imgtopdf(d)
    return

def imgtopdf_signal(input_path, outputpath=''):
    """将一张长图直接转为一个pd文件f"""
    #index=0
    # 取一个大小
    if outputpath=='':
        import datetime
        outputpath='combinefiles_%s.pdf'%datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d-%H:%M:%S')
    (maxw, maxh) = Image.open(input_path).size
    c = canvas.Canvas(outputpath, pagesize=portrait((maxw, maxh)))
    #for ont_path in input_paths :
    c.drawImage(input_path, 0, 0, maxw, maxh)
    c.showPage()
    #index=index+1
    c.save()
    return


if __name__=="__main__":
    splitimage2A4(sys.argv[1])
