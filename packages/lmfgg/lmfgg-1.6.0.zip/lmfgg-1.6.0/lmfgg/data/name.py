import re 

__krr1=["中标公示$",'招标公告$',"变更通知$","流标公示$","修改说明$","投标邀请公告$","招标失败公告$","流标公告$","中标结果公示$"
,"补充说明$","询价公告","暂停的公告","成交公示"
]

def extname(name):

    for w in __krr1:
            name1=re.sub(w,'',name)
    if name1==name:
        return None
    else:
        return name1
    



def reclear_qyname(qyname):
    if qyname is None:return None
    a=re.findall("^[\u4e00-\u9fa5（）\(\)]*公司",qyname.strip())
    if a!=[]:
        return a[0]
    else:
        return None


def reclear_xmjl(name):
    if name is None:return None 
    a=re.findall("^[\u4e00-\u9fa5]*",name.strip())
    if a!=[]:
        return a[0]
    else:
        return name
