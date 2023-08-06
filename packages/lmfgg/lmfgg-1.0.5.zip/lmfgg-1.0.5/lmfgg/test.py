from lmf.dbv2 import db_write ,db_query
import sys 
from lmfgg.table.common import tb1,tb2
from bs4 import BeautifulSoup
from lmfgg.ps.common import ps,getwordfdb
def wp(page):
    with open(sys.path[0]+"\\test.html",'w',encoding='utf8') as f:
        f.write(page)
krr=getwordfdb()

arr=['招标编号','项目名称','建设地点','项目概算','招标类别',"联系人","招标代理","联合体牵头人"]

krr.extend(arr)

conp=["postgres","since2015",'192.168.4.188','base','v1']
href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20190517/4b7346e7-cab7-4118-a5bf-fc579bbf379f.html"
href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20190424/af7df6ec-230f-42d9-8909-9d2c549d39d7.html"
#sql1="select * from v1.t_gg_anhui_anqing  where  href='%s' "%href
sql1="select * from v1.anhui_anqing where ggtype='中标公告'   limit 100"

df1=db_query(sql1,dbtype="postgresql",conp=conp)
# page=df1.at[0,'page']
# wp(page)

# soup=BeautifulSoup(page,'html.parser')
# table=soup.find('table')


df1['data']=df1['ps'].map(lambda x:ps(x,krr))

for w in df1['data']:print(w)

for w in df1['href'][:10]:print(w)
