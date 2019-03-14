# -*- coding: utf-8 -*-
import requests
import os
import time
import socket
"""
    @Author: mmciel
    @Time:2018年12月31日15:05:20
    @version：1.0
    
    python3.5
    实现思路：
        判断login_data.ini是否存在：不存在写入登录信息，存在则读取
        修改post请求数据包
        提交数据包
        通过www.baidu.com测试网络是否联通
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
dynamic_R6_data = ['1', '0', '0']
url_test = [
    "10.62.24.217",
    "10.62.25.128",
    "10.62.25.110"
]
referer_data = [
    "http://10.168.6.10/a70.htm?wlanuserip=10.62.24.217&wlanacip=10.168.6.9&wlanacname=&vlanid=0&ip=10.62.24.217&ssid=null&areaID=null&mac=00-00-00-00-00-00",
    "http://10.168.6.10/a70.htm?wlanuserip=10.62.25.128&wlanacip=10.168.6.9&wlanacname=&vlanid=0&ip=10.62.25.128&ssid=null&areaID=null&mac=00-00-00-00-00-00",
    "http://10.168.6.10/a70.htm?wlanuserip=10.62.25.110&wlanacip=10.168.6.9&wlanacname=&vlanid=0&ip=10.62.25.110&ssid=null&areaID=null&mac=00-00-00-00-00-00",
]
url = [
    "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.168.6.10&iTermType=2&wlanuserip=10.62.24.217&wlanacip=10.168.6.9&mac=00-00-00-00-00-00&ip=10.62.24.217&enAdvert=0&queryACIP=0&loginMethod=1",
    "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.168.6.10&iTermType=1&wlanuserip=10.62.25.128&wlanacip=10.168.6.9&mac=00-00-00-00-00-00&ip=10.62.25.128&enAdvert=0&queryACIP=0&loginMethod=1",
    "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.168.6.10&iTermType=1&wlanuserip=10.62.25.110&wlanacip=10.168.6.9&mac=00-00-00-00-00-00&ip=10.62.25.110&enAdvert=0&queryACIP=0&loginMethod=1",
]


def login(temp_url, temp_data, temp_headers):
    """提交请求"""
    requests.post(temp_url, data=temp_data, headers=temp_headers)
    time.sleep(0.5)
    requests.post(temp_url, data=temp_data, headers=temp_headers)
    time.sleep(0.5)
    test_result = is_net_china_ok()
    # print(test_result)
    return test_result
    pass


def solve_login():
    """尝试多个服务器登录"""
    data_num = len(url)
    print("对于用户"+login_data[0]+":")
    for i in range(data_num):
        print("====================================")
        temp_url = url[i]
        
        headers["Referer"] = referer_data[i]
        temp_headers = headers
        
        data["DDDDD"] = "," + dynamic_R6_data[i] + "," + login_data[0] + "@" + login_data[2]
        data["upass"] = login_data[1]
        data["R6"] = dynamic_R6_data[i]
        temp_data = data

        if login(temp_url, temp_data, temp_headers):
            print("尝试登录服务器："+url_test[i])
            print("登录成功")
            print("====================================")
            time.sleep(1)
            return
        else:
            print("尝试登录服务器："+url_test[i])
            print("登录失败")
            print("尝试登录下一个ip")
        # print(data)
        print("====================================")
        pass

    print("现有服务器地址无法访问，登录失败\n")
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
            f.write(line+'\n')
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
        if os.access(file_path, os.F_OK):
            login_data = get_login_data(login_data)
        else:
            print("初始化程序：请配置登录信息\n")
            set_login_data()
            login_data = get_login_data(login_data)

        solve_login()
pass
