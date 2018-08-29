#!/usr/bin/env python3
#添加可执行权限chmod 775 dict_server.py
#coding=utf-8
'''
name : Lixiao
data  : 2018-5-30
modules ：python3.5 mysql pymysql
This is a dict project for AID
'''
from socket import *
from multiprocessing import Process
from time import sleep,ctime
import sys ,os
from signal import *
import pymysql

DICT_TEXT = "./dict.txt"
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)


def do_child(c,db):
    while True:
        data = c.recv(1024).decode()
        print("Request:",data)
        if (not data) or data[0] =="E":
            c.close()
            print('客户端退出')
            sys.exit(0)
        elif data[0] =='R':
            do_register(c,db,data)
        elif data[0] == "L":
            do_login(c,db,data)
        elif data[0] =="Q":
            do_query(c,db,data)
        elif data[0] == "H":
            do_history(c,db,data)

def do_history(c,db,data):
    name = data.split(' ')[1]
    cursor = db.cursor()

    try:
        sql = "select * from hist where name='%s';"%name
        curcor.execure(sql)
        r = cursor.fetchall()
        if not r:
            c.send("没有历史记录".encode())
            return
        else:
            c.send(b'OK')
    except:
        print("Error")
        c.send("数据库查询错误".encode())
    n = 0
    for i in r:
        n +=1
        if n>10:
            break
        sleep(0.1)
        msg = "%s     %s     %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    sleep(0.1)
    c.send(b'##')


def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = ctime()
        sql = "insert into hist (name,word,time) \
                    values('%s','%s','%s');"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
            print("插入成功")
        except:
            print("Error")
            db.rollback
            return

    try:
        f = open(DICT_TEXT,'rb')
    except:
        c.send("500 服务端异常".decode())
        return
    while True:
        line = f.readline().decode()
        w = line.split(" ")[0]
        if (not line) or w > word:
            c.send("没找到该单词".encode())
            break
        elif w ==word:
            c.send(b"OK")
            sleep(0.1)
            c.send(line.encode())
            insert_history()
            break
    f.close()





def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name='%s' and \
                   passwd= '%s';"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r ==None:
        c.send('用户名或密码不正确'.encode())
    else:
        c.send(b"OK")

def do_register(c,db,data):
    l = data.split(' ')
    print(l)
    name = l[1]
    passwd = l[2]

    cursor = db.cursor()
    sql  = "select * from user where name='%s';"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    print(r)
    if r != None:
        c.send(b'EXISTS')
        print("EXISTS")
        return
    sql = "insert into user(name,passwd)\
                   values('%s','%s');"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b"OK")
        print("OK")
    except:
        db.rollback()
        c.send(b"FALL")
        print("FALL")
        return
    else:
        print("%s注册成功"%name)


#主控制流程
def main():
    #连接数据库
    db = pymysql.connect('localhost','root','123456','dictionary')

    #创建流式套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR) 
    sockfd.listen(5)
#忽略子进程退出
    signal(SIGCHLD,SIG_IGN)
    

    while True:
        try:
            c,addr = sockfd.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #创建子进程处理客户端请求
        pid = os.fork()
        if pid ==0:
            sockfd.close()
            do_child(c,db)
        else:
            c.close()



if __name__ == "__main__":
    main()