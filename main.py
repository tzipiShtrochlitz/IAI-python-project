import ctypes
import os
import sys
from sys import platform


def get_path_of_hosts():
    if platform == "linux" or platform == "linux2":
        return "/etc/hosts"
    elif platform == "win32":
        return "C:\Windows\System32\drivers\etc\hosts"

def split_name(full):
    try:
        begin=str.index(full,"//",0)+2
    except:
        begin = 0
    try:
        end=str.index(full,"/",begin)
    except:
        end=len(full)
    return full[begin:end]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def block_sites(lst):
    sites = []
    for i in lst:
        sites.append(split_name(i))
    to_add=set(sites).difference(blocked)
    path = get_path_of_hosts()
    try:
        if(not is_admin()):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        with open(path,'a') as file:
            for i in to_add:
                file.write(i+'\t')
        for i in to_add:
            blocked.add(i)
            print(i," is blocked")
    except:
        print("was an error")

def unblock(name):
    new_text=""
    name=split_name(name)
    with open(get_path_of_hosts(), 'r') as file:
        text = file.read().split('\n')
    for i in text:
        if i[0:9]=='127.0.0.1':
            if name in i.split('\t'):
                i=i.replace(name+'\t','')
        if len(i)>1:
            new_text=new_text+'\n'+i
    with open(get_path_of_hosts(),'w') as file:
        file.write(new_text)
    print(name," is unblocked")


#get the blocked web sites
blocked=set()
#if there are blocked web-sites already
flag=False
#find the blocked web-sites
with open(get_path_of_hosts(),'r+') as file:
    text=file.read().split('\n')
    for i in text:
        if i[0:9] == '127.0.0.1':
            blocked=blocked.union(set(i[str.index(i,'\t'):].split('\t')))
            flag=True
    if flag==False or text[-1][0:9]!='127.0.0.1':
        file.write('\n127.0.0.1\t')

block_sites(["https://www.meuhedet.co.il/","https://www.hhh.co.il"])
unblock("https://www.meuhedet.co.il/")