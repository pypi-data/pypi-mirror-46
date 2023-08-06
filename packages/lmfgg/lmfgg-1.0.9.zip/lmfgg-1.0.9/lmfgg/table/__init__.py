from lmfgg.table.tbpre import get_tb,clear 

from lmfgg.table.common import tb1,tb2,tb3 

def ext1(page):

    tbs=get_tb(page)
    if tbs==[]:return None
    tb=clear(tbs[0])
    data=tb1(tb)
    return data

def ext2(page):

    tbs=get_tb(page)
    if tbs==[]:return None
    tb=clear(tbs[0])
    data=tb2(tb)
    return data

def ext3(page,krr):

    tbs=get_tb(page)
    if tbs==[]:return None
    tb=clear(tbs[0])
    data=tb3(tb,krr)
    return data