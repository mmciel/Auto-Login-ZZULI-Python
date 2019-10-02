import requests
base_url = "http://www.msftconnecttest.com/redirect"
base_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": "www.msftconnecttest.com",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "zh-CN,zh;q=0.9"
}
print(requests.get(url=base_url,headers = base_headers).text)