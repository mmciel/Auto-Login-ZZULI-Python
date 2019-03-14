"""
ZZULI校园网自动连接程序
author:mmciel
time:2019年3月14日17:31:10
version:1.3
"""
import os
import socket
import time

import requests
from urllib.parse import parse_qs
from urllib.parse import urlsplit

# 简单请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
}
# 复杂请求头
login_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer":"",
}
# url参数表
get_par = {
    "wlanuserip":"",#
    "wlanacip":"",#
    "wlanacname":"",
    "vlanid":"0",
    "ip":"",#
    "ssid":"null",
    "areaID":"null",
    "mac":"00-00-00-00-00-00"
}
# post 请求包
user_post = {
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
# post url参数表
post_par = {
    "hostname":"10.168.6.10",
    "iTermType":"1",
    "wlanuserip":"10.66.67.119",
    "wlanacip":"10.168.6.9",
    "mac":"00-00-00-00-00-00",
    "ip":"10.66.67.119",
    "enAdvert":"0",
    "queryACIP":"0",
    "loginMethod":"1"
}
static_url = "http://www.msftconnecttest.com/redirect"

file_path = os.getcwd() + "\login_data.ini"

dynamic_R6_data = ['0', '1','2']


def get_url():
    static_response = requests.get(static_url, headers=headers)
    static_response_302_str = str(static_response.url)
    # 从静态链接302中的跳转页面获取信，用于构造真实的登录页面地址
    static_response_302_dict = dict(parse_qs(urlsplit(static_response.url).query))
    # 写入请求参数
    get_par['wlanuserip'] = static_response_302_dict['wlanuserip'][0]
    get_par['wlanacip'] = static_response_302_dict['wlanacip'][0]
    get_par['ip'] = static_response_302_dict['wlanuserip'][0]
    print("成功截获wlanuserip服务器："+get_par['wlanuserip'])
    print("成功截获wlanacip服务器：" + get_par['wlanacip'])
    real_url_head_str = "http://10.168.6.10/a70.htm?"
    real_url_par_str = 'wlanuserip=' + str(get_par['wlanuserip']) + \
                       '&wlanacip=' + str(get_par['wlanacip']) + \
                       '&wlanacname=' + str(get_par['wlanacname']) + \
                       '&vlanid=' + str(get_par['vlanid']) + \
                       '&ip=' + str(get_par['wlanuserip']) + \
                       '&ssid=' + str(get_par['ssid']) + \
                       '&areaID=' + str(get_par['areaID']) + \
                       '&mac=' + str(get_par['mac'])
    real_url = real_url_head_str + real_url_par_str
    login_headers["Referer"] = real_url
    post_par["wlanuserip"] = get_par["wlanuserip"]
    post_par["wlanacip"] = get_par["wlanacip"]
    post_par["ip"] = get_par["ip"]
    r_url_head = "http://10.168.6.10:801/eportal/?c=ACSetting&a=Login&protocol=http:"
    r_url_par = "&hostname=" + post_par["hostname"] + "&iTermType=" + post_par["iTermType"] + \
                "&wlanuserip=" + post_par["wlanuserip"] + "&wlanacip=" + post_par["wlanacip"] + \
                "&mac=" + post_par["mac"] + "&ip=" + post_par["ip"] + \
                "&enAdvert=" + post_par["enAdvert"] + "&queryACIP=" + post_par["queryACIP"] + \
                "&loginMethod=" + post_par["loginMethod"]
    r_url = r_url_head + r_url_par

    return r_url
def set_login_data():
    """
    配置登录信息
    :return:
    """
    ini_data = []
    for i in range(3):
        if i == 0:
            ini_data.append(input("请输入上网账号："))
        if i == 1:
            ini_data.append(input("请输入上网密码："))
        if i == 2:
            t = input("请输入运营商:\n联通【1】\n移动【2】\n单宽【3】\n")
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
def get_login_data():
    """
    读取配置信息
    :return:
    """
    temp = []
    try:
        f = open(file_path)
        for line in f.readlines():
            temp.append(line.strip('\n'))
        f.close()
        return temp
    except IOError:
        print("login_data.ini 文件找不到")
        return []
    pass
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
def open_wifi():
    """
    dos命令打开wifi并链接校园网
    :return:
    """
    os.system('netsh wlan connect name=zzuli-student')
    time.sleep(1)

def login(temp_url, temp_data, temp_headers):
    """
    提交登录信息，并测试是否链接到网络
    :param temp_url: url
    :param temp_data: post数据包
    :param temp_headers: 请求头
    :return: 真假
    """
    requests.post(temp_url, data=temp_data, headers=temp_headers)
    time.sleep(1)
    if is_net_ok():
        return True
    else:
        requests.post(temp_url, data=temp_data, headers=temp_headers)
        time.sleep(1)
        return is_net_ok()
    pass

def word():
    """
    工具说明
    :return: 
    """
    print("=====================================================================")
    print("使用说明：")
    print("1.本程序放在磁盘任意文件夹内")
    print("2.右键发送快捷方式到桌面")
    print("3.以管理员打开程序，配置账号")
    print("4.下次使用直接双击即可")
    print("注意：")
    print("1.首次启动请使用管理员方式启动程序，因为生成配置文件需要权限。")
    print("2.配置完成后目录下会生成login_data.ini文件谨慎删除，删除需要重新配置")
    print("3.配置信息有误删除login_data.ini文件后重新配置即可")
    print("=====================================================================")

if __name__ == '__main__':
    print("======================Auto Login ZZULI Net V1.3======================\n")
    print("                                           by:mmciel 761998179@qq.com\n")
    word()
    if os.access(file_path, os.F_OK):
        print("正在读取配置文件...")
    else:
        print("请按要求配置登录信息：\n")
        set_login_data()
        print("配置成功！正在进行登录操作...")

    if is_net_ok():
        print("网络已连接...2s后程序关闭")
        time.sleep(2)
    else:
        try:
            open_wifi()
        except Exception as e:
            print("wifi启动失败，请检查权限或驱动程序是否符合条件！")
            time.sleep(2)
        login_data = get_login_data()

        flag = False

        # 获取url
        URL = get_url()

        # 这里是由于不知道R6参数的含义，只能反复提交参数，有一个能命中就行了
        for i in range(len(dynamic_R6_data)):
            print("正在尝试登录参数：R" + dynamic_R6_data[i])

            user_post["DDDDD"] = "," + dynamic_R6_data[i] + "," + login_data[0] + "@" + login_data[2]
            user_post["upass"] = login_data[1]
            user_post["R6"] = dynamic_R6_data[i]

            if login(URL, user_post, login_headers):
                flag = True
                break
            else:
                continue

        if flag:
            print("联网成功！ 1秒后关闭程序...")
            time.sleep(2)
        else:
            print("联网失败！ 1秒后关闭程序...")
            time.sleep(2)
pass