#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys

def ebookconvert(pf):

    op=os.path.split(pf)[0]+'.epub'
    os.system('ebook-convert %s %s'%(pf,op))
    return

if __name__=="__main__":
    ebookconvert(sys.argv[1])
    
