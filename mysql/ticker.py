# -*- coding:utf-8 -*-

#安装MYSQL DB for python
import MySQLdb as mdb
conn= mdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='801019',
        db ='SDD',
        charset='utf8'
        )
cur = conn.cursor()
#cur = conn.cursor()

#创建数据表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#插入一条数据
#cur.execute("insert into student values('2','Tom','3 year 2 class','9')")


#修改查询条件的数据
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

#查询,like
sql="select * from gushiwen where author like '%李白%';"
sql="select * from gushiwen where author like '%%%s%%';"%'李白'
cur.execute(sql)

#删除查询条件的数据
d=cur.execute("delete from student where age='9'")
print d
cur.close()
conn.commit()
conn.close()
