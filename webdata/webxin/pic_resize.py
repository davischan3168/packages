#!/usr/bin/env python3
# -*-coding:utf-8-*-

# coding=utf-8 
import Image 
import shutil 
import os 
#https://www.jb51.net/article/136194.htm
  
class Graphics:
    infile = 'D:\\myimg.jpg'
    outfile = 'D:\\adjust_img.jpg'
  
    @classmethod
    def fixed_size(cls, width, height): 
        """按照固定尺寸处理图片"""
        im = Image.open(cls.infile) 
        out = im.resize((width, height),Image.ANTIALIAS) 
        out.save(cls.outfile) 
  
    @classmethod
    def resize_by_width(cls, w_divide_h): 
        """按照宽度进行所需比例缩放"""
        im = Image.open(cls.infile) 
        (x, y) = im.size 
        x_s = x 
        y_s = x/w_divide_h 
        out = im.resize((x_s, y_s), Image.ANTIALIAS) 
        out.save(cls.outfile) 
  
    @classmethod
    def resize_by_height(cls, w_divide_h): 
        """按照高度进行所需比例缩放"""
        im = Image.open(cls.infile) 
        (x, y) = im.size 
        x_s = y*w_divide_h 
        y_s = y 
        out = im.resize((x_s, y_s), Image.ANTIALIAS) 
        out.save(cls.outfile) 
  
    @classmethod
    def resize_by_size(cls, size): 
        """按照生成图片文件大小进行处理(单位KB)"""
        size *= 1024
        im = Image.open(cls.infile) 
        size_tmp = os.path.getsize(cls.infile) 
        q = 100
        while (size_tmp > size) and (q > 0):
            #print q 
            out = im.resize(im.size, Image.ANTIALIAS) 
            out.save(cls.outfile, quality=q) 
            size_tmp = os.path.getsize(cls.outfile) 
            q -= 5
        if q == 100: 
             shutil.copy(cls.infile, cls.outfile) 
  
    @classmethod
    def cut_by_ratio(cls, width, height): 
        """按照图片长宽比进行分割"""
        im = Image.open(cls.infile) 
        width = float(width) 
        height = float(height) 
        (x, y) = im.size 
         if width > height: 
             region = (0, int((y-(y * (height / width)))/2), x, int((y+(y * (height / width)))/2)) 
         elif width < height: 
             region = (int((x-(x * (width / height)))/2), 0, int((x+(x * (width / height)))/2), y) 
         else: 
             region = (0, 0, x, y) 
  
        #裁切图片 
        crop_img = im.crop(region) 
        #保存裁切后的图片 
        crop_img.save(cls.outfile) 




if__name__==" __main__":
    #url='https://mp.weixin.qq.com/s/87kQM5JpGm8UK2067IeBRQ'
    pass
