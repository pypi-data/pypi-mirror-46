from bs4 import BeautifulSoup
def get_ps(page):
    data=[]
    soup=BeautifulSoup(page,'html.parser')
    tables=soup.find_all('table')
    if tables !=[]:
        for tb in tables:
            tbtmp=tb.find('table')
            if tbtmp is  None:
                tb.extract()
    return str(soup)
