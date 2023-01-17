import json
import numpy as np

works=np.load('works.npy',allow_pickle=True)
authors=np.load('authors.npy',allow_pickle=True)

def search_work(search_text):
    result=[]
    i=0
    for work in works:
        if (search_text in work["Content"]) | (search_text in work["Title"]):
            result.append(work)
            i=i+1
        if i>=799:
            break
    return result

def search_author(search_text):
    result1=[]
    result2=[]
    i=0
    for author in authors:
        if search_text in author["Name"]:
            result1.append(author)
            i=i+1
        if i>=799:
            break
    i=0
    for work in works:
        if (search_text in work["Author"]):
            result2.append(work)
            i=i+1
        if i>=799:
            break
    return result1,result2
