#coding: utf-8
#内含中文字符的文件在引用时需在开头加上如上字符
'''#可以把cleaning中的kill_paren_all()注释掉
使用方法： cleaning(name, nlp)，输入原名称和分词处理过的名称，对输入值不会有改动，
输出清理过后的名称。
在这里，我简化了（省略了重复的部分，对结果不会有任何改变）之前的分类过程。之所以可以省略，
是因为我们只需要一个解，并不需要知道这个解具体是在哪个萝筐内的。
'''
import re
from helper import seg, tag

def qualifier(word):
    if len(word) <= 3:
        return False
    elif len(re.findall("[^\u4e00-\u9fa5]", word)) >= len(word)-3:
        return False
    return True

def kill_paren(name, mode):
    if mode == "(":
        index_1=name.find("(")
        if index_1==-1:
            index_1=name.find("（")
        index_2=name.find(")")
        if index_2==-1:
            index_2=name.find("）")
        if index_1 != -1:
            if index_2 != -1:
                if index_2 < index_1:
                    return name[index_2+1:index_1]
                return name[:index_1] + name[index_2 +1:]
            else:
                return name[:index_1]
    if mode == ")":
        index_1 = name.find(")")
        return name[index_1 +1:]
    elif mode == "【":
        index_1=name.find("【")
        index_2=name.find("】")
        if index_1 != -1:
            if index_2 != -1:
                return name[:index_1] + name[index_2 +1:]
            else:
                return name[:index_1]
    elif mode == "《":
        index_1=name.find("《")
        index_2=name.find("》")
        if index_1 != -1:
            if index_2 != -1:
                return name[:index_1] + name[index_2 +1:]
            else:
                return name[:index_1]
    return name

def kill_paren_all(content):
    while content.find("(")!=-1 or content.find("（")!=-1:
        content = kill_paren(content, "(")
    content = kill_paren(content, "【")
    content = kill_paren(content, "《")
    content = kill_paren(content, ")")
    return content

def kill_tail(name):
    index = 0
    for i, element in enumerate(name):
        if name[i:i+2]=="公司" or name[i:i+2]=="中心" or name[i:i+2]=="学校" or name[i:i+2]=="中学":
            index = i+1
            break
        if i != 0:
            if element=="医" and index==0 and i < 3:
                index = i
            if element=="大" and (index==0 or name[i-1] == "医") and i < 3:
                index = i
            if element=="局" or element=="社" or element=="院" or element=="所" or element=="部":
                if element=="部" and name[i:i+2]=="部队":
                    index = i+1
                    break
                index = i
                break
    if "公司" in  name:
        index = name.find("公司")
        return name[:index+2]
    if "实验室" in name and index == 0:
        index = name.find("实验室") + 2
    if index!=0:
        return name[:index+1]
    return name

def kill_name(name):
    raw = name.replace("老师", "").replace("学生", "")
    name = raw
    if name.find("-")==1 or name.find("-")==2 or name.find("-")==3 or name.find("-")==0:
        if name[name.find("-")-1]=="大":
            return name[:name.find("-")]
        else:
            return name[name.find("-")+1:]
    if name.find(".")==1:
        return name[2:]
    if name.find("-")==len(name)-4 or name.find("-")==len(name)-3 or \
       name.find("-")==len(name)-2 or name.find("-")==len(name)-1:
        if name.find("-")!=-1:
            return name[:name.find("-")]
    return name

def extract(name, mode):
    name = name.split()
    for i, element in enumerate(name):
        name[i] = element.split("/")
    for i in name:
        if len(i)==2:
            if i[1]==mode:
                return i[0]

def filtered(name):
    if re.search(r"[A-Za-z-－.、*\s~/]", name)==None:
        print("符合！")
    else:
        print("仍不符合！")

def cleaning(origin):
    if qualifier(origin) is False:
        return origin
    origin = origin.strip().strip("-").strip("#").strip(".").strip("*")
    name = kill_paren_all(origin)
    name = kill_tail(name)
    name = kill_name(name)
    #filtered(name)#这一步可以视需要省略，主要就是检测清理过后的名称是否还包含不合格的字符
    return name.strip("-").strip("经销商").strip()

#本地测试
if __name__=="__main__":
    name = "上海医学检验所有限公司"
    #nlp = ""
    after = cleaning(name)
    print(after)
    print("Cleaning finsihed.")
