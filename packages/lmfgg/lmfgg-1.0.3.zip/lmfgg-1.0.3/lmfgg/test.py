from lmf.dbv2 import db_write ,db_query
import sys 
from lmfgg.table.common import tb1,tb2
from bs4 import BeautifulSoup

def wp(page):
    with open(sys.path[0]+"\\test.html",'w',encoding='utf8') as f:
        f.write(page)
krr=['标段编号', '项目经理', '项目名称', '工期', '中标单位', '中标价',"标段包名称","标段包编号","中标单位"
,'异议、投诉受理', '第二中标候选人', '投标费率', '开标地点', '资质等级', '项目编号', '工期', '奖项', '资格等级', '业绩'
, '最高投标费率', '开标时间', '招标方式', '第三中标候选人', '工程名称', '招标人', '公示时间', '第一中标候选人', '项目总监'
,"工程名称","工期天","建造师","单位名称"
]
krr=list(set(krr))
conp=["postgres","since2015",'192.168.4.188','base','v1']
href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20190517/4b7346e7-cab7-4118-a5bf-fc579bbf379f.html"
href="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20190424/af7df6ec-230f-42d9-8909-9d2c549d39d7.html"
sql1="select * from v1.t_gg_anhui_anqing  where  href='%s' "%href
#sql1="select * from v1.t_gg_anhui_anqing  where ggtype='中标公告' limit 10"

df1=db_query(sql1,dbtype="postgresql",conp=conp)
page=df1.at[0,'page']
wp(page)

soup=BeautifulSoup(page,'html.parser')
table=soup.find('table')