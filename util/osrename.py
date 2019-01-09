# encoding:utf-8
##
# 实现批量修改文件夹下说有文件的名称，循环所有的文件夹
# 
##
import os
import sys

#fs=os.listdir(pf)
# 修改文件名
def rename_file(pf):
    for (pf,dirs,files) in os.walk(pf):
        for old in files:
            #print filename
            old=old.strip()
            tem=old.replace('[','〔')
            new=tem.replace(']','〕')
            try:
                os.rename(pf+'/'+old,pf+'/'+new)
                print (old + ' ---> ' + new)
            except Exception as e:
                print(e)
    return

#修改文件夹名称
def rename_dir(pf):
  for parent, dirnames, filenames in os.walk(pf, topdown=False):
    for dirname in dirnames:
      pathdir = os.path.join(parent, dirname)
      new_pathdir = os.path.join(parent, dirname.replace('[','〔').replace(']','〕'))
      if pathdir == new_pathdir: #如果文件夹名本身就是全小写
        continue
      print(pathdir + ' ---> ' + new_pathdir)
      os.rename(pathdir, new_pathdir)
  return
      
if __name__=="__main__":
    pf=sys.argv[1]
    #print (pf)
    rename_dir(pf)
    rename_dir(pf)
