from bs4 import BeautifulSoup 
import re
import Levenshtein
from lmfgg.common import to_arr
import Levenshtein 

import sys 
from txt import ismat
import time
import json 


def tb1(table):
    #href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20190103/f67eefee-2121-43dc-82f1-968b30837886.html"
    trs=table.find_all('tr')
    data={}
    i=0
    for tr in trs:
        tds=tr.find_all('td')
        if len(tds)==1 and i==0:continue
        tdl=len(tds)
        if tdl%2!=0:continue
        for j in range(int(tdl/2)):
            k=tds[j*2].text.strip()
            v=tds[j*2+1].text.strip()
            data[k]=v
        i=+1
    return data
def tb2(table):
    data={}
    tdrr=[ tr.find_all('td') for tr in table.find_all('tr') ]

    for i in range( int(len(tdrr)/2)):
        ktd,vtd=tdrr[2*i],tdrr[2*i+1]
        for j in range(len(ktd)):
            k=ktd[j].text.strip()
            v=vtd[j].text.strip()
            data[k]=v
    return data 


def calsep(table,krr):

   
    tdrr=[ td.text.strip() for tr in table.find_all('tr') for td in tr.find_all('td')  ]

    tdrr1=[ int(ismat(w,krr)) for w in tdrr]

    s=0
    #print(tdrr1)
    for  i in range(len(tdrr1)):
         if tdrr1[i]!=1:continue
         
         if i+1>=len(tdrr1):break 
         if tdrr1[i+1]==1:
            s+=1


    s1=tdrr1.count(1)-1 if tdrr1.count(1)-1>1 else 1

    v=s/s1 
    return v 


def fm(table):
    x=[ len(tr.find_all('td'))  for tr in table.find_all('tr')]
    return x


