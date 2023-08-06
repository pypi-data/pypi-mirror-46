from lmfgg.getdata import extpage_ol 

from lmf.dbv2 import db_query

from price import extprice

from name import extname  
import pandas as pd
from lmf.bigdata import pg2pg

#["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz']
sql="select * from v1.t_gg where quyu='anhui_anqing' order by random() limit 1000 "

conp=["postgres","since2015","192.168.4.188","base","v1"]



def df2df(df):
    mdata=[]
    for i in range(len(df)):
        page=df.at[i,'page']

        data=extpage_ol(page)

        if data is None:data={}
        data['href']=df.at[i,'href']
        data['html_key']=df.at[i,'html_key']
        #kzj  zhongbiaojia

        if 'kzj' in data.keys():
            data['kzj']=extprice(data['kzj'])

        if 'zhongbiaojia' in data.keys():
            data['zhongbiaojia']=extprice(data['zhongbiaojia'])

        #name 清洗算法

        if 'xmmc' not in data.keys():
            xmmc=df.at[i,'name']
            xmmc=extname(xmmc)
            data['xmmc']=xmmc
        mdata.append(data)

    df=pd.DataFrame(data=mdata,columns=["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz','html_key','href'])



pg2pg(sql,'anhui_anqing_bd',conp,conp,chunksize=100,f=df2df)

