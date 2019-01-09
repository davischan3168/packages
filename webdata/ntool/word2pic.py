#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
from io import  StringIO
from PIL import  Image, ImageFont, ImageDraw
import pygame
pygame.init()

text = u'''可以看到，使用 pyGame ，点阵字体的问题终于搞定了。\n

结合 PIL 和 pyGame\n

pyGame 虽然可以解决点阵字体的渲染问题，但讲到对图片的处理，还是 PIL 更为强大。那
么，我们为什么不把两者结合起来呢？用 pyGame 渲染点阵字体，然后用 PIL 生成整张图
片。\n

代码如下：'''
def text2pic(text):
    im = Image.new("RGB", (300, 50), (255, 255, 255))
    font = pygame.font.Font(os.path.join("C:\Windows\Fonts", "simsun.ttc"), 14)
    rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))

    fname = "circle_blue.png"
    pygame.image.save(rtext,fname)
    line = Image.open(fname)
    #im.show()
    im.paste(line,(10,5))
    im.show()
    return 

if __name__=="__main__":
    text2pic(text)
