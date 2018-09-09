from socket import *
import time
import sys
import hashlib
import pygame

HOST = '127.0.0.1'
PORT = 18065
ADDR = (HOST,PORT)

class Client(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    def jiami(self,pwd):
        hash3 = hashlib.md5(bytes('e',encoding="utf-8"))
        hash3.update(bytes(pwd,encoding='utf-8'))
        return hash3.hexdigest()

    def do_login(self):
        while True:
            name = input('请输入姓名:')
            if name == "##":
                return
            elif not name or (' ' in name) or ('^' in name) \
                 or (not 5<len(name)<20):
                print("格式错误")
                continue
            passwd = input("请输入密码:")

            if not passwd or ("^" in passwd) or \
               (" " in passwd) or (not 5<len(passwd)<20):
                print('格式错误')
                continue
            elif passwd == "##":
                return
            passwd = self.jiami(passwd)
            msg = "L^{}^{}".format(name,passwd)
            self.sockfd.send(msg.encode())
            print(1111111)
            data = self.sockfd.recv(1024).decode()
            if data == "OK":
                print('注册成功')
                return name
            else:
                print(data)

    def do_register(self):
        while True:
            name = input("请输入姓名:")
            passwd = input("请输入密码:")
            if name == "##" or passwd =="##":
                return
            passwd = self.jiami(passwd)
            msg = "R^"+ name + "^" + passwd
            self.sockfd.send(msg.encode())
            data = self.sockfd.recv(128).decode()
            if data == "OK":
                print("登录成功")
                return name
            else:
                print(data)

    def do_query_msg(self,name):
        msg = "M^" + name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if not data:
            print("查询出错了")
        else:
            List = data.split("^")
            print("用户名 :", name)
            print("活跃度 :", List[1])
            print("金币 :", List[2])
            print("游戏场次:", List[3])
            print("胜场 :",List[4],"负场 :",List[5])
            print("积分 :", List[6])
            print("段位 :", List[7])


    def do_query_friend(self,name):
        msg = "F^" + name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data =="Faile":
            print("没有更多好友")
        else:
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == "##":
                    print("获取好友列表完成")
                    break
                List = data.split("^")
                print(List)
    
    def do_sendmail(self,name):
        friend = input("请选择接收方>>")
        message = input("请输入消息>>")
        if len(message) > 200:
            print("消息太长，只能发送２００字以内")
        msg = "S^" + name + "^" + friend + "^" + message
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == "Faile":
            print("邮件发送失败，可能是用户不存在")
        else:
            print(data)
        
    def do_recvmail(self,name):
        msg = "C^" +name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        # print(data)
        if data == "NONE":
            print("没有邮件")
        elif data == "OK":
            print("开始接收邮件")
            while True:
                data = self.sockfd.recv(1024).decode()
                if data =="##":
                    break
                List = data.split("^")
                # print(List)
                print(List[0] +" 发来邮件 "+ " : " + List[1] + "  时间 ： " + List[2])
    
    def do_add_friend(self,name):
        add_friend = input("请输入添加的好友名>>")
        if add_friend == name:
            print("不能添加自己为好友")
            return
        msg = "A^" + name + "^" +add_friend
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        if data =="Faile":
            print("添加的好友不存在")
        elif data == "OK":
            print("好友添加成功")

    def do_drop_friend(self,name):
        drop_friend = input("请选择要删除的好友")
        msg = "D^" + name +"^" + drop_friend
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            print("删除成功")
        else:
            print(data)

    def do_recharge(self,name):
        pass

    def zhuxiao(self,name):
        print("注销")
        msg = "B^" + name
        self.sockfd.send(msg.encode())
        print("注销完成")



    def second_menu(self,name):
        while True:
            print("""
                1. 开始游戏
                2. 查询信息
                3. 好友信息
                4. 积分充值(不实现)
                5. 设置
                6. 注销
                """)
            try:
                cmd = int(input("请选择>>"))
            except ValueError:
                print("错误命令")
            except KeyboardInterrupt:
                self.zhuxiao(name)
                print("退出当前登录")
                return

            except:
                continue

            if cmd == 1:
                print("哈哈,没有充钱，就不让你玩")
            elif cmd ==2:
                self.do_query_msg(name)
            elif cmd == 3:
                self.third_menu(name)
            elif cmd == 4:
                print("想充钱，再等等吧")
                # self.do_recharge()
            elif cmd == 5:
                self.do_setting()
            elif cmd == 6:
                self.zhuxiao(name)
                print("退出当前登录")
                return
    def third_menu(self,name):
        while True:
            print("""
                1. 显示好友
                2. 发送邮件
                3. 查看邮件
                4. 添加好友
                5. 删除好友
                6. 返回
                """)
            try:
                cmd = int(input("请选择>>"))
            except ValueError:
                print("命令错误")
                continue
            except KeyboardInterrupt:
                print("退出好友界面")
                return
            except: 
                continue
            if cmd == 1:
                self.do_query_friend(name)
            elif cmd == 2:
                self.do_sendmail(name)
            elif cmd == 3:
                self.do_recvmail(name)
            elif cmd == 4:
                self.do_add_friend(name)
            elif cmd ==5:
                self.do_drop_friend(name)
            elif cmd == 6:
                break

    def do_bgm(self):
        pygame.init()
        track = pygame.mixer.music.load("bgm.ogg")
        pygame.mixer.music.play(-1)
    def do_setting(self):
        while True:
            print("""
                1. 关闭背景音乐
                2. 开启背景音乐
                3. 设置音量
                4. 返回
                """)
            try:
                cmd = int(input("选择命令>>"))
                if cmd == 1:
                    pygame.mixer.music.stop()
                    print("暂停背景音乐")
                elif cmd == 2:
                    self.do_bgm()
                    # pygame.mixer.music.unpause()
                    # pygame.mixer.music.rewind()
                    print("继续播放背景音乐")
                elif cmd == 3:
                    S = float(input("请输入一个0-1的数>>"))
                    pygame.mixer.music.set_volume(S)
                    v = pygame.mixer.music.get_volume()
                    print(v)
                    print("音量设置为",S)
                elif cmd == 4:
                    return

            except ValueError:
                print("错误命令")
            except KeyboardInterrupt:
                break
                print("退出设置")
            except:
                continue
def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    user = Client(sockfd)
    user.do_bgm()
    while True:
        try:
            print("""
                1.注册
                2.登录
                3.设置
                4.退出
                """)
            cmd = int(input("请选择>>"))
            if cmd == 1:
                name = user.do_login()
                if name:
                    user.second_menu(name)
            elif cmd == 2:
                print(2222222)
                name = user.do_register()
                if name:
                    user.second_menu(name)
            elif cmd == 4:
                msg = "E^bye" 
                sockfd.send(msg.encode())
                sys.exit("客户端退出")
            elif cmd == 3:
                user.do_setting()
        except KeyboardInterrupt:
            msg = "E^bye"
            sockfd.send(msg.encode())
            print("谢谢使用")
            sys.exit("Bye")
        except ValueError:
            print("错误命令")



if __name__ == "__main__":
    main()