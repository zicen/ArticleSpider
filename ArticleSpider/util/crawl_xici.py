#coding=utf8

import requests


class GetIP(object):
    def judge_ip(self):
        httpurl = "http://www.baidu.com"
        proxy_url = "http://118.190.95.35:9001"
        try:
            proxy_dict={
                "http":proxy_url,
            }
            requests.get(httpurl,proxies = proxy_dict)
            print("success")
        except Exception as e:
            print("invalid ip and port")
            print(e)


if __name__ == '__main__':
    GetIP().judge_ip()