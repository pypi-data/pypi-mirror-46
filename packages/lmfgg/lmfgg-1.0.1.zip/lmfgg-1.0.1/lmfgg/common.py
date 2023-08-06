from bs4 import BeautifulSoup
def to_arr(page):
    cm=["：","："]
    if page is None:return []
    soup=BeautifulSoup(page,'html.parser')
    tmp=soup.find('style')
    if tmp is not  None:tmp.clear()
    tmp=soup.find('script')
    if tmp is not  None:tmp.clear()
    arr=[]
    for w in soup.strings:
            w=w.strip()
            if w=='':continue
            if len(w)==1 and w not in cm:continue
            arr.append(w)
    return arr 