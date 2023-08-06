
from lmfgg.common import getpage
from bs4 import BeautifulSoup 
from lmfgg.table.common import fm 


# url="http://aqggzy.anqing.gov.cn/jyxx/012001/012001004/20180112/bee00e3f-473d-4b8d-94b3-07852eb2e23b.html"

# page=getpage(url,'anhui_anqing')
#对一个table进行清洗，去除无用trtd 

#传入clear的必须为table
def clear(page):

    soup=BeautifulSoup(page,'html5lib')
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
    page=page.replace("<th>",'<td>').replace("</th>","</td>")
    return page 

#从page中提取无嵌套的table 返回tabled额数组
def get_tb(page):
    if page is None:return None
    data=[]
    soup=BeautifulSoup(page,'html5lib')
    tables=soup.find_all('table')
    if len(tables)==0:return None

    if len(tables)==1:
        data=[str(tables[0])]
        return data

    for tb in tables:
        tbtmp=tb.find('table')
        if tbtmp is  None:
            data.append(str(tb))
            continue
        if len(tbtmp.text.strip())<10:continue
        data.append(str(tbtmp))
    if data==[]:return None
    return data

# def replace_th(page):
#     if page is None:return None 
#     page=page.replace("<th>",'<td>').replace("</th>","</td>")
#     return page



def get_pure_tbs(page):

    tbs=get_tb(page)
    if tbs is None:return None
    tbs=[clear(w)  for w in tbs]

    return tbs 