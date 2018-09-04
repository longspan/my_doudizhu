from socket import *
from select import *
from signal import *
import time
import sys
import database
d = database.Mydatabase()

HOST= '0.0.0.0'
PORT = 18065
ADDR= (HOST,PORT)

class Server(object):
    def __init__(self,c):
        self.c = c

    def do_login(self,Lst):
        name = Lst[1]
        passwd = Lst[2]
        shoujihao = '18888888888'
        nicheng = 'xxxxxx'
        if d.check_usrexist(name):
            d.insert_user(name,passwd,shoujihao,nicheng)
            print("用户注册成功")
            self.c.send(b"OK")
        else:
            print("用户注册失败")
            self.send("用户名已经存在")







def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    #创建地图
    dic_map = {sockfd.fileno():sockfd}
    #创建epool对象
    p = epoll()
    #将sockfd加入到关注
    p.register(sockfd,EPOLLIN|EPOLLERR)
    while True:

        events = p.poll()
        for event,fd in events:
            if fd == sockfd.fileno():
                c,addr = dic_map[fd].accept()
                print("Connect from ",addr)
                #将c添加关注
                p.register(c,EPOLLERR)
                #维护地图
                dic_map[c.fileno()] = c
            elif fd ==c.fileno():
                data = dic_map[fd].recv(2048).decode()
                print(data)
                if not data:
                    p.unregister(fd)
                    dic_map[fd].close()
                    del dic_map[fd]
                Lst = data.split("^")
                print(Lst)
                for i in Lst:
                    if  i[0] == "注册":
                        do_login(Lst)
                    elif i[0]== "登录":
                        do_register()
                    elif i[0] == '地主':
                        do_dizhu()
                    elif i[0] =="查询":
                        do_select()
                    elif i[0] =='退出':
                        print("客户端退出")
                        p.unregister(fd)
                        dic_map[fd].close()
                        del dic_map[fd]






if __name__ =="__main__":
    main()