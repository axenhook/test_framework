import simplejson
import sys
import os
import re

# 封装脚本
def exec_one_json(name):
    s = '.'+name
    l = open(s,"w+")
    f = open(name,"r")
    result = []
    flag = 0
    for line in f:
       a= line
       b = a.strip('\r\n')
       c = b.split("//")[0]
       if c.startswith('/*'):
           flag = 1
           continue
       if flag == 1:
           if c.startswith('*/'):
               flag = 0
           continue
       result.append(c)
       print(c,file=l)
    f.close()
    l.close()
    
    with open(s, 'r', encoding='UTF-8') as f:
        try:
            dic = simplejson.load(f)
            k3 = dic.keys()
        except:
            os.remove(s)
    k1 = dic.keys()
    k2 = list(k1)
    k = len(k2)
    e1 = 0
    e2 = 0
    for i in k2:
        q = dic.get(i)
        for x in q:
            command = ('%s  | egrep -w %s | head -1' %(i,x))
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
    os.remove(s)

# 判断传入的路径是否为目录
def main():
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
                                print(" json文件格式出现错误")
        
        elif os.path.isfile(sys.argv[1]):  # 查找为文件则直接处理
            exec_one_json(sys.argv[1])
        else:
            print("There is no such file or directory")

if __name__ == '__main__':
    main()