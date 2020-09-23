# distributed-downloader
This is a distributed tool for a group to download data granules together. The data granules are first downloaded by a remote server and than delivered to several computers. An English version of the ReadMe file will be offered soon if it is needed.
# 分布式下载器
利用多台计算机进行同一数据集的下载任务。数据集首先下载到远程服务器上，然后再由远程服务器转发到多台计算机上。
这里给出了下载哨兵5号二氧化氮Level2数据的例子。直接在国内下载NASA EarthData的数据非常慢，而下载数据量可以达到T级别以上。所以通过AWS的云服务器下载数据集，然后再分发到研究组的多台计算机上。
## 运行环境
### 云服务器
```shell
Ubuntu 19.10
Python 3.7.5
```
### 本地计算机
```shell
Win 10
Python 3.7
```
## 使用方法
需要下载其它数据集请替换数据下载脚本download.sh

将下载列表download.json，下载脚本download.sh和python脚本disdown_server.py放到云服务器，运行disdown_server.sh
```shell
python disdown_server.sh
```

在本地计算机（多台）运行disdown_client.py
```shell
python disdown_client.py
```
