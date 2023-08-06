from lmfgg.getdata import extpage_ol 

from lmf.dbv2 import db_query

from price import extprice  


sql="select * from t_gg where quyu='anhui_anqing' and href='http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20161101/1844db20-1490-4a09-aca7-440bcd373b9d.html' "

conp=["postgres","since2015","192.168.4.188","base","v1"]

df=db_query(sql,dbtype="postgresql",conp=conp)


page=df.at[0,'page']


data=extpage_ol(page)
