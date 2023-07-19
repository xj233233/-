import requests


def proxy(url: str):
    # 提取代理API接口，获取1个代理IP
    api_url = url

    # 获取API接口返回的代理IP
    proxy_ip = requests.get(api_url).text

    # 用户名密码认证(私密代理/独享代理)
    username = ""
    password = ""
    proxies = {
        "http": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
        "https": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    }
    return proxies

