from socket import *
from select import *
from signal import *
import time
import sys
import database
import hashlib
d = database.Mydatabase()

HOST= '0.0.0.0'
PORT = 18065
ADDR= (HOST,PORT)

class Server(object):
    def __init__(self,c):
        self.c = c

    def jiami(self,pwd):
        hash3 = hashlib.md5(bytes('e',encoding='utf-8'))
        hash3.update(bytes(pwd,encoding='utf-8'))
        return hash3.hexdigest()

    def do_login(self,Lst,user_dict):
        print(333333)
        name = Lst[1]
        passwd = Lst[2]
        print(passwd)
        # passwd = str(self.jiami(passwd))
        # print(passwd)
        # print(type(passwd))
        shoujihao = '18888888888'
        nicheng = 'xxxxxx'
        if d.check_usrexist(name):
            print(44444)
            d.insert_user(name,passwd,nicheng,shoujihao)
            print("用户注册成功")
            self.c.send(b"OK")
            user_dict[name] = self.c
        else:
            print("用户注册失败")
            self.c.send("用户名已经存在".encode())

    def do_register(self,Lst,user_dict):
        print(1234567)
        name = Lst[1]
        passwd = Lst[2]
        if d.check_login(name,passwd) == 0:
            print(self.c.getpeername(),"用户登录失败")
            self.c.send("密码或用户错误".encode())
        elif d.check_login(name,passwd) == 1:
            print(self.c.getpeername(),'登录成功')
            self.c.send(b"OK")
            user_dict[name] = self.c
            count = d.check_loign_count(name) +1
            print(count)
            d.user_login(count,name)
            print(888999)


    def do_query_msg(self,Lst):
        name = Lst[1]
        #获取登录次数
        count = d.check_loign_count(name)
        print(count)
        #获取用户活跃度
        vitality = d.check_vitality(name)
        print(vitality)
        #获取用户金币
        user_gold = d.check_gold(name)
        print(user_gold)
        #获取用户的游戏场次，胜负场次
        user_changci = d.count_changci(name)
        print(user_changci)
        #总场次
        total1 = user_changci[0]
        #胜场
        win_c = user_changci[1]
        #负场
        lose_c = user_changci[2]
        user_changci = str(total1) + "^" + str(win_c) + "^" + str(lose_c)
        #获取用户积分,段位
        integral = d.check_integr_level(name)
        print(integral)
        #积分
        integral1 = integral[0]
        #段位
        level = integral[1]

        integral = str(integral1) + "^" +str(level)
        
        msg = str(count) + "^" +str(vitality) +"^" +str(user_gold)  +"^" + \
                   user_changci + "^" + integral
        print(msg)
        self.c.send(msg.encode())

    def do_query_friend(self,Lst):
        name = Lst[1]
        try:
            friends = d.query_friend(name)
            if not friends:
                self.c.send(b"Faile")
                return
            else:
                self.c.send(b"OK")
        except:
            self.c.send("数据查询失败".encode())

        for friend in friends:
            print(friend)
            #获取用户活跃度
            vitality = str(d.check_vitality(name))
            #获取用户金币
            user_gold = str(d.check_gold(name))
            #获取用户积分,段位
            integral = d.check_integr_level(name)
            # print(integral)
            #积分
            integral1 = integral[0]
            #段位
            level = integral[1]

            integral = str(integral1) + "^" +str(level)
            msg = friend[0] + "^" +  vitality + "^" +user_gold +"^" + integral
            print(msg)
            self.c.send(msg.encode())
        time.sleep(0.1)
        self.c.send(b"##")
        print("完成")



    def do_add_friend(self,Lst):
        name = Lst[1]
        add_friend = Lst[2]
        if d.check_usrexist(add_friend) ==0:
            print("可以添加")

            d.add_friend(name,add_friend)
            print("添加成功")
            self.c.send(b"OK")
        else:
            print("该用户名不存在")
            self.c.send(b"Faile")
    def do_drop_friend(self,Lst):
        name = Lst[1]
        drop_friend = Lst[2]
        try:
            d.drop_friend(name,drop_friend)
            self.c.send(b"OK")
            print('删除成功')
        except Exception as e:
            print(e)
            self.c.send("错误".encode())

    def do_sendmail(self,Lst,user_dict):
        send_name = Lst[1]
        recv_name = Lst[2]
        message = Lst[3]
        datetime = time.ctime()
        if d.check_usrexist == 0:
            self.c.send(b"Faile")
        elif recv_name in user_dict:
            msg = send_name + "^" + message + "^" +datetime
            user[recv_name].send(msg.encode())
            self.c.send(b"OK")
        else:
            d.add_mail(recv_name,send_name,message,datetime)
            self.c.send("邮件以缓存".encode())
    
    def do_recvmail(self,Lst):
        recv_name = Lst[1]
        message = d.recv_mail(recv_name)
        print(message)
        if not message:
            self.c.send(b"NONE")
            return
        else:
            self.c.send(b"OK")
        for m in message:
            msg = m[0] + "^" +m[1] +"^" + m[2]
            self.c.send(msg.encode())
        print("邮件发送完毕")
        time.sleep(0.1)
        self.c.send(b"##")




def main():
    #字典用来存储登录在线的用户
    user_dict = {}
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
        for fd,event in events:
            if fd == sockfd.fileno():
                c,addr = dic_map[fd].accept()
                CL = Server(c)
                print("Connect from ",addr)
                #将c添加关注
                p.register(c,EPOLLIN)
                #维护地图
                dic_map[c.fileno()] = c
                print(222222)
            else:
                print(11111)
                data = dic_map[fd].recv(2048).decode()
                print(data)
                if not data:
                    p.unregister(fd)
                    dic_map[fd].close()
                    del dic_map[fd]
                    continue

                Lst = data.split("^")
                print(Lst)
                if len(Lst) >1 :
                    for i in Lst:
                        if  i[0] == "L":
                            #注册
                            CL.do_login(Lst,user_dict)
                        elif i[0]== "R":
                            #登录
                            CL.do_register(Lst,user_dict)
                        elif i[0] == 'P':
                            #开始游戏
                            CL.do_dizhu(Lst,user_dict)
                        elif i[0] =="M":
                            #查询信息
                            CL.do_query_msg(Lst)
                        elif i[0] =="F":
                            #查询好友列表
                            CL.do_query_friend(Lst)
                        elif i[0] == "A":
                            #添加好友
                            CL.do_add_friend(Lst)
                        elif i[0] == "D":
                            #删除好友
                            CL.do_drop_friend(Lst)
                        elif i[0] == "S":
                            #发送邮件
                            CL.do_sendmail(Lst,user_dict)
                        elif i[0] == "C":
                            #收邮件
                            CL.do_recvmail(Lst)
                        elif i[0] =='E':
                            print("客户端退出")
                            p.unregister(fd)
                            dic_map[fd].close()
                            del dic_map[fd]






if __name__ =="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("服务器退出")
        sys.exit("Bye")