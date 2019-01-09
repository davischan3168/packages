#!/usr/bin/env python3
# -*-coding:utf-8-*-

#from __future__ import division
from io import StringIO
import math
from wand.image import Image # 这里我起了个别名
from PIL import Image as PImage
# 百度OCR最大长度
bai_du_ocr_max = 4096
#主要方法
def convert(file_name, target_width=1500):
    try:
        with Image(filename=file_name) as img:
            image_page_num = len(img.sequence)
            # PDF里面只有一张图片
            if image_page_num == 1:
                # 获取最终图片宽高
                target_width, target_height = _get_one_info(target_width,
                                                            img.width,
                                                            img.height)
                # 缩放，文档上说比resize速度快
                img.sample(target_width, target_height)

                # 如果最终高度大于百度最大高度，则crop
                if target_height > bai_du_ocr_max:
                    img.crop(0, 0, target_width, bai_du_ocr_max)

                # img.save(filename='%s.jpg' % (str(int(time.time())) + '_' +
                # str(img.width)))
                result = img.make_blob('jpg')
                # 下面是准备二值化，发现总体速度还不如直接传给百度
                # paste_image =
                # PImage.open(StringIO.StringIO(img.make_blob('jpg')))
                # paste_image = paste_image.convert("L")
                # paste_image.show()
                # d = StringIO.StringIO()
                # paste_image.save(d, 'JPEG')
                # result = d.getvalue()
            # PDF里面有一张以上图片
            else:
                # 多张时，获取最终宽高、拼接页数
                target_width, target_height, page_num = _get_more_info(
                    target_width, img.width, img.height, image_page_num )
                # 生成粘贴的背景图 (测试多次，发现L比RGB快)
                paste_image = PImage.new('L', (target_width, target_height))
                # 拼接图片
                for i in range(0, page_num):
                    image = Image(image=img.sequence[i])
                    # 计算一张图的高度
                    one_img_height = int(target_height / page_num)
                    # 缩放
                    image.sample(target_width, one_img_height)
                    # 将wand库文件转成PIL库文件
                    pasted_image = PImage.open(StringIO.StringIO(image.make_blob('jpg')))
                    # 将图片粘贴到背景图
                    paste_image.paste(pasted_image, (0, one_img_height * i))
                    # 如果最终高度大于百度最大高度，则crop
                    if target_height > bai_du_ocr_max:
                        paste_image = paste_image.crop((0, 0, target_width,
                                                        bai_du_ocr_max))
                    # 从内存中读取文件
                    d = StringIO.StringIO()
                    # 这里是JPEG不是JPG
                    paste_image.save(d, 'JPEG')
                    result = d.getvalue()
                    # paste_image.save('%s.jpg' % (str(int(time.time())) + '_' +
                    # str(img.width)))
                    # 测试的时候可以打开
                    # paste_image.show()
    except Exception as e:
        result = False
    return result

# 一张时获取宽高,如果图片宽度大于我们想要的宽度，则等比缩放图片高度
def _get_one_info(target_width, img_width, img_height):
    if img_width > target_width:
        ratio = target_width / img_width
        target_height = int(ratio * img_height)
    else:
        target_width = img_width
        target_height = img_height
        return target_width, target_height

# 多张时获取宽高和拼接页数
def _get_more_info(target_width, img_width, img_height, image_page_num):
    one_width, one_height = _get_one_info(target_width, img_width, img_height)
    if one_height < bai_du_ocr_max:
        # 百度最大高度除以每张图高度，向上取整，即拼接图片的数量
        num = int(math.ceil(bai_du_ocr_max / one_height))
        # 取拼接数和总页数的最小值
        page_num = min(num, image_page_num)
        return one_width, one_height * page_num, page_num
    else:
        return one_width, one_height, 1 # 1页

# 调试时候用
"""
def _ocr(content):
    url = '百度OCR链接(自己去百度OCR官网申请就行)'
    img = base64.b64encode(content)
    params = {"image": img}
    params = urllib.urlencode(params)
    request = urllib2.Request(url, params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read()
    # print content
    dict_content = json.loads(content)
    text = "\n".join(map(lambda x: x["words"],dict_content["words_result"]))
    return text
"""

# 调试时候用
def _write_file(path, data, type="w"):
    try:
        f = open(path, '%sb' % type)
    except:
        f = open(path.encode("utf-8"), '%sb' % type)

    f.write(data)
    f.close()
    # 调试时候用
if __name__ == '__main__':
    import sys
    import base64
    import json
    import urllib
    #import urllib2
    import time
    start = time.time()
    source_file = sys.argv[1]
    ret = convert(source_file, 1500)
    end = time.time()
    # 这里我统一保存下文件，方便打开观察
    _write_file(str(end) + '.jpg', ret)
    if ret:
        #text = _ocr(ret)
        pass
    end_parse = time.time()
    print ('____________________________________________')
    print (end - start)
    print( end_parse - end)
    print ('+++++++++++++++++++++++++++++++++++++++++++++')
    #print (text )
