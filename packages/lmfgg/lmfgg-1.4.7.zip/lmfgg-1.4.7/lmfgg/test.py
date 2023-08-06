from lmf.dbv2 import db_write ,db_query
import sys 
from lmfgg.table.common import tb1,tb2,fm
from lmfgg.txt import ismat
from bs4 import BeautifulSoup
from lmfgg.ps.common import ps,getwordfdb
from lmfgg.table import ext1,ext2,ext3
from lmfgg.common import getpage 

from lmfgg.getdata import extpage_ol

page=getpage("http://aqggzy.anqing.gov.cn/jyxx/012001/012001003/20161017/de5862d2-30b2-42ea-992e-e953cf47d359.html","anhui_anqing")


data=extpage_ol(page)


# df1['data']=df1['ps'].map(lambda x:ps(x,krr))

# for w in df1['data']:print(w)

# for w in df1['href'][:10]:print(w)
