#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-03-20 15:07:12
# @Author  : Eamonn (china.eamonn@gmail.com)

import warnings
warnings.filterwarnings("ignore")  # 忽略警告

# =========================================请求类=========================================

#   请求器


def get(url, timetry=3, headers="", ip='', timeout=60, ex="", data='', cache=False, cookie='', cachedur=2 , getcks=False):
    import requests
    parm = struct_parm(
        {'url': url, 'data': data, 'headers': headers, 'cookie': cookie})
    if headers != "":
        headers = f2h(headers)

    if ip != '':
        ip = {"http": ip, "https": ip}

    if cache:  # 文件缓存
        hash = md5(parm['url']+str(data))  # 参数哈希待调优
        state, res_text = rwcache(hash, suffix='.html', dur=cachedur)
        if state:
            return exa(res_text, ex)
    response, try_time = None, 1
    while 1:
        try:
            if data == '':
                response = requests.get(
                    parm['url'], headers=parm['headers'], proxies=ip, timeout=timeout)
            else:
                response = requests.post(
                    parm['url'], headers=parm['headers'], data=parm['data'], proxies=ip, timeout=timeout)

            if response.status_code != None:
                break

        except Exception as e:
            try_time += 1
            if try_time > timetry:
                if ex != '':
                    return 404, e
                else:
                    return e
    if response.status_code == 200:
        if getcks:
            return response.cookies
        res_text = response.text
        if cache:
            if len(res_text) > 0:
                rwcache(hash, res_text, suffix='.html', dur=cachedur)
        if ex == 'jq' or ex == 'xpath' or ex == 'bs4' or ex == 'json':
            _, rt = exa(res_text, ex)
            return _, rt
        if ex == "":
            return res_text

#   参数构造器


def struct_parm(parm):
    if 'headers' in parm:
        cookie = ''
        if 'cookie' in parm:
            cookie = parm['cookie']
        parm['headers'] = struct_headers(parm['headers'], cookie)
    if 'url' in parm:
        parm['url'] = struct_url(parm['url'])
    if 'data' in parm:
        parm['data'] = struct_data(parm['data'])
    return parm

#   构造header


def struct_headers(header, cookie):
    header_s = {"User-Agent": rua()}  # 生成最新ua
    if type(header) == str and header != '':
        header = f2h(header)
    if type(header) == list:
        hd1, hd2 = header
        hd = f2h(hd1)
        hd.update(hd2)
        header = hd
    if header != '':
        header_s.update(header)  # 更新ua
    if cookie != '':
        header_s['cookie'] = cookie
    header = header_s
    return header

#   构造url


def struct_url(url):
    if url[:4] != 'http':
        url = r'http://'+url
    if type(url) == list:
        urlc, parc = url
        if r'?' in urlc:
            urld = urlc.split('?')
            urldd, pardd = urld
            parddd = pardd.split('&')
            dd = {}
            for d in parddd:
                if '=' in d:
                    d1, d2 = d.split('=')
                    dd[d1] = d2
            dd.update(parc)
            urlc, parc = urldd, dd
        par = ''
        for key in parc:
            par = par+key+"="+str(parc[key])+"&"
        url = urlc+"?"+par[:-1]
    return url

#   构造data


def struct_data(data):
    if type(data) == str and data != '':
        import urllib.parse
        mdata = map(lambda i: i.split('='),
                    urllib.parse.unquote(data).split('&'))
        data = {}
        for i in mdata:
            if i[0] not in data:
                data[i[0]] = i[1]
            else:
                if type(data[i[0]]) == str:
                    data[i[0]] = [data[i[0]]]
                if type(data[i[0]]) == list:
                    data[i[0]].append(i[1])
    return data


def rwcache(fhash, res_text='', suffix='', dur=2, path='cache', fname='', aw='w'):
    init()  # 修改工作空间
    res_text = str(res_text)
    if len(fname) > 0:
        fname = r'/'+fname
    if dur != 9:
        ftdur = r'/'+ftime(dur)
    else:
        ftdur = ''
    if res_text == '':
        import os
        # 目录路径,所有子目录,非目录子文件
        for root, dirs, fs in os.walk(r'%s/%s%s' % (path, ftdur, fname)):
            for f in fs:
                if f == fhash+suffix:  # os.path.splitext()
                    res_text = rw(os.path.join(root, f))
                    return True, res_text
        return False, ''
    else:
        rw(r'%s%s%s/%s%s' % (path, ftdur, fname, fhash, suffix), res_text, aw=aw)


def rw(path, line=True, aw='a', sp="", cut=False):
    init()  # 修改工作空间
    import os
    path0 = os.path.split(path)[0]
    if path0 != '':
        mk(path0, False)
    if line == True:
        aw = 'r'
    if line == None:
        line = ''
        aw = 'w'
    if aw == 'r':
        arr = []
        with open(path, 'r', encoding=get_encode(path, 'text'), errors="ignore") as f:
            if aw == "r" and not cut:
                return f.read().strip()
            for l in f:
                if sp == "":
                    arr.append(l.replace("\n", ""))
                else:
                    arr.append(l.replace("\n", "").split(sp))
        return arr
    if aw == 'w' or aw == 'a':
        if type(line) == set or type(line) == list:
            cont = ''
            for l in line:
                cont += l + "\n"
            with open(path, aw, encoding='utf-8') as f:
                f.write(cont)
        else:
            with open(path, aw, encoding='utf-8') as f:
                if aw == 'w' and line == '':
                    f.write('')
                else:
                    f.write(line + "\n")
    if aw == 'wb':
        with open(path, 'wb') as f:
            f.write(line)


def mk(path, cut=True):
    init()  # 修改工作空间
    import os
    import sys
    if cut:
        path = path.replace('.', '/')
    rpath = os.path.dirname(os.path.realpath(
        __file__)).replace('\\', '/')+'/'+path
    if not os.path.exists(path):
        os.makedirs(path)
    return rpath

#   编码处理器


def get_encode(response, type='html'):
    import requests
    if type == 'html':
        rxt = response.text
        encodings = requests.utils.get_encodings_from_content(rxt)
        if encodings:
            return encodings[0]
        else:
            return response.apparent_encoding
    if type == 'text':
        try:
            with open(response, 'r', encoding='utf-8') as f:
                f.read()
                encoding = 'utf-8'
        except:
            encoding = 'gbk'
        return encoding


def init():
    import os
    import sys
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    path = path.replace('\\', '/')+'/'
    os.chdir(path)  # 修改工作目录


def md5(*arg):
    import hashlib
    hl = hashlib.md5()
    line = ''.join(list(map(lambda x: str(x), arg)))
    hl.update(line.encode(encoding='utf-8'))
    return hl.hexdigest()

#   格式化html


def exa(res_text, ex=''):
    if ex == 'bs4':
        import bs4
        soup = bs4.BeautifulSoup(res_text, "html.parser")
        return res_text, soup
    if ex == 'xpath':
        from lxml import etree
        selector = etree.HTML(res_text)
        return res_text, selector
    if ex == 'jq':
        from lxml import etree
        from pyquery import PyQuery as pq
        try:
            doc = pq(etree.fromstring(res_text))
        except:
            doc = pq(res_text)
        return res_text, doc
    if ex == 'json':
        import json
        js = json.loads(res_text)
        return res_text, js
    if ex == 'btf':
        import bs4
        soup = bs4.BeautifulSoup(res_text, "html.parser")
        return soup.prettify()

#   fiddler转header


def f2h(txt):
    arr = txt.split("\n")
    headers = {}
    for i in arr:
        if ": " in i:
            ic = i.split(": ")
            headers[ic[0].replace("\t", "").replace(" ", "")] = ic[1]
    return headers
    # =========================================并发类=========================================

#   线程池


def pool(callback, lists, threadNum=20):
    # 需要开启多线程的函数，任务列表，线程数量(默认为20)
    import threadpool
    pool = threadpool.ThreadPool(threadNum)
    requests = threadpool.makeRequests(callback, lists)
    [pool.putRequest(req) for req in requests]
    pool.wait()

#   线程锁


def lock():
    import threading
    lock = threading.Lock()
    return lock

#   队列

def queue():
    from queue import Queue
    return Queue()

    # ========================================数据库类========================================

#   存入mongodb数据库


class save_mongo():
    def __init__(self, ip="127.0.0.1", fname='', dname="Default_name", time=True):
        import pymongo
        if fname == '':
            if time:
                self.cname = 'Default_name'+"_" + ftime(2)
            else:
                self.cname = 'Default_name'
        else:
            if time:
                self.cname = fname + "_" + ftime(2)
            else:
                self.cname = fname
        self.conn_mgo = pymongo.MongoClient(ip, 27017)
        self.db = self.conn_mgo[dname]
        self.collection = self.db[self.cname]

    def insert(self, arr):
        self.collection.insert(arr)

    def insert_many(self, arr):
        self.collection.insert_many(arr)

#   从mongodb取


def get_mongo(ip="127.0.0.1", dname="", fname=""):
    import pymongo
    if dname == "":
        print("Please select database(dname).")
    if fname == "":
        print("Please select form(fname).")
    if dname != "" and fname != "":
        client = pymongo.MongoClient(ip, 27017)
        db = client[dname]
        collection = db[fname]
        return collection


    # =========================================工具类=========================================

#   多个replace


def rpc(str, arr=[' ']):
    for i in arr:
        str = str.replace(i, '')
    return str

#   判断类型


def mtype(*args):
    typelist = []
    for i in args:
        typelist.append(type(i))
    return typelist

#   时间格式


def ftime(i=0):
    import time
    if i == 0:
        return time.strftime("%Y_%m_%d %H:%M:%S", time.localtime())
    if i == 1:
        return time.strftime("%Y_%m_%d %H%M%S", time.localtime())
    if i == 2:
        return time.strftime("%Y_%m_%d", time.localtime())
    if i == 3:
        return time.strftime("%Y%m%d", time.localtime())
    if i == 4:
        return time.strftime("%Y_%m", time.localtime())
    if i == 5:
        return time.strftime("%Y%m", time.localtime())
    if i == 6:
        return time.strftime("%Y", time.localtime())
    if i == 7:
        return ''

#   时间暂停


def sleep(t):
    import time
    time.sleep(t)

#   格式化打印


def print(arg):
    from pprint import pprint
    pprint(arg)

#   最新浏览器随机useragent


def rua(lang="zh-CN", pl=[2, 4, 3, 1]):
    import random
    user_agent_list = [
        'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language} rv:{Firefox}) Gecko/{builddata} Firefox/{Firefox}'.format(
            **{'WindowsNT': _wc(["6.1", "6.2", "6.3", "10.0"], [3, 2, 2, 3]), 'WOW64':_wc(["", " WOW64;", " Win64;", " x64;"], [3, 4, 2, 1]), 'language':_wc(["", " {};".format(lang)], [6, 4]), 'builddata':random.choice(["201{}0{}{}".format(random.randint(0, 6), random.randint(1, 9), random.randint(10, 28))]), 'Firefox': random.choice(["50.0.1", "50.0.2", "50.0", "50.01", "50.010", "50.011", "50.02", "50.03", "50.04", "50.05", "50.06", "50.07", "50.08", "50.09", "50.1.0", "51.0.1", "51.0", "51.01", "51.010", "51.011", "51.012", "51.013", "51.014", "51.02", "51.03", "51.04", "51.05", "51.06", "51.07", "51.08", "51.09", "52.0.1", "52.0.2", "52.0", "52.01", "52.02", "52.03", "52.04", "52.05", "52.06", "52.07", "52.08", "52.09", "52.1.0", "52.1.1", "52.1.2", "52.2.0", "52.2.1", "52.3.0", "52.4.0", "52.4.1", "53.0.2", "53.0.3", "53.0", "53.01", "53.010", "53.02", "53.03", "53.04", "53.05", "53.06", "53.07", "53.08", "53.09", "54.0.1", "54.0", "54.01", "54.010", "54.011", "54.012", "54.013", "54.02", "54.03", "54.04", "54.05", "54.06", "54.07", "54.08", "54.09", "55.0.1", "55.0.2", "55.0.3", "55.0", "55.01", "55.010", "55.011", "55.012", "55.013", "55.02", "55.03", "55.04", "55.05", "55.06", "55.07", "55.08", "55.09", "56.0.1", "56.0", "56.01", "56.010", "56.011", "56.012", "56.02", "56.03", "56.04", "56.05", "56.06", "56.07", "56.08", "56.09", "57.03", "57.04", "57.05", "57.06"]), }),
        'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language}) AppleWebKit/{Safari} (KHTML, like Gecko) Chrome/{Chrome} Safari/{Safari}'.format(
            **{'WindowsNT': _wc(["6.1", "6.2", "6.3", "1"], [3, 2, 2, 3]), 'WOW64':_wc(["", " WOW64;", " Win64;", " x64;"], [3, 4, 2, 1]), 'language':_wc(["", " {};".format(lang)], [6, 4]), 'Chrome': '{0}.{1}.{2}.{3}'.format(random.randint(50, 61), random.randint(0, 9), random.randint(1000, 9999), random.randint(10, 99)), 'Safari': '{0}.{1}'.format(random.randint(100, 999), random.randint(0, 99)), }),
        'Mozilla/5.0 ({compatible}Windows NT {WindowsNT};{WOW64} MSIE {ie}.0; Trident/{Trident}.0;){Gecko}'.format(
            **{'compatible': random.choice(["", "compatible; "]), 'WindowsNT': _wc(["6.1", "6.2", "6.3", "10"], [3, 2, 2, 3]), 'WOW64':_wc(["", " WOW64;", " Win64;", " x64;"], [3, 4, 2, 1]), 'ie': random.randint(10, 11), 'Trident': random.randint(5, 7), 'Gecko':random.choice(["", " like Gecko;"])}),
        'Mozilla/5.0 (Windows NT {WindowsNT}; MSIE 9.0;) Opera {opera1}.{opera2}'.format(
            **{'WindowsNT': _wc(["6.1", "6.2", "6.3", "10"], [3, 2, 2, 3]), 'opera1': random.randint(10, 12), 'opera2': random.randint(10, 99)}),
    ]
    rs = _wc(user_agent_list, pl) 
    return rs

#   随机返回列表里的一个元素


def _wc(list, weight):
    import random
    new_list = []
    for i, val in enumerate(list):
        for i in range(weight[i]):
            new_list.append(val)
    return random.choice(new_list)

#   列表去重


def rd(list):
    from functools import reduce

    def f(x, y): return x if y in x else x + [y]
    list = reduce(f, [[], ] + list)
    return list



#   获取列表第一个


def get1(arr):
    if len(arr) > 0:
        return arr[0]
    return ''



#   数组切片


def cut(arr, cut=5):
    arc, tmp_arr, tmp_a = [], [], []
    for x, i in enumerate(arr):
        tmp_arr.append(i)
        if (x+1) % cut == 0:
            arc.append(tmp_arr)
            tmp_arr = []
        tmp_a = tmp_arr
    arc.append(tmp_a)
    try:
        arc.remove([])
    except:
        pass
    return arc
