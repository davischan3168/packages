#!/usr/bin/env python3
# -*-coding:utf-8-*-

 
import difflib
import string
import sys

"""
比较两份文件的不同之处，并以html的格式输出。
"""
def readfile(filename):
    try:
        try:
            fileHandle = open(filename,'r',encoding='utf8')
            text = fileHandle.read().splitlines()
        except:
            fileHandle = open(filename,'r',encoding='gbk')
            text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
        print('Read file Error:' + str(error))
        #sys.exit()
        return

def diff_2files_html(textfile1,textfile2): 
    if textfile1 == "" or textfile2 == "":
        print("Usage:test.py filename1 filename2")
        #sys.exit()

    else:
        text1_lines = readfile(textfile1)
        text2_lines = readfile(textfile2)
        d = difflib.HtmlDiff()
        doc=d.make_file(text1_lines,text2_lines)
        #print(d.make_file(text1_lines,text2_lines))
        f=open('diff_file.html','w')
        f.write(r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        #f.write("<meta charset='UTF-8'>")
        f.write(doc)
        f.close()
        """
        ff=open('diff_file.txt','w')
        diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='')
        ff.write('\n'.join(list(diff)))
        ff.close()"""
    return

if __name__=="__main__":
    diff_2files_html(sys.argv[1],sys.argv[2])
