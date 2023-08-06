from lmfgg.getdata import extpage_ol 

from lmf.dbv2 import db_query

from price import extprice
import time 
from name import extname,reclear_qyname
from mytime import exttime  
import pandas as pd
from lmfgg.getdata import initwords_ol,final
from lmf.bigdata import pg2pg
from sqlalchemy.dialects.postgresql import TEXT,BIGINT,TIMESTAMP,NUMERIC

#["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz']
sql="select * from v1.t_gg where quyu='anhui_anqing' limit 100  "

conp=["postgres","since2015","192.168.4.188","base","v1"]

krr,krrdict=initwords_ol()
def df2df(df):
    mdata=[]
    for i in range(len(df)):
        page=df.at[i,'page']

        #data=extpage_ol(page)
        data=final(page,krr,krrdict)

        if data is None:data={}
        data['href']=df.at[i,'href']
        data['html_key']=df.at[i,'html_key']
        data['ggtype']=df.at[i,'ggtype']
        #kzj  zhongbiaojia

        if 'kzj' in data.keys():
            data['kzj']=extprice(data['kzj'])

        if 'zhongbiaojia' in data.keys():
            data['zhongbiaojia']=extprice(data['zhongbiaojia'])

        #name 清洗算法

        # if 'xmmc' not in data.keys():
        #     xmmc=df.at[i,'name']
        #     xmmc=extname(xmmc)

        #     data['xmmc']=xmmc

        #时间清洗算法
        gg_fabutime=exttime(page)
        if gg_fabutime is None:
            gg_fabutime=df.at[i,'ggstart_time']
        data['gg_fabutime']=gg_fabutime
        for w in ["zhongbiaoren","zbdl","zhaobiaoren"]:
            if w in data.keys():data[w]=reclear_qyname(w)
        mdata.append(data)
    
    df=pd.DataFrame(data=mdata,columns=["xmmc","gg_fabutime",'ggtype','xmbh',"zhaobiaoren",'zbdl','zbfs',"kzj",'zhongbiaoren','zhongbiaojia','xmjl','xmdz','html_key','href']
        )
    return df

bg=time.time()
datadict={"xmmc":TEXT(),"gg_fabutime":TIMESTAMP(),"ggtype":TEXT(),"ggtype":TEXT(),"xmbh":TEXT(),"zhaobiaoren":TEXT(),"zbdl":TEXT(),"zbfs":TEXT()
       ,"kzj":NUMERIC(),"zhongbiaoren":TEXT(),"zhongbiaojia":NUMERIC(),"xmjl":TEXT(),"xmdz":TEXT(),"html_key":BIGINT(),"href":TEXT()}
pg2pg(sql,'anhui_anqing_bd',conp,conp,chunksize=1000,f=df2df,datadict=datadict)

ed=time.time()

cost=int(ed-bg)
print("共耗时%d 秒"%cost)
