# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:33:28 2020

@author: Hao Kong
"""

import socket               # 导入 socket 模块
import os
import sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         # 创建 socket 对象
host = '<address>'#socket.gethostname() # 获取本地主机名
port = <端口号>#50001             # 设置端口号
 
s.connect((host, port))
#s.send('<用户名>'.encode()) #向远程服务器发送用户名
s.send(sys.argv[1].encode())

print( s.recv(1024).decode('utf-8'))
s.send('ready'.encode())
cmd = s.recv(1024).decode('utf-8')
print(cmd)
while(cmd == 'ready'):
    print('服务端就位')
    
    filesize = s.recv(1024).decode('utf-8')
    s.send(filesize.encode())
    filesize = int(filesize)
    filename = s.recv(1024).decode('utf-8')
    s.send(filename.encode())
    print('开始下载',filename,'大小',filesize)
    recvLen = 0
    with open(filename,'wb') as ob:
        while recvLen < filesize:
            sys.stdout.write("\r"+str(round(recvLen/filesize,2)*100)[:4]+'%  ')
            sys.stdout.flush()
            temp = s.recv(1024)
#            print(temp.decode('utf-8'))
            recvLen += len(temp)
            ob.write(temp)
    if int(os.path.getsize(filename)) == int(filesize):
        s.send('1'.encode())
    else:
        s.send('0'.encode())
    s.send('ready'.encode())
    cmd = s.recv(5).decode('utf-8')
s.close()
