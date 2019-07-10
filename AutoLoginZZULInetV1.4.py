"""
ZZULI校园网自动连接程序
author:mmciel
time:2019-6-19 22:46:48
end-time：2019-7-10 19:30:32
version:1.4
update：
    1.3太慢了，等不及了，重写个暴力的
    重构爬虫逻辑，以前逻辑混乱，原因：信号与系统是个什么鬼啊，一点也看不懂啊。
    新增Linux、windows判断逻辑。
    还在考虑密码要不要隐写
    希望半小时写完，还要看数据结构呢
    登录错误信息反馈给用户

    新增了登录选项
    新增了抢占
"""

import platform
import os
import socket
import time
from urllib.parse import parse_qs
from urllib.parse import urlsplit
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer":"",
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
user_data = {
    "DDDDD":"",
    "upass":"",
    "R1":"0",
    "R2":"0",
    "R3":"0",
    "R6":"",
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
msg_dict = {
    "aW51c2UsIGxvZ2luIGFnYWlu" : "多端登录",
    "NTEy":"AC认证失败",
    "dXNlcmlkIGVycm9yMQ==" : "账户不存在",
    "QXV0aGVudGljYXRpb24gRmFpbCBFcnJDb2RlPTE2" : "非正常时段"
}

static_url = "http://www.msftconnecttest.com/redirect"
dynamic_R6_data = ['0','1','2']
def loading_config():
    """
    加载配置信息
    :return:
    """
    file_path = os.getcwd() + "/login_config.ini"
    temp_data_list = []
    # 判断是否有配置文件
    if os.access(file_path, os.F_OK):
        '''加载文件到list'''
        try:
            f = open(file_path)
            for line in f.readlines():
                temp_data_list.append(line.strip('\n'))
            f.close()
            print("配置文件加载完毕：login_config.ini")
            print("成功写入登录账号：" + str(temp_data_list[0]))
            return temp_data_list
        except IOError:
            print("login_config.ini加载失败")
            e_exit()
    else:

        '''用户初始化配置'''
        first_word()
        ini_data = []
        for i in range(3):
            if i == 0:
                ini_data.append(input("请输入上网账号："))
            if i == 1:
                ini_data.append(input("请输入上网密码："))
            if i == 2:
                t = input("请输入运营商:\n联通【1】\n移动【2】\n单宽【3】\n校内资源【4】\n校园网【5】\n")
                if t == "1":
                    ini_data.append("unicom")
                if t == "2":
                    ini_data.append("cmcc")
                if t == "3":
                    ini_data.append("other")
                if t == "4":
                    ini_data.append("inside")
                if t == "5":
                    ini_data.append("zzulis")
        if len(ini_data) != 3:
            print("数据录入错误")
            e_exit()
        else:
            f = open(file_path, 'w')
            for line in ini_data:
                f.write(line + '\n')
            f.close()
        return ini_data

def get_real_url():
    # try:
    static_response = requests.get(static_url, headers=headers,timeout=5)
    temp_url = static_response.url
    temp_url_dict = dict(parse_qs(urlsplit(temp_url).query))
    wlanuserip = temp_url_dict['wlanuserip'][0]
    wlanacip = temp_url_dict['wlanacip'][0]

    get_atter['wlanuserip'] = wlanuserip
    get_atter["wlanacip"] = wlanacip
    get_atter["ip"] = wlanuserip
    print("已解析登录服务器："+wlanuserip)
    print("已解析校验服务器："+wlanacip)

    # 构造请求
    real_url = 'http://10.168.6.10/a70.htm?' \
                'wlanuserip=' + str(get_atter['wlanuserip']) + \
                '&wlanacip=' + str(get_atter['wlanacip']) + \
                '&wlanacname=' + str(get_atter['wlanacname']) + \
                '&vlanid=' + str(get_atter['vlanid']) + \
                '&ip=' + str(get_atter['wlanuserip']) + \
                '&ssid=' + str(get_atter['ssid']) + \
                '&areaID=' + str(get_atter['areaID']) + \
                '&mac=' + str(get_atter['mac'])

    headers["Referer"] = real_url
    post_atter['wlanuserip'] = wlanuserip
    post_atter["wlanacip"] = wlanacip
    post_atter["ip"] = wlanuserip
    final_url = "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:" \
                 "&hostname=" + post_atter["hostname"] + "&iTermType=" + post_atter["iTermType"] + \
                "&wlanuserip=" + post_atter["wlanuserip"] + "&wlanacip=" + post_atter["wlanacip"] + \
                "&mac=" + post_atter["mac"] + "&ip=" + post_atter["ip"] + \
                "&enAdvert=" + post_atter["enAdvert"] + "&queryACIP=" + post_atter["queryACIP"] + \
                "&loginMethod=" + post_atter["loginMethod"]
    # print(final_url)
    print("截获真正登录地址：***")
    return final_url
    # except:
    #     print("访问超时！")
    #     e_exit()

def e_exit():
    print("2秒后退出...")
    time.sleep(2)
    exit()
def is_net_ok():
    """
    判断网络是否链接
    :return:
    """
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
# def print_msg(url):
#     msg_data = dict(parse_qs(urlsplit(url).query))
#     msg = msg_data['ErrorMsg'][0]
#     # print(msg)
#
#     if msg == "NTEy":
#         print(">>>登录结果：失败\n>>>原因：AC认证失败")
#         return False
#     elif msg == "dXNlcmlkIGVycm9yMQ==":
#         print(">>>登录结果：失败\n>>>原因：账户不存在")
#         return True
#     elif msg == "QXV0aGVudGljYXRpb24gRmFpbCBFcnJDb2RlPTE2":
#         print(">>>登录结果：失败\n>>>原因：非正常时段")
#         return True

    # print(msg_data)
def login(temp_url, temp_data, temp_headers):
    flag = True
    retry = 1
    while flag and retry<4:
        res = requests.post(temp_url, data=temp_data, headers=temp_headers)
        time.sleep(1)
        msg_data = dict(parse_qs(urlsplit(res.url).query))

        if "ErrorMsg" in msg_data:
        # 错误信息
            msg = msg_data['ErrorMsg'][0]
            if msg in msg_dict:
                # 已知错误信息
                print(">>>登录结果：失败\n>>>原因："+msg_dict[msg])
                if msg == "aW51c2UsIGxvZ2luIGFnYWlu" or msg == "NTEy":
                    print(">>>尝试解决：再次请求")
                    retry = retry + 2
                else:
                    return False
            else:
                print(">>>登录结果：失败\n>>>原因：未知")
                print("正在重试：第"+retry+"次")
                retry = retry + 1
        else:
            print(">>>登录结果：失败\n>>>原因：登录成功")
            return True
    return False


def word():
    """
    工具说明
    :return:
    """
    print("======================Auto Login ZZULI Net V1.4======================\n")
    print("                                          by:mmciel 761998179@qq.com \n")
    print("                                          微信公众号：并非一无所有       \n")
    print("=====================================================================")
def first_word():
    print("使用说明：")
    print("0.打开程序")
    print("1.本程序放到非桌面，右键将快捷发送到桌面会有更好体验")
    print("2.首次使用按照提示配置，配置文件与本程序同目录，删除后需要重新配置")
    print("3.后续使用双击程序即可")
    print("=====================================================================")

# def is_link():
#     code = requests.get("http://www.baidu.com")
#     if(code.status_code == 200):
#         return False
#     else:
#         return False
if __name__ == "__main__":
    word()
    '''加载配置文件'''
    login_data = loading_config()
    # print(login_data)
    '''启动wifi'''
    # 判断系统版本，决定是否通过dos启动wlan
    system_version = platform.platform()
    print("程序运行系统环境："+system_version)
    if "Windows" in system_version:
        # 系统是windows
        try:
            os.system('netsh wlan connect name=zzuli-student')
            time.sleep(1)
            print("打开系统网络连接：zzuli-student")
        except:
            print("wifi连接失败，请检查设置或驱动！")
            e_exit()
        pass
    else:
        # 系统是linux
        os.system('sudo ip link set wlan0 up')
        os.system('sudo iw dev wlan0 scan | zzuli-student')
        pass
    '''判断是否联网'''
    if is_net_ok():
        print("连接成功")
        e_exit()
    else:
        '''发送请求'''
        real_url = get_real_url()
        for i in range(len(dynamic_R6_data)):
            print("正在尝试登录参数：R6-" + dynamic_R6_data[i])
            user_data["DDDDD"] = "," + dynamic_R6_data[i] + "," + login_data[0] + "@" + login_data[2]
            user_data["upass"] = login_data[1]
            user_data["R6"] = dynamic_R6_data[i]
            if login(real_url, user_data, headers):
                break
