from bs4 import BeautifulSoup
def get_ps(page):
    data=[]
    soup=BeautifulSoup(page,'lxmlr')
    tables=soup.find_all('table')
    if tables !=[]:
        for tb in tables:
            tbtmp=tb.find('table')
            if tbtmp is  None:
                tb.extract()
    return str(soup)



def get_pure_ps(page):

    page=get_ps(page)
    return page
