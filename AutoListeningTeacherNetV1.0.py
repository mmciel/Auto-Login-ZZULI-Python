import datetime
import json
import os
import random
import socket
import time
from urllib.parse import parse_qs, urlsplit

import requests
base_url = "http://www.msftconnecttest.com/redirect"
base_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": "www.msftconnecttest.com",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests": "1",
    # "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}
user_data_type0 = {
    "DDDDD":",0,",
    "upass":"",
    "R1":"0",
    "R2":"0",
    "R3":"0",
    "R6":"0",
    "para":"00",
    "0MKKey":"123456",
    "buttonClicked":"",
    "redirect_url":"",
    "err_flag":"",
    "username":"",
    "password":"",
    "user":"",
    "cmd":"",
    "Login":""
}
user_data_type1 = {
    "DDDDD":",1,",
    "upass":"",
    "R1":"0",
    "R2":"0",
    "R3":"0",
    "R6":"1",
    "para":"00",
    "0MKKey":"123456",
    "buttonClicked":"",
    "redirect_url":"",
    "err_flag":"",
    "username":"",
    "password":"",
    "user":"",
    "cmd":"",
    "Login":""
}

get_atter = {
    "wlanuserip":"",#
    "wlanacip":"",#
    "wlanacname":"",
    "vlanid":"0",
    "ip":"",#
    "ssid":"null",
    "areaID":"null",
    "mac":"00-00-00-00-00-00"
}
post_atter = {
    "hostname":"10.168.6.10",
    "iTermType":"1",
    "wlanuserip":"",#
    "wlanacip":"",#
    "mac":"00-00-00-00-00-00",
    "ip":"",#
    "enAdvert":"0",
    "queryACIP":"0",
    "loginMethod":"1"
}

def get_json():
    with open("userandpsw.json", 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict["data"],len(load_dict)

def get_userdata(offset):
    userdata,length = get_json()
    # 不用随机数，有风险
    # tempdict = userdata[random.randint(0,length)]
    # 获取当前日期
    day = datetime.datetime.now().day
    # 能保证每天用的账号是一样的
    tempdict = userdata[(day+30+offset)%length]
    return tempdict["user"],tempdict["password"]
def check_IP():
    response = requests.get(url = base_url, headers=base_headers)
    # print(len(response.url))
    if len(response.url) > 20 :#"http://10.30.1.19"
        return False
    else:
        return True
def is_net_ok():
    """
    判断网络是否链接
    :return:
    """
    # 如果锁了IP
    if check_IP():
        Log.info("IP被锁",False)
        Log.log("IP被锁")
        return False
    s = socket.socket()
    s.settimeout(1)
    try:
        status = s.connect_ex(('www.baidu.com', 443))
        if status == 0:
            s.close()
            return True
        else:
            s.close()
            return False
    except Exception as e:
        return False

def login(username,password):
    time.sleep(1)
    update_redirect_url = "http://10.168.6.10/a70.htm?wlanuserip=10.66.1.1&wlanacip=10.168.6.9&wlanacname=&vlanid=0&ip=10.66.1.1&ssid=null&areaID=null&mac=00-00-00-00-00-00"
    response = requests.get(url = base_url, headers=base_headers)
    if len(response.url) > 20 :#"http://10.30.1.19"
        update_redirect_url = response.url
    temp_url_dict = dict(parse_qs(urlsplit(update_redirect_url).query))
    wlanuserip = temp_url_dict['wlanuserip'][0]
    wlanacip = temp_url_dict['wlanacip'][0]
    get_atter['wlanuserip'] = wlanuserip
    get_atter["wlanacip"] = wlanacip
    get_atter["ip"] = wlanuserip

    real_url = 'http://10.168.6.10/a70.htm?' \
               'wlanuserip=' + str(get_atter['wlanuserip']) + \
               '&wlanacip=' + str(get_atter['wlanacip']) + \
               '&wlanacname=' + str(get_atter['wlanacname']) + \
               '&vlanid=' + str(get_atter['vlanid']) + \
               '&ip=' + str(get_atter['wlanuserip']) + \
               '&ssid=' + str(get_atter['ssid']) + \
               '&areaID=' + str(get_atter['areaID']) + \
               '&mac=' + str(get_atter['mac'])
    Log.info("截获用户服务器与校验服务器IP...",False)
    headers["Referer"] = real_url
    post_atter['wlanuserip'] = wlanuserip
    post_atter["wlanacip"] = wlanacip
    post_atter["ip"] = wlanuserip
    dynamic_R6_data = ['0', '1', '2']

    final_url = "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:" \
                "&hostname=" + post_atter["hostname"] + "&iTermType=" + post_atter["iTermType"] + \
                "&wlanuserip=" + post_atter["wlanuserip"] + "&wlanacip=" + post_atter["wlanacip"] + \
                "&mac=" + post_atter["mac"] + "&ip=" + post_atter["ip"] + \
                "&enAdvert=" + post_atter["enAdvert"] + "&queryACIP=" + post_atter["queryACIP"] + \
                "&loginMethod=" + post_atter["loginMethod"]

    # print(final_url)
    user_data_type0["DDDDD"] = ",0,"+username
    # user_data_type0["DDDDD"] = ",0,"+username+"@zzulis"
    user_data_type0["upass"] = password

    user_data_type1["DDDDD"] = ",1,"+username
    # user_data_type1["DDDDD"] = ",1,"+username+"@zzulis"
    user_data_type1["upass"] = password
    time.sleep(1)
    Log.info("正在登录...", False)
    status = requests.post(final_url,headers=headers,data=user_data_type0).url
    status_dict = dict(parse_qs(urlsplit(status).query))
    time.sleep(2)
    if  status_dict.__contains__("ErrorMsg"):
        status = requests.post(final_url,headers=headers,data=user_data_type1).url
        status_dict = dict(parse_qs(urlsplit(status).query))
        if status_dict.__contains__("ErrorMsg"):
            return status_dict["ErrorMsg"]
        else :
            return "success"
    else :
        return "success"

class Log():
    @staticmethod
    def log(message):
        with open(r'./link_teacher.log', 'a+',encoding="utf-8") as f:
            f.write("["+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"-->"+message+"]\n")

    @staticmethod
    def info(message,handle):
        if handle:
            print(">>>Info:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"-->"+message)
        else:
            print(">>>Info:" + message)
    @staticmethod
    def warn(message,handle):
        if handle:
            print(">>>Warning:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"-->"+message)
        else:
            print(">>>Warning:" + message)
    @staticmethod
    def error(message,handle):
        if handle:
            print(">>>Error:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"-->"+message)
        else:
            print(">>>Error:" + message)
msg_dict = {
    "aW51c2UsIGxvZ2luIGFnYWlu" : "多端登录",
    "NTEy":"AC认证失败",
    "dXNlcmlkIGVycm9yMQ==" : "账户不存在",
    "QXV0aGVudGljYXRpb24gRmFpbCBFcnJDb2RlPTE2" : "非正常时段",
    "success":"登录成功"
}
def solve_status(status):
    if msg_dict.__contains__(status):
        Log.info(status,True)
    else :
        Log.info(msg_dict[status],True)

if __name__ == "__main__":
    Log.info("ZZULI 网络自动登录工具V1.0",False)
    Log.info("author：mmciel",False)
    Log.info("功能：支持多账号登录；支持断线重连；支持自定义添加账号；支持zzuli-teacher；",False)
    Log.info("正常启动...",False)
    wifi = "zzuli-teacher"

    cmd = "netsh wlan connect name={}".format(wifi)

    flag = True

    while flag:
        if is_net_ok():
            Log.info("网络正常连接",True)
            Log.log("网络正常连接")
        else:
            Log.info("网络连接异常",True)
            Log.log("网络连接异常")
            Log.info("正在打开WLAN（{}）".format(wifi),False)
            os.system(cmd)
            time.sleep(4)
            # try:
            username, password = get_userdata(0)
            Log.info("获取登录数据：["+username+":"+password+"]", False)
            Log.log("获取登录数据：["+username+":"+password+"]")
            status = login(username, password)
            solve_status(status)
            count = 1
            while status != "success" and count < 4:
                # 加入偏移量 换账号登录尝试
                username, password = get_userdata(count)
                Log.info("再次尝试：[" + username + ":" + password + "]", False)
                Log.log("再次尝试：[" + username + ":" + password + "]")
                status = login(username, password)
                count = count + 1
        time.sleep(20)









