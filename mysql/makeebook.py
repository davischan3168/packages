#!/usr/bin/env python3
# -*-coding:utf-8-*-

import webdata.mysql as ql
import webdata.util.ebookconvert as eb

a=['唐诗三百首','宋词三百','小学古诗','初中古诗','高中古诗','诗经']
b=['epub/'+i+'.html' for i in a]
c=['李白','杜甫','白居易','王维','王勃','陆游','李清照']
for i in a:
    ql.Sql2html_GushiByNote(i)

for i in b:
    eb.ebookconvert(i)

for i in c:
    ql.Sql2html_GushiByAuthor(i)

d=['epub/'+i+'.html' for i in c]
for i in d:
    eb.ebookconvert(i)
