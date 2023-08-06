from bs4 import BeautifulSoup
def get_ps(page):
    data=[]
    soup=BeautifulSoup(page,'lxml')
    tables=soup.find_all('table')
    if tables !=[]:
        for tb in tables:
            tbtmp=tb.find('table')
            if tbtmp is  None:
                tb.extract()
    return str(soup)

def clear_tag(page,tagname):
    soup=BeautifulSoup(page,'lxml')
    spans=soup.find_all(tagname)

    for span in spans:
        # contents=span.contents
        # if len(contents)>1:continue
        # if  str(type(contents[0]))=="<class 'bs4.element.NavigableString'>":
        #     span.replace_with()
            span.unwrap()
    return str(soup)




def get_pure_ps(page):
    page=clear_tag('span')
    page=clear_tag('font')
    page=clear_tag('u')
    page=get_ps(page)
    return page
