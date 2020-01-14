# -*- coding: utf-8 -*-
#内含中文字符的文件在引用时需在开头加上如上字符
import pandas as pd
import numpy as np
import re
from helper import seg, tag

def qualifier(word):
    if "医院" not in word and "保健院" not in word:
        return False
    elif word.find("医院") == word.find("医院）") or word.find("医院") == word.find("医院 ）"):
        return False
    elif len(word) <= 3:
        return False
    elif len(re.findall("[^\u4e00-\u9fa5]", word)) >= len(word)-3:
        return False
    return True

def hos_only(word):
    indeh = word.find("医院")
    if "医院大学" in word:
        indeh = indeh + 2
    raw = word[:indeh+2]
    index = raw.find("-")
    if index == -1:
        index = raw.find(" ")
    if index != -1 and raw[index-2:index] == "大学":
        raw = raw[:index] + raw[index+1:]
        index = -1
    segs = seg.segment(raw[index+1:])
    tags = tag.tag(segs)
    lst_s = list(segs)
    lst_t = list(tags)
    ind = 0
    for i in range(len(lst_t)):
        if lst_t[i] == "nr":
            ind = i + 1
        else:
            break
    string = "".join(lst_s[ind:])
    string = "".join(list(re.findall("[0-9\u4e00-\u9fa5]", string)))
    return string.strip("-")

def hos_c(word):
    if qualifier(word) is False:
        return word
    else:
        return hos_only(word)

if __name__=="__main__":
    #df = pd.read_csv("master_unique.csv")
    #df["result"] = df["customer_name"].apply(hos_c)
    #df.to_csv("ttt.csv", encoding = "utf-8-sig")
    a = "北京大学第三医院"
    print(hos_c(a))
    