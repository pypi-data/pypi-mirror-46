
from lmfgg.common import getpage
from bs4 import BeautifulSoup 
from lmfgg.table.common import fm 


# url="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20180112/bee00e3f-473d-4b8d-94b3-07852eb2e23b.html"

# page=getpage(url,'anhui_anqing')
#对一个table进行清洗，去除无用trtd 

def clear(page):
    soup=BeautifulSoup(page,'html.parser')
    table=soup.find('table')
    trs=table.find_all('tr')
    for tr in trs:
        if tr.text.strip()=='':
            tr.extract()
        tds=tr.find_all('td')
        for td in tds:
            if td.text.strip()=='':
                td.extract()
    page=str(table)
    return page 

#从page中提取无嵌套的table 返回tabled额数组
def get_tb(page):
    data=[]
    soup=BeautifulSoup(page,'html.parser')
    tables=soup.find_all('table')
    if len(tables)==0:return None

    if len(tables)==1:
        data=[str(tables[0])]
        return data

    for tb in tables:
        tbtmp=tb.find('table')
        if tbtmp is  None:continue
        if len(tbtmp.text.strip())<10:continue
        data.append(str(tbtmp))
    if data==[]:return None
    return data