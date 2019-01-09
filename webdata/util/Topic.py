#!/usr/bin/env python3
# -*-coding:utf-8-*-

def text2png(text):
    # Configurations:
    adtexts = [u'---------------', u'广告太多是不对的!']
    textcolor = "#000000"
    adcolor = "#FF0000"
    
    # Don't touch the code below
    #import Image, ImageDraw, ImageFont, uuid
    from PIL import Image, ImageDraw, ImageFont
    import uuid
    
    # Build rich text for ads
    ad = []
    for adtext in adtexts:
        ad += [(adtext.encode('gbk'), adcolor)]
    
    # Wrap line for text
    #   Special treated Chinese characters
    #   Workaround By Felix Yan - 20110508
    wraptext = [""]
    l = 0
    for i in text.decode('utf-8'):
        fi = i.encode('gbk')
        delta = len(fi)
        if i == '\n':
            wraptext += [""]
            l = 0
        elif l + delta > 40:
            wraptext += [fi]
            l = delta
        else:
            wraptext[-1] += fi
            l += delta
            
    # Format wrapped lines to rich text
    wrap = [(text, textcolor) for text in wraptext]
    wrap += ad
    
    # Draw picture
    i = Image.new("RGB", (330, len(wrap) * 17 + 5), "#FFFFFF")
    d = ImageDraw.Draw(i)
    f = ImageFont.truetype("YaHeiYt.ttf", 16)
    for num, (text, color) in enumerate(wrap):
        d.text((2, 17 * num + 1), text.decode('gbk'), font = f, fill = color)
    
    # Write result to a temp file
    filename = uuid.uuid4().hex + ".png" 
    with open(filename, "wb") as s:
        i.save(s, "PNG")
    return filename

if __name__=="__main__":
    text2png('你还还上对方')
