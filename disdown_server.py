# -*- coding: utf-8 -*-
import socket,os,re
import json,threading
import gc

class partner:
    def __init__(self,NAME,n):
        self.name = ''
        self.connet = None
        self.addr = None
        self.taskList = []
        self.complete = []
        self.uncomplete = []
        self.processing = ''
        self.maxQueue = 0
        self.name = NAME
        self.maxQueue = n

    def getTasks(self,files):
        if len(self.uncomplete) < self.maxQueue:
            for i in range(self.maxQueue - len(self.uncomplete)):
                if files == []:
                    break
                self.uncomplete.append(files.pop(0))
            return 1
        else:
            print(self.name,'任务队列已满！')
            return 0

    def startTask(self):
        if self.uncomplete == []:
            print(self.name,'等待新任务。。。')
            return ''
        else:
            self.processing = self.uncomplete.pop(0)
            return self.processing

    def completeTask(self,judge):
        if judge:
            print(self.name,'成功完成',self.processing)
            self.complete.append(self.processing)
            self.processing = ''
        else:
            print(self.name,'未完成',self.processing)
            self.uncomplete.append(self.processing)
            self.processing = ''

    def showTasks(self):
        return '\n'.join(self.uncomplete)

    def popTasks(self , n ,files):
        if n < self.maxQueue:
            for i in range(len(self.maxQueue) - n):
                files.append(self.uncomplete.pop(0))
        if n == 0 and self.processing != '':
            files.append(self.processing)

    def stopTask(self):
        self.completeTask(False)

def forEachPar(p,fl,tl,urldict):
    c = p.connect
    while(fl != [] or (p.uncomplete != [] or p.processing != '')):
        print(p.name)
        print(len(p.uncomplete))
        try:
            cmd = c.recv(1024)
        except:
            p.popTasks(0,fl)
            break
        if cmd != 'ready':
            p.popTasks(0,fl)
            break
        c.send('ready')
        f = p.startTask()
        if f == '':
            continue
        print(f)
        c.send(str(os.path.getsize(f)))
        if int(c.recv(1024)) != os.path.getsize(f):
            p.popTasks(0,fl)
            break
        c.send(f)
        if c.recv(1024) != f :
            p.popTasks(0,fl)
            break
        with open(f,'rb') as ob:
            temp = 1
            while temp:
                temp = ob.read(1024*64)
                c.send(temp)
#            del temp
#            gc.collect()
        try:
            callback = c.recv(1)
        except:
            p.popTasks(0,fl)
            break
        if callback == '1':
            p.completeTask(True)
            p.getTasks(flist)
            download(tl,fl,urldict,1,ifshow = True)
            os.popen('rm -rf '+f)
            #print(123)
            #t = threading.Thread( target=download, args=(tl, fl, urldict, 1) )
            #print(311)
        elif callback == '0':
            p.completeTask(False)
        else:
            p.popTasks(0,fl)
            break
    c.close()
   
def download(tlist,flist,urldict,n,ifshow=False,really=True):
    for i in range(n):
        if tlist == []:
            print('所有文件下载完成')
            return

        f = tlist.pop(0)
        url = urldict[f]
        ob = open('./download.sh','r')
        lines = ob.read()
        ob.close()
        lines = re.sub('konghao_text_here',url,lines)
        ob = open('./temp.sh','w')
        ob.write(lines)
        ob.close()
        print('下载：')
        print(f)
        if really:
            if ifshow:
                print(os.popen('./temp.sh').read())
            else:
                os.popen('./temp.sh')
        flist.append(f)

#######################################################################
flistTot = 'download.json'
with open(flistTot,'r') as ob:
    print('下载项目来自: ')
    print(flistTot)
    tlist = json.load(ob)
urldict = {}
for t in tlist:
    f = t.split('/')[-1]
    urldict[f] = t
tlist = list(urldict.keys())
flist = []
download(tlist,flist,urldict,20,ifshow=True)#,really = False)

print('正在运行下载器服务端：')
host = socket.gethostname()
print('本地计算机名：')
print(host)
port = <端口号>#50001
print('监听端口：')
print(port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)
s.settimeout(3600)
partners = {}
quelen = 5
threads = {}
while tlist!=[]:
    c,addr = s.accept()
    #print(c.recv(1024))
    name = c.recv(1024)
    if name not in partners:
        partners[name] = partner(name,quelen)
    partners[name].addr = addr
    partners[name].connect = c
    partners[name].getTasks(flist)
    print(name)
    print(addr)
    line = '谢谢您参与数据下载，'+name+'同学！'
    c.send(line)

    t = threading.Thread( target=forEachPar, args=(partners[name], flist, tlist, urldict, ) )
    t.start()
    threads[name] = t
for t in threads:
    threads.join()
s.close()

