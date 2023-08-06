from bs4 import BeautifulSoup 
import re
import Levenshtein
from lmfgg.common import to_arr
import Levenshtein 
from lmf.dbv2 import db_query
import sys 
from lmfgg.txt import ismat
import time
import json 
import copy
from lmfgg.ps.common import pat
from collections import OrderedDict
htmlparser="lxml"


def g_strings(tag):
    v='$sep$'.join(filter(lambda x:x!='' ,[w.strip() for w in tag.strings]))
    return v 

def tb1(table):
    #href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20190103/f67eefee-2121-43dc-82f1-968b30837886.html"
    soup=BeautifulSoup(table,htmlparser)
    table=soup.find('table')
    trs=table.find_all('tr')
    data=OrderedDict({})
    i=0
    for tr in trs:
        tds=tr.find_all('td')
        if len(tds)==1 and i==0:continue
        tdl=len(tds)
        if tdl%2!=0:continue
        for j in range(int(tdl/2)):
            k=tds[j*2].text.strip()
            #v=tds[j*2+1].text.strip()
            v=g_strings(tds[j*2+1])
            if k not in data.keys():data[k]=v
            else:
                if not isinstance(data[k],list):
                    arr=[copy.deepcopy(data[k]),v]
                    data[k]=arr
                else:
                    data[k].append(v)
        i=+1
    return data

def tb2(table):
    soup=BeautifulSoup(table,htmlparser)
    table=soup.find('table')
    data=OrderedDict({})
    tdrr=[ tr.find_all('td') for tr in table.find_all('tr') ]

    for i in range( int(len(tdrr)/2)):
        try:
            ktd,vtd=tdrr[2*i],tdrr[2*i+1]
            for j in range(len(ktd)):
                k=ktd[j].text.strip()
                #v=vtd[j].text.strip()
                v=g_strings(vtd[j])
                if k not in data.keys():data[k]=v
                else:
                    if not isinstance(data[k],list):
                        arr=[copy.deepcopy(data[k]),v]
                        data[k]=arr
                    else:
                        data[k].append(v)
        except:
            pass
    return data 


def tb3(page,krr):
    soup=BeautifulSoup(page,htmlparser)
    table=soup.find('table')
    tdarr=[  tr.find_all('td') for tr in  table.find_all('tr')  ] 
    data=OrderedDict({})
    for i in range(len(tdarr)):
        tr=tdarr[i]
        for j in range(len(tr)):
            word=tr[j].text.strip()

            if ismat(word,krr):

                k=word
                v=None
                if j+1<len(tr):
                    #hx1=tr[j+1].text.strip()
                    hx1=g_strings(tr[j+1])

                    if not ismat(hx1,krr):
                        v=hx1
                    else:
                        if i+1<len(tdarr) and j<len(tdarr[i+1]):
                            #hx2=tdarr[i+1][j].text.strip()
                            hx2=g_strings(tdarr[i+1][j])
                            if not ismat(hx2,krr):v=hx2
                else:
                    if i+1<len(tdarr):
                        if j<len(tdarr[i+1]):
                            #hx2=tdarr[i+1][j].text.strip()
                            hx2=g_strings(tdarr[i+1][j])
                            if not ismat(hx2,krr):v=hx2
                if v is not None:
                    if k not in data.keys():data[k]=v
                    else:
                        if not isinstance(data[k],list):
                            arr=[copy.deepcopy(data[k]),v]
                            data[k]=arr
                        else:
                            data[k].append(v)

            else:
                continue
    return data


def calsep(table,krr):
    soup=BeautifulSoup(table,htmlparser)
    table=soup.find('table')
    if table is None:return 0
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
    soup=BeautifulSoup(table,htmlparser)
    table=soup.find('table')
    x=[ len(tr.find_all('td'))  for tr in table.find_all('tr')]
    return x


def rev(v,krr):
    data=OrderedDict({})
    arr=v.split("$sep$")
    n=len(arr)
    x=[]
    for i in range(n):
        for j in range(3):
            word=''.join(arr[i:i+j+1])
            if pat(word,krr):
                words=re.split(":|：",word)
                k,v=words[0],''.join(words[1:])
                data[k]=v
                x.append(i)
                break
    brr=copy.deepcopy(arr)
    for i in x:brr.remove(arr[i])
    s=''.join(brr)
    return s,data


def redata(data,krr):
    if data is None:return None
    tmps={}
    rdata={}
    for k in data.keys():
        v=data[k]
        if isinstance(v,list) and len(v)>=1:
            v=v[0]
        s,tmp=rev(v,krr)
        data[k]=s
        for k1 in tmp.keys():
            if k1 in tmps.keys():
                continue
            else:
                tmps[k1]=tmp[k1]
        
    data.update(tmps)
    return data






# sql="select * from t_gg where quyu='anhui_anqing' and href='http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20161101/1844db20-1490-4a09-aca7-440bcd373b9d.html' "

# conp=["postgres","since2015","192.168.4.188","base","v1"]

# df=db_query(sql,dbtype="postgresql",conp=conp)


# page=df.at[0,'page']
