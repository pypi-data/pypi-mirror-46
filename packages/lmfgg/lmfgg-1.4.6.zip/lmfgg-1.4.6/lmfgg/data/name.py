import re 

__krr1=["中标公示$",'招标公告$',"变更通知$","流标公示$","修改说明$","投标邀请公告$","招标失败公告$","流标公告$"]

def extname(name):

    for w in __krr1:
            name=re.sub(w,'',name)
    return name