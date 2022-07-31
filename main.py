from source import *

#get the blocked web sites
blocked=set()
#if there are blocked web-sites already
flag=False
#find the blocked web-sites
with open(get_path_of_hosts(),'r+') as file:
    for i in file.read().split('\n'):
        if i[0:9] == '127.0.0.1':
            blocked=set(i[str.index(i,'\t'):].split('\t'))
            flag=True
    if flag==False:
        file.write('\n127.0.0.1\t')

add_sites("https://www.meuhedet.co.il/","https://www.hhh.co.il")