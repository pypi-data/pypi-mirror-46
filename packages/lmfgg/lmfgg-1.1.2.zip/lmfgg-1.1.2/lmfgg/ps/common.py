from bs4 import BeautifulSoup 
import re
import Levenshtein
from lmfgg.common import to_arr
import Levenshtein 

import sys 
from lmfgg.txt import ismat
import time
import json 
import os 
from lmf.dbv2 import db_query,db_write ,db_command

import pandas as pd
from lmfgg.common import getpage


def pat(word,krr):
    words=re.split(":|：",word)
    if len(words)<2:return 0
    word1,word2=words[0],''.join(words[1:])
    if word1=='' or word2=='':return 0
    return ismat(word1,krr)

def ps(page,krr):
    arr=to_arr(page)
    data={}
    for i in range(len(arr)):
        for j in range(3):
            word=''.join(arr[i:i+j+1])
            if pat(word,krr):
                words=re.split(":|：",word)
                k,v=words[0],''.join(words[1:])
                data[k]=v
                break
    return data


def getwordftxt():
    path=os.path.join(os.path.dirname(__file__),'worddict.txt')
    with open(path,'r',encoding='utf8') as f:
        
        lines=f.readlines()
        lines=[ w.replace('\n','') for w in lines ]
    return lines 




def getwordfdb():
    conp=['postgres','since2015','192.168.4.188','base','v1']
    df=db_query("select name from v1.words",dbtype="postgresql",conp=conp)

    arr=df['name'].tolist()
    return arr

def wordttxt(arr):
    path=os.path.join(os.path.dirname(__file__),'worddict.txt')
    words=getwordftxt()
    words.extend(arr)

    words=list(set(words))
    print("共有词%d 个 "%len(words))
    with open(path,'w',encoding='utf8') as f:
        for w in words:
            f.write(w+"\n")

def wordtdb(arr):
    arr=list(set(arr))
    df=pd.DataFrame(data={"name":arr})
    conp=['postgres','since2015','192.168.4.188','base','v1']
    db_write(df,'words_tmp',dbtype="postgresql",conp=conp,if_exists='append')

    sql="insert into v1.words(name) select name from v1.words_tmp where name not in(select name from v1.words)"
    db_command(sql,dbtype="postgresql",conp=conp)

def dbtotxt():
    path=os.path.join(os.path.dirname(__file__),'worddict.txt')
    words=getwordfdb()
    print("共有词%d 个 "%len(words))
    with open(path,'w',encoding='utf8') as f:
        for w in words:
            f.write(w+"\n")


















# krr=list(set(krr))
# df=pd.DataFrame(data={"name":krr})
# conp=['postgres','since2015','192.168.4.188','base','v1']
# db_write(df,'words',dbtype="postgresql",conp=conp,if_exists='append')





# krr=['标段编号', '项目经理', '项目名称', '工期', '中标单位', '中标价',"标段包名称","标段包编号","中标单位"
# ,'异议、投诉受理', '第二中标候选人', '投标费率', '开标地点', '资质等级', '项目编号', '工期', '奖项', '资格等级', '业绩'
# , '最高投标费率', '开标时间', '招标方式', '第三中标候选人', '工程名称', '招标人', '公示时间', '第一中标候选人', '项目总监'
# ,"工程名称","工期天","建造师","单位名称","项目编号","成交金额","成交供应商","项目名称","项目编号","采购单位","流标原因","招标单位"
# ]


# page=getpage("http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20161227/32685317-a525-4fd9-a402-70159914a7a1.html","anhui_anqing")
