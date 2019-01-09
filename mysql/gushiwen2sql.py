# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time, re
import sys,os
try:
    import MySQLdb
except:
    import pymysql as MySQLdb
import urllib
from urllib.parse import quote
import pickle
"""
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')   
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')
"""
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
dcap["phantomjs.page.settings.loadImages"] = True    
driver=webdriver.PhantomJS(desired_capabilities=dcap)

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def _wf(path,content,mode='a'):
    f=open(path,mode)
    f.write(content)
    f.flush()
    return

def writePoemBySql(datasets):
    try:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='SDD', charset="utf8")
    except:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='pytest', charset="utf8")
    cur = conn.cursor()
    try:
        cur.executemany("insert into gushiwenI(title,author,content,yiwen,zhus,shangxi,note) value(%s, %s, %s,%s,%s,%s,%s)",datasets)
    except:
        cur.execute("insert into gushiwenI(title,author,content,yiwen,zhus,shangxi) value(%s, %s, %s,%s,%s,%s)",datasets)
    #cur.execute("insert into gushiwen(title,author,content) value(%s, %s, %s)",[title.encode('utf-8'), author.encode('utf-8'),content.encode('utf-8')])
    conn.commit()
    print('Finished insert..')
    cur.close()
    conn.close()
    return

def page_settle(driver,note,mSQL):
    #if mSQL:
    datasets=[]
    #else:
    #    global datasets1
        
    res=driver.find_elements_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="cont"]')
    for elm in res:
        title=elm.find_element_by_xpath('p[1]').text
        author=elm.find_element_by_xpath('p[2]').text
        text=elm.find_element_by_xpath('div[@class="contson"]').text
        textlist=text.split('\n')
        print(title)
        
        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="赏析"]').click()
            sxs=elm.find_element_by_xpath('div[@class="contson"]').text
            sxslist=sxs.split('\n')
            xs=[x for x in sxslist if x not in textlist]
            xstext='\n'.join(xs)
        except Exception as e:
            print("   赏析 Failed")
            xstext=''
            pass

        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="译文"]').click()
            yws=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#993300;"]')
            ywtext=[]
            for yw in yws:
                ywtext.append(yw.text)
            ywstext='\n'.join(ywtext)
        except Exception as e:
            print("   译文 Failed")
            ywstext=''
            pass

        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="注释"]').click()
            zss=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#006600;"]')
            zstext=[]
            for yw in zss:
                zstext.append(yw.text)
            zsstext='\n'.join(zstext)
        except Exception as e:
            print('   注释 Failed')
            zsstext=''
            pass
            
        #if mSQL:
        datasets.append((title,author,text,ywstext,zsstext,xstext,note))
        #else:
        #    datasets1.append((title,author,text,ywstext,zsstext,xstext,note))
    #if mSQL:
    writePoemBySql(datasets)
    return

def Gushiwen2Sql(url,note,mSQL=True):
    """
    按朝代收集，如唐代、宋代等等
    """
    driver.get(url)
    #waitForLoad(driver)
    driver.implicitly_wait(3)
    page_settle(driver,note,mSQL)
    while True:
        try:
            xulr=driver.find_element_by_xpath("//div[@class=\"pages\"]/a[text()='下一页']").get_attribute('href')
            print(xulr)
            driver.get(xulr)
            driver.implicitly_wait(3)
            #waitForLoad(driver)
            page_settle(driver,note,mSQL)
        except Exception as e:
            print(e)
            break
    return

def get_urls(driver):
    urls=driver.find_elements_by_xpath('//div[@class="typecont"]//span')
    
    urlset={}
    for u in urls:
       urlset[u.text] = u.find_element_by_xpath('a').get_attribute('href')
    return urlset

def per_pagesettle(url,note):
    driver.get(url)
    print(url)
    elm=driver.find_element_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="cont"]')
        
    title=elm.find_element_by_xpath('h1').text
    author=elm.find_element_by_xpath('p[1]').text
    text=elm.find_element_by_xpath('div[@class="contson"]').text
    textlist=text.split('\n')
    print(title)
        
    try:
        elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="赏析"]').click()
        sxs=elm.find_element_by_xpath('div[@class="contson"]').text
        sxslist=sxs.split('\n')
        xs=[x for x in sxslist if x not in textlist]
        xstext='\n'.join(xs)
    except Exception as e:
        print("   赏析 Failed")
        xstext=''
        pass

    try:
        elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="译文"]').click()
        yws=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#993300;"]')
        ywtext=[]
        for yw in yws:
            ywtext.append(yw.text)
        ywstext='\n'.join(ywtext)
    except Exception as e:
        print("   译文 Failed")
        ywstext=''
        pass

    try:
        elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="注释"]').click()
        zss=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#006600;"]')
        zstext=[]
        for yw in zss:
            zstext.append(yw.text)
        zsstext='\n'.join(zstext)        
    except Exception as e:
        print('   注释 Failed')
        zsstext=''
        pass

    return (title,author,text,ywstext,zsstext,xstext,note)

def Gushiwen2Gb(url,note):
    driver.get(url)
    #waitForLoad(driver)
    driver.implicitly_wait(3)
    global dataset
    urls=get_urls(driver)

    for k,v in urlset.items():
        try:
            dataset.append(per_pagesettle(url,note))
        except Exception as e:
            print(e)
    return
            
def Gushiwen2Groupby(url,note):
    """
    收集同系列的诗歌，如诗经、唐诗三百首、宋词三百首。
    
    """
    driver.get(url)
    #waitForLoad(driver)
    driver.implicitly_wait(3)
    urls=driver.find_elements_by_xpath('//div[@class="typecont"]//span')
    
    urlset={}
    #dataset=[]
    for u in urls:
       urlset[u.text] = u.find_element_by_xpath('a').get_attribute('href')

    for k,v in urlset.items():
        print(v)
        if v is None:
            continue
        
        driver.get(v)
        #print(v)
        elm=driver.find_element_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="cont"]')
        
        title=elm.find_element_by_xpath('h1').text
        author=elm.find_element_by_xpath('p[1]').text
        text=elm.find_element_by_xpath('div[@class="contson"]').text
        textlist=text.split('\n')
        #print(title)
        
        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="赏析"]').click()
            sxs=elm.find_element_by_xpath('div[@class="contson"]').text
            sxslist=sxs.split('\n')
            xs=[x for x in sxslist if x not in textlist]
            xstext='\n'.join(xs)
        except Exception as e:
            print("   赏析 Failed")
            xstext=''
            pass

        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="译文"]').click()
            yws=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#993300;"]')
            ywtext=[]
            for yw in yws:
                ywtext.append(yw.text)
            ywstext='\n'.join(ywtext)
        except Exception as e:
            print("   译文 Failed")
            ywstext=''
            pass

        try:
            elm.find_element_by_xpath('div[@class="yizhu"]/img[@alt="注释"]').click()
            zss=elm.find_elements_by_xpath('div[@class="contson"]//span[@style="color:#006600;"]')
            zstext=[]
            for yw in zss:
                zstext.append(yw.text)
            zsstext='\n'.join(zstext)        
        except Exception as e:
            print('   注释 Failed')
            zsstext=''
            pass

        #if sys.platform == 'win32':
        #print(title,author,text,ywstext,zsstext,xstext,note)
        writePoemBySql([(title,author,text,ywstext,zsstext,xstext,note)])
        #dataset.append((title,author,text,ywstext,zsstext,xstext,note))
        #else:
        #    writePoemBySql((title,author,text,ywstext,zsstext,xstext,note))
    
    return #dataset
    

def Search2Sql(title,mSQL=True):
    sch=urllib.parse.quote(title)
    url='http://so.gushiwen.org/search.aspx?value='+sch
    driver.get(url)
    #waitForLoad(driver)
    driver.implicitly_wait(3)
    page_settle(driver,mSQL)
    while True:
        try:
            xulr=driver.find_element_by_xpath("//div[@class=\"pages\"]/a[text()='下一页']").get_attribute('href')
            print(xulr)
            driver.get(xulr)
            #waitForLoad(driver)
            driver.implicitly_wait(3)
            page_settle(driver,mSQL)
        except Exception as e:
            print(e)
            break
    return


def _guwentext(url):
    driver.get(url)
    driver.find_element_by_xpath('//div[@class="contson"]')
    gw=driver.find_element_by_xpath('//div[@class="contson"]').text
    try:
        driver.find_element_by_link_text("译注").click()
        gwzs=driver.find_element_by_xpath('//div[@class="shisoncont"]').text
    except:
        gwzs='Null'
    return gw,gwzs

def _List_Book(url,mtype):
    driver.get(url)
    txt=driver.find_elements_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="bookcont"]/ul/span/a')
    if len(txt)==0:
        txt=driver.find_elements_by_xpath('//div[@class="left"]/div[@class="sons"]/div[@class="bookcont"]//span/a')
    s={}
    try:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='SDD', charset="utf8")
    except:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='pytest', charset="utf8")
    cur = conn.cursor()
    cur.execute('select book from Guwen where sset like "%%%s%%"'%mtype)
    ds=set()
    dd=cur.fetchall()
    for i in dd:
        ds.add(i[0])

    cur.close()
    conn.close()
    
    for d in txt:
        bookname=d.text
        if bookname not in ds:
            s[bookname]=d.get_attribute('href')
    return s

def booktext(url,name,mtype):
    booklst=_List_Book(url,mtype)
    text=[]
    for k,v in booklst.items():
        gw,zs=_guwentext(v)
        text.append((mtype,name,k,gw,sz))
    return text        
        

def _guwen(mtype):
    url='http://so.gushiwen.org/guwen/Default.aspx?p=1&type=%s'%quote(mtype)
    driver.get(url)
    driver.implicitly_wait(3)
    lsd={}
    ds=driver.find_elements_by_xpath('//div[@class="sonspic"]/div[@class="cont"]/p[1]/a[1]')
    for d in ds:
        name=d.text
        href=d.get_attribute('href')
        lsd[name]=href
        print(name,href)

    while True:
        old=driver.page_source
        try:
            driver.find_element_by_link_text('下一页').click()
            driver.implicitly_wait(3)
            #driver.find_elements_by_xpath('//div[@class="main3"]/div[@class="left"]/div[@class="pages"]/a[@last()]').click()
            if old == driver.page_source:
                break
            else:
                ds=driver.find_elements_by_xpath('//div[@class="sonspic"]/div[@class="cont"]/p[1]/a[1]')
                for d in ds:
                    name=d.text
                    href=d.get_attribute('href')
                    lsd[name]=href
                    print(name,href)
        except:
            break

    return lsd
        
def guwen(mtype,sql=True):
    booklist=_guwen(mtype)
    #allbook=[]
    for k,v in booklist.items():
        bookn=[]
        chartL=_List_Book(v,mtype)
        for k1,v1 in chartL.items():
            print(k1)
            if sql:
                try:
                    gw,gwzs=_guwentext(v1)
                    bookn.append((mtype,k,k1,gw,gwzs))
                except Exception as e:
                        print(e)
            else:
                pathdir=mtype+'/'+k
                if not os.path.exists(pathdir):
                    try:
                        os.mkdir(pathdir)
                    except:
                        os.makedirs(pathdir)
                pathfile=pathdir+'/'+k1+'.txt'
                if not os.path.exists(pathfile):
                    try:
                        gw,gwzs=_guwentext(v1)
                        f=open(pathfile,'a',encoding='utf8')
                        f.write(gw+'\n\n'+gwzs)
                        f.close()
                    except Exception as e:
                        print(e)
                        #pass
        writeGuwenBySql(bookn,k)
        #print(allbook)
        #print('%s finished'%k)
    return             


def writeGuwenBySql(datasets,book):
    try:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='SDD', charset="utf8")
    except:
        conn = MySQLdb.connect(host="localhost", port=3306, user='root',passwd='801019', db='pytest', charset="utf8")    
    cur = conn.cursor()
    try:
        cur.executemany("insert into Guwen(sset,book,charpter,content,zhushi) value (%s, %s, %s,%s,%s)",datasets)
    except:
        cur.execute("insert into Guwen(sset,book,charpter,content,zhushi) value (%s, %s, %s,%s,%s)",datasets)
    #cur.execute("insert into gushiwen(title,author,content) value(%s, %s, %s)",[title.encode('utf-8'), author.encode('utf-8'),content.encode('utf-8')])
    conn.commit()
    print('Finished ------------------%s'%book)
    cur.close()
    conn.close()
    return


    
    
    
if __name__ == "__main__":
    #XueQiu('000039')
    #url='http://so.gushiwen.org/type.aspx?p=48&c=%e5%85%83%e4%bb%a3&x=%e6%9b%b2'
    #dataset1=[]
    #Gushiwen2Sql(sys.argv[1],sys.argv[2])
    dataset=Gushiwen2Groupby(sys.argv[1],sys.argv[2])
    #元代，81页
    """
    conn = MySQLdb.connect(host="localhost", port=3306,
                           user='root',passwd='801019', db='SDD',
                           charset="utf8")
    cur = conn.cursor()
    sql="insert into Guwen1(sset,book,charpter,content,zhushi) value (%s, %s, %s,%s,%s)"
    datasets=guwen(sys.argv[1])
    """
    #datasets=guwen(sys.argv[1])
    pass
    

