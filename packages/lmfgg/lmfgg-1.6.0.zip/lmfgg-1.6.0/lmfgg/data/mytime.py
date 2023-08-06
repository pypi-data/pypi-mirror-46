#coding=utf-8
import re
from lmfgg.common import getpage
from bs4 import BeautifulSoup


def exttime(page):

    soup=BeautifulSoup(page,'lxml')
    txt=soup.text
    parterns=[
    '信息时间.{,3}(20[0-1][0-9])[\/\-\.年]([0-9]{1,2})[\/\-\.月]([0-9]{1,2})', # 例子
    '发稿时间.{,3}(20[0-1][0-9])[\/\-\.年]([0-9]{1,2})[\/\-\.月]([0-9]{1,2})', # 例子
    '信息发布时间.{,3}(20[0-1][0-9])[\/\-\.年]([0-9]{1,2})[\/\-\.月]([0-9]{1,2})',# ggzy江苏南京
    '信息时间.\s(20[0-1][0-9])[\/\-\.年]([0-9]{1,2})[\/\-\.月]([0-9]{1,2})', #ggzy 内蒙古锡林郭勒盟
    '发布日期.{,3}(20[0-1][0-9])[\/\-\.年]([0-9]{1,2})[\/\-\.月]([0-9]{1,2})', #ggzy江苏东台
    ]
    for p in parterns:
        arr=re.findall(p,txt)
        if arr!=[]:
            return '-'.join([ w if len(w)>=2 else '0'+w for w in arr[0]])
    return None

