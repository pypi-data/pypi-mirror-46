from lmfgg.ps.pspre import get_pure_ps

from lmfgg.ps.common import ps 
from lmfgg.common import getpage

def psext(page,krr):
    page=get_pure_ps(page)
    data= ps(page,krr)
    return data