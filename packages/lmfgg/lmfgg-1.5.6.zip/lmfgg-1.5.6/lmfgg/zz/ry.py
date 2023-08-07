

from lmfgg.table.tbpre import get_pure_tbs,clear,get_tb
from lmfgg.table.tbpre import get_tb
from lmf.dbv2 import db_query ,db_write
from lmf.bigdata import pg2pg
from bs4 import BeautifulSoup
from lmfgg.table.tbdata import ext1
import re
import pandas as pd 
import json
import sys

def ryext1(page):
    columns=["name","zjhm","zclb","zch","zhuanye"]
    page=get_pure_tbs(page)
    if page is None:
        return pd.DataFrame(columns=columns)
    page=page[0]
    soup=BeautifulSoup(page,'lxml')
    tbody=soup.find("tbody")
    trs=tbody.find_all('tr')
    data=[]
    headers=["姓名","身份证号","注册类别","注册号（执业印章号）","注册专业"]
    
    if trs!=[]:
        for tr in trs:
            #tmp=[None if tr.find("td",id=re.compile("tb__[0-9]+_%d"%i)) is  None else tr.find("td",id=re.compile("tb__[0-9]+_%d"%i)).text.strip()  for i in range(1,7)]
            tmp=[None if tr.find("td",attrs={"data-header": w}) is  None else tr.find("td",attrs={"data-header": w}).text.strip()  for w in headers]
            if tmp.count(None)>3:continue
            data.append(tmp)
    df=pd.DataFrame(data=data,columns=columns)
    return df 

def ext(page):
    #第一种page为 多页
    if page.startswith("["):
        pages=json.loads(page)
        dfs=[]
        for page in pages:
            if not  isinstance(page,str):continue
            page=json.loads(page)["trs"]

            tbs=get_pure_tbs(page)
            if tbs is None:continue
            for tb in tbs:
                df=ryext1(tb)
                dfs.append(df)
        if dfs==[]:return None
        df=pd.concat(dfs,ignore_index=False)
        df.index=range(len(df))
        return df 

    #第二种page 为
    elif page.startswith("<ta"):
        dfs=[]
        tbs=get_pure_tbs(page)
        if tbs is None:return None
        for tb in tbs:
            df=ryext1(tb)
            dfs.append(df)

        df=pd.concat(dfs,ignore_index=False)
        df.index=range(len(df))
        return df 
    else:
        return None


def df2df(df):

    df1=pd.DataFrame(columns=["name","zjhm","zclb","zch","zhuanye",'href'])
    for i in df.index:
        page=df.at[i,'zcry']
        href=df.at[i,'href']
        dftmp=ext(page)
        if dftmp is None:continue
        #print(len(dftmp))
        dftmp['href']=href
        df1=df1.append(dftmp)

    return df1



# sql="""SELECT href,zcry FROM "tc"."jianzhu_gg_html"   """

# conp=["postgres","since2015","192.168.4.188","base","tc"]

# df=db_query(sql,dbtype="postgresql",conp=conp)

# pg2pg(sql,'ryzz',conp,conp,f=df2df,chunksize=1000)
# page=df.at[0,'zcry']









