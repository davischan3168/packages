#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys
#import thtml.Tohtml import C2htmlBase
def ebookconvert(ifile,mtype='mobi'):
    """
    make ebook to mobi,epub etc,and so on:
    ifile:which is a input file maybe txt,html files
    """
    if os.path.isfile(ifile):
        ifile=os.path.abspath(ifile)
        ofile=os.path.splitext(ifile)[0]+'.'+mtype
        ofile1=os.path.splitext(ifile)[0]+'.epub'
        cmd='ebook-convert %s %s'%(ifile,ofile)
        cmd1='ebook-convert %s %s'%(ofile,ofile1)
        os.system(cmd)
        os.system(cmd1)
    else:
        sys.exit()
    return

if __name__=="__main__":
    ebookconvert(sys.argv[1])
    
