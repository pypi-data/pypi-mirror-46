from lmfgg.table.tbpre import get_pure_tbs 

from lmfgg.table.common import tb1,tb2,tb3 ,calsep

from lmfgg.txt import ismat

def ext1(page):

    tbs=get_pure_tbs(page)
    if tbs is None:return None
    tb=tbs[0]
    data=tb1(tb)
    return data

def ext2(page):

    tbs=get_pure_tbs(page)
    if tbs is None:return None
    tb=tbs[0]
    data=tb2(tb)
    return data

def ext3(page,krr):

    tbs=get_pure_tbs(page)
    if tbs is None:return None
    tb=tbs[0]
    data=tb3(tb,krr)
    return data


def ext(page,krr):
    v=calsep(page,krr)
    if v==0:
        data=ext1(page)
    elif v==1:
        data=ext2(page)
    else:
        data=ext3(page,krr)
    return data


def name(data,namerr):
    
    for w in data.keys():
        if ismat(w,namerr):return data[w]
    return None

