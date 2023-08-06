
from lmfgg.txt import ismat
import json
from lmfgg.table.tbdata import ext 
from lmfgg.ps.common import ps
from lmfgg.common import getpage 
import os 
import re
import copy 
from lmf.dbv2 import db_query 
__krr=None
__datadict=None

def get_name(data,name_list):
    for w in data.keys():
        if ismat(w,name_list):
            v=data[w]
            if isinstance(v,list):
                result=v[0]
            else:
                result=v
            return result
    return None

def getsist(data,arrdict):
    result={}
    it=["xmmc","kzj","zhaobiaoren",'zbdl','zbfs','xmbh','zhongbiaoren','zhongbiaojia','xmjl','xmdz']
    for w in it:
        if w not in arrdict.keys():continue
        arr=arrdict[w]
        v=get_name(data,arr)
        if v is not None:result[w]=v
    return result

def getfinal(psdata,tbdata,arrdict):
    psdict=getsist(psdata,arrdict)
    tbdict=getsist(tbdata,arrdict)
    psdict.update(tbdict)
    return psdict

def final(page,krr,arrdict):
    psdata=ps(page,krr)
    tbdata=ext(page,krr)

    data=getfinal(psdata,tbdata,arrdict)
    return data


#def api(page)
def initwords():

    print("初始化字典")
    global __krr
    global __datadict
    with open(os.path.join(os.path.dirname(__file__),'words.txt'),encoding='utf8') as f:
        lines=f.readlines()
    arr=[list( filter(lambda x:x.strip()!='',re.split('\s+',w))) for w in lines]

    krr=copy.deepcopy([w[0] for w in arr])

    result={"xmmc":[],"zhaobiaoren":[],"zhongbiaoren":[],"kzj":[],"zhongbiaojia":[]
    ,"xmjl":[],"xmbh":[],"zbdl":[],"zbfs":[],"xmdz":[],"others":[]
    }

    for w in arr:
        #flag=0
        for k in result.keys():
                    if len(w)<=1:continue
                    if w[1]==k :
                        result[k].append(w[0])
                        #flag=1
        #if flag==0:result["others"].append(w[0])
    datadict=copy.deepcopy(result)
    return krr,datadict


__krr,__datadict=initwords()
def extpage(page):
    data=final(page,__krr,__datadict)

    return data 


def extpage_ol(page):
    df=db_query("select name,tag from v1.words",dbtype="postgresql",conp=["postgres","since2015","192.168.4.188","base","v1"])
    krr=df['name'].values.tolist()
    result={"xmmc":[],"zhaobiaoren":[],"zhongbiaoren":[],"kzj":[],"zhongbiaojia":[]
    ,"xmjl":[],"xmbh":[],"zbdl":[],"zbfs":[],"xmdz":[],"others":[]
    }
    a=df.to_dict(orient='records')
    for w in a:
        flag=0
        for k in result.keys():
                    if w['tag']==k:
                        result[k].append(w['name'])
                        flag=1
        if flag==0:result["others"].append(w['name'])
    datadict=result
    data=final(page,krr,datadict)

    return data 



# arr=['成交人','成交金额','成交价','成交供应商名称','成交供应商','成交单位','采购人名称','采购人','采购方式','开标地点','奖项','资质等级','资格等级','工期天','业绩','单位名称','第二中标候选人'
# ,'公示时间'
# ,'流标原因','第三中标候选人','开标时间','最高投标费率','工期','异议、投诉受理','建造师','投标费率','社会保险号','采购单位','采购代理机构','公示期','标段编号','标段包名称','标段包编号','建筑面积'
# ,'设计负责人','标的名称','中标候选人排名','公示期限','公告发布日期',"'资格证书编号'",'联系人','设备名称','发布时间','抽取日期','推荐排名第二单位','推荐排名第一单位','第一名','第二名','第三名'
# ,'最高投标限价','中标金额','中标价','中标单位','第一成交候选人','招标人名称','招标人','招标方式','招标单位','第二成交候选人','招标代理','招标代理机构','预中标候选人','预算金额','业主单位'
# ,'项目总监','项目所在区域','项目名称','项目类别','项目经理','项目管理人员','项目负责人','项目地点','项目编号','投标总报价','投标人业绩','工程名称','标段工程名称','标段内容','编号'
# ,'采购名称','采购项目名称','第三成交候选人','中标金额元','中标合同价元','合同价','投标报价','招标控制价','第一中标候选人','中标成交金额','中标成交供应商','中标供应商','中标人','招标编号'
# ,'地址','中标候选人']
# arrdict={
#   "xmmc": [
#     "标段包名称",
#     "标的名称",
#     "项目名称",
#     "工程名称",
#     "标段工程名称",
#     "标段内容",
#     "采购名称",
#     "采购项目名称"
#   ],
#   "zhaobiaoren": [
#     "采购单位",
#     "招标人名称",
#     "招标人",
#     "招标单位"
#   ],
#   "zhongbiaoren": [
#     "成交人",
#     "成交供应商名称",
#     "成交供应商",
#     "成交单位",
#     "采购人名称",
#     "采购人",
#     "推荐排名第一单位",
#     "第一名",
#     "中标单位",
#     "第一成交候选人",
#     "预中标候选人",
#     "第一中标候选人",
#     "中标成交供应商",
#     "中标供应商",
#     "中标人"
#   ],
#   "kzj": [
#     "最高投标限价",
#     "预算金额",
#     "招标\r\n\r\n控制价"
#   ],
#   "zhongbiaojia": [
#     "成交金额",
#     "成交价",
#     "中标金额",
#     "中标价",
#     "投标总报价",
#     "中标金额元",
#     "中标合同价元",
#     "合同价",
#     "投标报价",
#     "中标成交金额"
#   ],
#   "xmjl": [
#     "项目总监",
#     "项目经理",
#     "项目管理人员",
#     "项目负责人"
#   ],
#   "xmbh": [
#     "标段编号",
#     "标段包编号",
#     "项目编号",
#     "编号",
#     "招标编号"
#   ],
#   "zbdl": [
#     "采购代理机构",
#     "招标代理",
#     "招标代理机构"
#   ],
#   "zbfs": [
#     "采购方式",
#     "招标方式"
#   ],
#   "xmdz": [
#     "项目所在区域",
#     "项目地点",
#     "地址"
#   ]
# }


# data="""
# {"招 标 人": "岳西县农业综合开发办公室", "工程名称": "岳西县国家农业综合开发2017年土地治理项目土建工程施工4标", "招标方式": "公开招标", "招标代理机构": "安徽皖国建设项目管理有限公司", "开标时间": "2017年10月31日10时00分", "中标候选人": "第一名", "公示时间": "（2017年11月01日至2017年11月07日17：00时）"}
# """


