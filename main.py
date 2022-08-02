import ctypes
import os
import sys
from sys import platform
import argparse


# get the path of the 'hosts' file
def get_path_of_hosts():
    if platform == "linux" or platform == "linux2" or platform == "MacOs":
        return "/etc/hosts"
    elif platform == "win32":
        return "C:\Windows\System32\drivers\etc\hosts"


# get the short name of the site (without "https://" and the final path)
def split_name(full):
    try:
        begin = str.index(full, "//", 0) + 2
    except:
        begin = 0
    try:
        end = str.index(full, "/", begin)
    except:
        end = len(full)
    return full[begin:end]


# check if the user can change the hosts file
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# block all the given sites in the list,of course if the certain site is not already block
def block_sites(lst):
    #contains the short names
    sites = []
    for i in lst:
        sites.append(split_name(i))
    to_add = set(sites).difference(blocked)
    with open(get_path_of_hosts(), 'a') as file:
        for i in to_add:
            file.write(i + '\t')
            blocked.add(i)
            print(i, " is blocked")


# release all the given sites,of course if the certain site is block
def unblock(sites):
    for name in sites:
        # if this site is blocked
        flag = False
        new_text = ""
        name = split_name(name)
        with open(get_path_of_hosts(), 'r') as file:
            text = file.read().split('\n')
        for i in text:
            if i[0:9] == '127.0.0.1':
                if name in i.split('\t'):
                    i = i.replace(name + '\t', '')
                    flag = True
            if len(i) > 1:
                new_text = new_text + '\n' + i
        with open(get_path_of_hosts(), 'w') as file:
            file.write(new_text)
        print("{} is unblocked".format(name) if flag is True else "the site wasn't block")


# get the blocked web sites and make the file ready to get sites
def get_the_blockes():
    blocked = set()
    # find the blocked web-sites
    with open(get_path_of_hosts(), 'r+') as file:
        text = file.read().split('\n')
        for i in text:
            if i[0:9] == '127.0.0.1':
                blocked = blocked.union(i[str.index(i, '\t'):].split('\t'))
        if text[-1][0:9] != '127.0.0.1':
            file.write('\n127.0.0.1\t')
    return blocked


# set the arguments properties
parser = argparse.ArgumentParser()
parser.add_argument('--block', '-b', default=[], help="enter sites to block", nargs='*')
parser.add_argument('--unblock', '-ub', default=[], help="enter sites to unblock", nargs='*')
args = parser.parse_args()

if (not is_admin()):
    exit('you are not admin')
# the blocked sites
blocked = get_the_blockes()

if len(args.block) > 0:
    block_sites(args.block)
if len(args.unblock) > 0:
    unblock(args.unblock)

# block_sites(["https://www.jdn.co.il","https://wwww.ggg.co.il"])
# unblock(["https://www.jdn.co.il"])
