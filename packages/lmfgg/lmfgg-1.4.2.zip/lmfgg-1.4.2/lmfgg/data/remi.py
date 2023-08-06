from lmfgg.getdata import extpage_ol 

from lmf.dbv2 import db_query

from price import extprice

from name import extname  
import pandas as pd

#["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz']
sql="select * from t_gg where quyu='anhui_anqing' order by random() limit 10 "

conp=["postgres","since2015","192.168.4.188","base","v1"]

df=db_query(sql,dbtype="postgresql",conp=conp)

mdata=[]
for i in range(len(df)):
    page=df.at[i,'page']

    data=extpage_ol(page)
    if data is None:data={}
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

df=pd.DataFrame(data=mdata,columns=["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz'])




