import pandas as pd
import hos_cleanse as hc
import univ_cleanse as uc
import cleanse as c
import re
from helper import seg, tag

'''#ͬʱ����ͬһ���ݽṹ��Ķ�������
def test(content, key1, key2):
    if "ҽԺ" in str(content[key1]) and "ҽԺ" in str(content[key1]):
        return str(content[key1])+str(content[key2])
    return "nooooooooo"
'''
def three_in_one(word):
    word = str(word)
    new = hc.hos_c(word)
    if hc.qualifier(word) is True:
        return new
    new = uc.univ_c(word)
    if uc.qualifier(word) is True:
        return new    
    new = c.cleaning(word, "")
    return new

def fen(word):#�ٴηִ�Ч�����ɲ�̫�ã���Ҫ����Ϊ��������
    word = str(word)
    if len(re.findall("[^\u4e00-\u9fa5]", word)) != len(word) and (" " in word or "-" in word):
        word.replace("-", " ")
        words = word.split(" ")
        string = ""
        for i in words:
            segs = seg.segment(i.replace("����", ""))
            tags = tag.tag(segs)
            if len(tags)==1 and tags[0] == "nr":
                continue
            string += "".join(segs)
        string = "".join(list(re.findall("[A-Za-z0-9\u4e00-\u9fa5]", string)))
        if string == "":
            return word
        return string.replace(" ", "").replace("-", "")
    else:
        return word

#���ز���
if __name__=="__main__":
    df = pd.read_csv("dis_unique.csv", header = None, names = ["customer_name"])
    df["result"] = df["customer_name"].apply(three_in_one)
    df["result"] = df["result"].apply(fen)
    #df["test"] = df.apply(test, axis = 1, args = ("customer_name", "result"))
    df.to_csv("ttt.csv", encoding = "utf-8-sig")