import ctypes
import os
import sys
from sys import platform

def get_path_of_hosts():
    if platform == "linux" or platform == "linux2":
        return "/etc/hosts"
    elif platform == "win32":
        return "C:\Windows\System32\drivers\etc\hosts"


def get_list(*lst):
    new_lst=[]
    for i in lst:
        try:
            begin=str.index(i,"//",0)+2
        except:
            begin = 0
        try:
            end=str.index(i,"/",begin)
        except:
            end=-1
        new_lst.append(i[begin:end])
    return new_lst

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_sites(*lst):
    sites = get_list(*lst)
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
