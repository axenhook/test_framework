import simplejson
import sys
import os
import re

# 封装脚本
def exec_one_json(name):
    with open(name, 'r', encoding='UTF-8') as f:
        dic = simplejson.load(f)
    k1 = dic.keys()
    k2 = list(k1)
    k = len(k2)
    e1 = 0
    e2 = 0
    for i in k2:
        q = dic.get(i)
        command = ('%s' %(i))
        r2 = os.popen(command)
        info2 = r2.readlines()
        l = open('log.txt','w+')
        for linee in info2:
              line2 = linee.strip('\r\n')
              print(line2,file=l)
        l.close() 
        l2 = 'cat log.txt'
        for x in q:
            command = ('%s  | egrep -w %s | head -1' %(l2,x))
            r = os.popen(command)
            info = r.readlines()
            for line in info:
                line1 = line.strip('\r\n')
                # print(line1)

                zhi = q.get(x)
                if zhi in line:
                    e1 += 1
                else:
                    e2 += 1
                    print(i+"\x20---\x20failed")
                    print(40*'-')

    e3 = e1+e2
    print("total:%s, \x20\x20 successful: %s,\x20\x20 failed: %s" % (e3, e1, e2))
    os.remove('log.txt')

# 判断传入的路径是否为目录
if len(sys.argv) <=1:
    print("usage:\x20"+sys.argv[0]+"\x20file_name/dir_name")
    exit
else:
    if os.path.isdir(sys.argv[1]):  # 查找目录下以.json文件结尾的文件
        for root, dirs, files in os.walk(sys.argv[1]):
            for file in files:
                if file.endswith(".json"):
                    json = os.path.join(root, file)
                    if not os.path.getsize(json):
                        pass
                    else:
                        try:
                            print('\n')
                            print(json)
                            print(40*'-')
                            exec_one_json(json)
                        except:
                            print("json file format error!")
    
    elif os.path.isfile(sys.argv[1]):  # 查找为文件则直接处理
        exec_one_json(sys.argv[1])
    else:
        print("There is no such file or directory")
