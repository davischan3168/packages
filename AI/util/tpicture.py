#!/usr/bin/env python3
# -*-coding:utf-8-*-
# !/usr/bin/python
# -*- coding: utf-8 -*-
 
 
"""
create_author: 蛙鳜鸡鹳狸猿
create_time  : 2016-12-21
program      : *_*convert, resize, reshape and add watermark handlers for image file*_*
"""
 
 
import os
import subprocess
 
 
class ImageHandler:
    """
    Conventional image file program.
    To execute the script you need the third
        "ImageMagick"(http://www.imagemagick.org/ : via yum and apt can easily install) in your OS.
    The developer(me) tested it on my local Linux(Both CentOS and Ubuntu) and Python2.7.12.
    """
    def __init__(self, image):
        """
        Get image to handle.
        :param image: string
            full directory of the image file under handling in OS.
        """
        self.image = image
 
 
    def __repr__(self):
        printer = 'o(>﹏<)o ......Image "{0}" handling...... o(^o^)o'.format(self.image)
        return printer
 
 
    def getattr(self):
        """
        Get image resolving power.
        :return: list
            image attribute of [width, height].
        """
		# attr = os.popen("identify {0}".format(self.image)).next().split()[2].split('x')   # alpha version
		attr = subprocess.getoutput("identify {0}".format(self.image)).split()[2].split('x')
        attr[0] = int(attr[0])
        attr[1] = int(attr[1])
        return attr
 
 
    def handconvert(self, fmat, odir=None):
        """
        Convert image file format.
        :param fmat: string
            image format(eg : "PNG", "JPEG" etc which ImageMagick support) to convert.
        :param odir: string, default : original image directory with underline and specified converted format
            image directory(default or specify both OK) to output.
        :return: none.
        """
        if odir: pass
        else:
            o_fmat = '.' + self.image.split('.')[-1]
            o_odir = self.image.replace('.', '_.')  # irregular directory with '.' or other may cause BUG
            odir = o_odir.replace(o_fmat, '.' + fmat)
        print('o(>﹏<)o ...... Convert "{0}" to "{1}" ...... o(>﹏<)o'.format(self.image, odir))
        try:
            os.system("convert -strip {0} {1}".format(self.image, odir))
        except Exception, e:
            print(e)
 
 
    def handresize(self, wid=None, hei=None, fmat=None, odir=None):
        """
        Resize image resolving power.
        :param wid: int, default : none
            image width to resize. if none, lock aspect ratio with "hei".
        :param hei: int, default : none
            image height to resize. if none, lock aspect ratio with "wid".
        :param fmat: string, default : none
            image format(eg : "PNG", "JPEG" etc which ImageMagick support) to convert.
        :param odir: string, default : original image directory with underline and specified converted format
            image directory(default or specify both OK) to output.
        :return: none.
        """
        if not wid and not hei:
            raise TypeError, 'Argument "wid" and "hei" can not both be None'
        if not wid: wid = ''
        if not hei: hei = ''
        o_fmat = '.' + self.image.split('.')[-1]
        o_odir = self.image.replace('.', '_.')  # irregular directory with '.' or other may cause BUG
        if fmat and not odir      : odir = o_odir.replace(o_fmat, '.' + fmat)
        elif not fmat and not odir: odir = o_odir
        else: pass
        print('o(>﹏<)o ...... Resize "{0}" to "{1}" ...... o(>﹏<)o'.format(self.image, odir))
        try:
            os.system("convert {0} -resize {1}x{2} {3}".format(self.image, wid, hei, odir))
        except Exception, e:
            print(e)
 
 
    def handreshape(self, dep, col, fmat=None, odir=None):
        """
        Reshape image file attribute
        :param dep: int
            image depth to reshape.
        :param col: int
            image color to reshape.
        :param fmat: string, default : none
            image format(eg : "PNG", "JPEG" etc which ImageMagick support) to convert.
        :param odir: string, default : original image directory with underline and specified converted format
            image directory(default or specify both OK) to output.
        :return: none.
        """
        o_fmat = '.' + self.image.split('.')[-1]
        o_odir = self.image.replace('.', '_.')  # irregular directory with '.' or other may cause BUG
        if fmat and not odir      : odir = o_odir.replace(o_fmat, '.' + fmat)
        elif not fmat and not odir: odir = o_odir
        else: pass
        print('o(>﹏<)o ...... Reshape "{0}" to "{1}" ...... o(>﹏<)o'.format(self.image, odir))
        try:
            os.system("convert -strip {0} -depth {1} -colors {2} {3}".format(self.image, dep, col, odir))
        except Exception, e:
            print(e)
 
 
    def handwatermark(self, watermark, locate="center", fmat=None, odir=None):
        """
        Add watermark to image
            This is a mid function and for an optimization better to choose "handoptedwatermark()" below.
        :param watermark: string
            full directory of the watermark file add to in OS.
        :param locate: string, default : "center"(add watermark to the center of image file)
            watermark location("ImageMagick" support four positions and "center") to add.
        :param fmat: string, default : none
            image format(eg : "PNG", "JPEG" etc which ImageMagick support) to convert.
        :param odir: string, default : original image directory with underline and specified converted format
            image directory(default or specify both OK) to output.
        :return: none.
        """
        o_fmat = '.' + self.image.split('.')[-1]
        o_odir = self.image.replace('.', '_.')  # irregular directory with '.' or other may cause BUG
        if fmat and not odir      : odir = o_odir.replace(o_fmat, '.' + fmat)
        elif not fmat and not odir: odir = o_odir
        else: pass
        print('o(>﹏<)o ...... Watermark "{0}" to "{1}" ...... o(>﹏<)o'.format(self.image, odir))
        try:
            os.system("convert {0} {1} -gravity {2} -composite {3}".format(self.image, watermark, locate, odir))
        except Exception, e:
            print(e)
 
 
    def handoptedwatermark(self, watermark, rwid=None, rhei=None, locate="center", fmat=None, odir=None):
        """
        Optimized add watermark function.
        :param watermark: string
            full directory of the watermark file add to in OS.
        :param rwid: float, default : none(do not resize watermark on width level)
            Ratio of watermark width with value among (0, 1) to resize to image file.
        :param rhei: float, default : none(do not resize watermark on height level)
            Ratio of watermark height with value among (0, 1) to resize to image file.
        :param locate: string, default : "center"(add watermark to the center of image file)
            watermark location("ImageMagick" support four positions and "center") to add.
        :param fmat: string, default : none
            image format(eg : "PNG", "JPEG" etc which ImageMagick support) to convert.
        :param odir: string, default : original image directory with underline and specified converted format
            image directory(default or specify both OK) to output.
        :return: none.
        """
        if   (rwid == 0 or (rwid and (rwid < 0 or rwid >= 1))) or (rhei == 0 or (rhei and (rhei < 0 or rhei >= 1))):
            raise TypeError, 'Argument "rwid" and "rhei" can set in (0, 1) or with default None'
        elif not rwid and not rhei:
            self.handwatermark(watermark=watermark, locate=locate, fmat=fmat, odir=odir)
        else:
            image_attribute = self.getattr()
            wid = ''
            hei = ''
            if rwid: wid = int(image_attribute[0] * rwid)
            if rhei: hei = int(image_attribute[1] * rhei)
            watermark_sized = ImageHandler(image=watermark).handresize(wid=wid, hei=hei)
            self.handwatermark(watermark=watermark.replace('.', '_.'), locate=locate, fmat=fmat, odir=odir)
 
 
# self test
if __name__ == "__main__":
    IH = ImageHandler(image="/home/student/src.jpg")
    # print(IH)
    # print(IH.getattr())
    # IH.handconvert(fmat="PNG")
    # IH.handconvert(fmat="JPEG", odir="/home/student/sh/src.JPEG")
    # IH.handresize(wid=1024, fmat="PNG")
    # IH.handresize(hei=1024, odir="/home/student/sh/src.PNG")
    # IH.handresize(wid=1024, hei=123)
    # IH.handreshape(dep=8, col=2)
    # IH.handreshape(dep=8, col=2, fmat="PNG")
    # IH.handreshape(dep=8, col=2, odir="/home/student/src__.JPEG")
    # IH.handwatermark(watermark="/home/student/logo.PNG")
    # IH.handwatermark(watermark="/home/student/logo.PNG", fmat="PNG")
    # IH.handoptedwatermark(watermark="/home/student/logo.PNG")
    # IH.handoptedwatermark(watermark="/home/student/logo.PNG", rwid=.1, rhei=.1,
    #                       locate="southeast", fmat="PNG", odir="/home/student/sh/src_.PNG")
