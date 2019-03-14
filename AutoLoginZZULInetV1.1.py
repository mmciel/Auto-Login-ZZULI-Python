# -*- coding: utf-8 -*-
import requests
import os
import time
import socket
from urllib.parse import parse_qs

"""
    @Author: mmciel
    @Time:2019年1月2日
    @version：1.1

    python3.5
    实现思路：
        判断login_data.ini是否存在：不存在写入登录信息，存在则读取
        修改post请求数据包
        提交数据包
        通过www.baidu.com测试网络是否联通
        update：
        抓取源地址，锁定跳转地址，提取跳转url，获取服务器ip。数据提交到指定服务器
"""
# 请求头字典
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Referer": "",
}
# 请求包字典
data = {
    "DDDDD": "",
    "upass": "",
    "R1": "0",
    "R2": "0",
    "R3": "0",
    "R6": "",
    "para": "00",
    "0MKKey": "123456",
    "buttonClicked": "",
    "redirect_url": "",
    "err_flag": "",
    "username": "",
    "password": "",
    "user": "",
    "cmd": "",
    "Login": ""
}
# 配置文件地址
file_path = os.getcwd() + "\login_data.ini"
# 登录信息录入
login_data = []

# 多个服务器访问
dynamic_R6_data = ['0', '1']

# 请求头封装的temp data
referer_data = [
    "http://10.168.6.10/a70.htm?",
    "wlanuserip=",
    "&wlanacip=10.168.6.9",
    "&wlanacname=",
    "&vlanid=0",
    "&ip=",
    "&ssid=null&areaID=null&mac=00-00-00-00-00-00",
]
# url的封装 temp
url = [
    "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.168.6.10",
    "&iTermType=1",
    "&wlanuserip=",
    "&wlanacip=10.168.6.9",
    "&mac=00-00-00-00-00-00",
    "&ip=",
    "&enAdvert=0&queryACIP=0&loginMethod=1",
]
msg = [
    "登录失败",
    "登录成功",
    "",
    "",
]


def login(temp_url, temp_data, temp_headers):
    """提交请求"""
    requests.post(temp_url, data=temp_data, headers=temp_headers)
    time.sleep(1)
    if is_net_china_ok():
        return True
    else:
        # print("")
        requests.post(temp_url, data=temp_data, headers=temp_headers)
        time.sleep(0.8)
        test_result = is_net_china_ok()
        # print(test_result)
        return test_result
    pass


def solve_login():
    """获取动态url 请求头"""

    # 静态url提取真实url
    static_url = "http://www.msftconnecttest.com/redirect"
    print("正在截获动态url："+static_url)
    response = requests.get(static_url)
    temp = str(response.url).split('?', 1)
    happy_str = temp[1]
    happy_data = parse_qs(happy_str)
    print("成功获取服务器地址："+ happy_data['wlanuserip'][0])
    # print(happy_data)

    # 写入url 请求头的临时key
    referer_data[1] = referer_data[1] + happy_data['wlanuserip'][0]
    referer_data[5] = referer_data[5] + happy_data['wlanuserip'][0]
    url[2] = url[2] + happy_data['wlanuserip'][0]
    url[5] = url[5] + happy_data['wlanuserip'][0]

    # 构造请求
    temp_url = ""
    temp_referer = ""
    for i in url:
        temp_url = temp_url + i
    for i in referer_data:
        temp_referer = temp_referer + i
    headers["Referer"] = temp_referer
    temp_headers = headers
    print("请求构造成功！")

    # 这里是由于不知道R6参数的含义，只能提交两个参数，有一个能命中就行了
    for i in range(len(dynamic_R6_data)):
        print("正在尝试登录参数：R"+dynamic_R6_data[i])
        data["DDDDD"] = ","+dynamic_R6_data[i]+","+login_data[0]+"@"+login_data[2]
        data["upass"] = login_data[1]
        data["R6"] = dynamic_R6_data[i]
        if login(temp_url, data, temp_headers):
            return msg[1]
        else:
            continue
    return msg[0]
    pass


def set_login_data():
    """向login_data.ini中写入登录信息"""
    ini_data = []
    for i in range(3):
        if i == 0:
            ini_data.append(input("请输入登录名："))
        if i == 1:
            ini_data.append(input("请输入密码："))
        if i == 2:
            t = input("请输入运营商编码==> 联通：1 ; 移动：2; 单宽：3:")
            if t == "1":
                ini_data.append("unicom")
            if t == "2":
                ini_data.append("cmcc")
            if t == "3":
                ini_data.append("other")

    if len(ini_data) != 3:
        print("error:input data")
        return
    else:
        f = open(file_path, 'w')
        for line in ini_data:
            f.write(line + '\n')
        f.close()
    pass


def get_login_data(temp):
    """从login_data.ini中提取登录信息"""
    try:
        f = open(file_path)
        for line in f.readlines():
            temp.append(line.strip('\n'))
        f.close()
        return temp
    except IOError:
        print("login_data.ini file not read")
        return []
    pass


def is_net_ok(test_server):
    s = socket.socket()
    s.settimeout(1)
    try:
        status = s.connect_ex(test_server)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False


def is_net_china_ok(test_server=('www.baidu.com', 443)):
    return is_net_ok(test_server)


def open_wifi():
    """win10右下角的wifi管理器就是个垃圾！"""
    os.system('netsh wlan connect name=zzuli-student')
    time.sleep(1)
'''
    获取登录信息
    请求登录信息
'''
if __name__ == '__main__':
    print("======================auto login net  by:mmciel======================\n")

    if is_net_china_ok():
        print("网络已连接...")
        time.sleep(1)
    else:
        open_wifi()
        if os.access(file_path, os.F_OK):
            login_data = get_login_data(login_data)
        else:
            print("初始化程序：请配置登录信息\n")
            set_login_data()
            login_data = get_login_data(login_data)

        print(solve_login())
        time.sleep(1)
pass
