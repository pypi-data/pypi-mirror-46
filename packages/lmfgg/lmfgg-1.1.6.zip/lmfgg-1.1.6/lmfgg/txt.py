from bs4 import BeautifulSoup



from lmfgg.common import to_arr
import re
import Levenshtein

def ismat(word,exm):

    word=re.sub("[^\u4E00-\u9FA50-9]",'',word)
    for w in exm:
        if Levenshtein.ratio(w,word)>=0.85:
            return True 
    return False

def fismat(exm,arr,ng=3):
    k=ng
    for i in range(len(arr)):
        for j in range(k):
            word=''.join(arr[i:i+j+1])

            if ismat(word,exm):
                #print(word)
                return 1
    return 0


def cismat(hwd,arr):
    count=0
    for wd in hwd:
        count+=fismat(wd,arr)
    return count






