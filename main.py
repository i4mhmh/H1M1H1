import re
import requests
import uuid
import threading

class page_scan:
    # 这里随机一个目录到全局变量里边,用于查看404页面回显的状态码
    # 全局定义一个ip跟端口,由main输入
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.random_filename = str(uuid.uuid1()) + 'qwerdf111.html'
        self.headers = headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}

    
    # 检测404 -》 200模块 like zhihu
    def filter_404(self):
        ip = self.ip
        port = self.port
        url_for404 = ip + ':' + port + '/' + self.random_filename
        r = requests.get(url = url_for404, headers = self.headers)
        # 判断拿到的404status是否为200状态,若是则对404页面进行特征提取
        if r.status_code == 200:
            title_404 = re.findall('<title>(.*?)</title>', r.text)[0]
            div_404 = len(re.findall('div', r.text))
            class_404 = len(re.findall('class', r.text))
            length_404 = len(r.text)
            # 打包404特征信息带回
            character_404 = [title_404, div_404, class_404, length_404]
            return character_404
        character_404 = 404
        return character_404

    # 正常404 直接跑
    def normal_model(self, file_name):
        url = self.ip + ':' + self.port + file_name
        slow_req = requests.get(url=url, headers=self.headers)
        if slow_req.status_code != 404:
            msg = ('[+]' + url + ' is Alive')
            print(msg)
            return msg
        else:
            print(url)
    def slow_mode(self, character_404, *file_name):
        url = self.ip + ':' + self.port + file_name[0]
        slow_req = requests.get(url=url, headers=self.headers)
        # 匹配特征
        try:
            slow_title = re.findall('<title*>(.*?)</title>',slow_req.text)[0]
        except:
            slow_title = ''
        slow_div = len(re.findall('div',slow_req.text))
        slow_class = len(re.findall('class',slow_req.text))
        slow_length = len(slow_req.text)
        if slow_title == character_404[0]:
            pass
        elif (slow_div > character_404[1] * 0.95 and slow_div < character_404[1] * 1.05) and (slow_class > character_404[2] * 0.95 and slow_class < character_404[2] * 1.05) and (slow_length > character_404[3] * 0.95 and slow_length < character_404[3] * 1.05):
            pass
        elif slow_req.status_code == 404:
            pass
        else:
            msg = "[+] " + url + ' is Alive'
            print(msg)
            return msg

def main():
    url = 'https://www.bilibili.com'
    port = '443'
    character_404 = page_scan(url,port).filter_404()
    
    if character_404 == 404:
        # 如果404页面正常回404 status,则开始多线程跑目录
        with open ('dictionary/test.txt', 'r') as f:
            i = 1
            for line in f.readlines():
                i = i + 1
                line = line.strip()
                thread_normal = threading.Thread(target= page_scan(url,port).normal_model(line)) 
                thread_normal.start()
                thread_normal.join()
    else:
        # 404页面返200, 在每次检索时都需要对特征进行模糊匹配
        with open ('dictionary/test.txt', 'r') as f:
            i = 1
            for line in f.readlines():
                i = i + 1
                line = line.strip()
                thread_normal = threading.Thread(target= page_scan(url,port).slow_mode(character_404, line)) 
                thread_normal.start()
                thread_normal.join()
main()