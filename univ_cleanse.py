# -*- coding: utf-8 -*-
#内含中文字符的文件在引用时需在开头加上如上字符
import pandas as pd
import numpy as np
import re
from helper import seg, tag

def qualifier(word):
    if "大学" not in word and "学院" not in word:
        return False
    elif "医院" in word:
        return False
    elif len(word) <= 3:
        return False
    elif len(re.findall("[^\u4e00-\u9fa5]", word)) >= len(word)-3:
        return False
    return True

def univ_only(word):
    inde1 = word.find("大学")
    inde2 = word.find("学院")
    if inde1 == -1:
        indeh = inde2
    else:
        indeh = inde1
    raw = word[:indeh+2].replace("老师", "").replace("学生", "")
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
    string = "".join(list(re.findall("[\u4e00-\u9fa5]", string)))
    if string == "大学" and ind > 0:
        string = "".join(lst_s[ind-1:])
        string = "".join(list(re.findall("[\u4e00-\u9fa5]", string)))
    return string

def univ_c(word):
    if qualifier(word) is False:
        return word
    else:
        return univ_only(word)

if __name__=="__main__":
    '''
    df = pd.read_csv("master_unique.csv")
    df["result"] = df["customer_name"].apply(univ_c)
    df.to_csv("ttt.csv", encoding = "utf-8-sig")
    '''
    a = "鲁东大学 "
    print(univ_c(a))