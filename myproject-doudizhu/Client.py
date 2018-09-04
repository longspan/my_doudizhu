from socket import *
import time
import sys

HOST = '127.0.0.1'
PORT = 18065
ADDR = (HOST,PORT)

class Client(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_login(self):
        while True:
            name = input('请输入姓名:')
            if not name or (' ' in name) or ('^' in name):
                print("格式错误")
                continue
            elif name == "##":
                return
            passwd = input("请输入密码:")
            if not passwd or ("^" in passwd) or (" " in passwd):
                print('格式错误')
                continue
            elif passwd == "##":
                return
            msg = "注册^{}^{}".format(name,passwd)
            self.sockfd.send(msg.decode())
            data = self.sockfd.recv(1024).decode()
            if data == "OK":
                print('注册成功')
                return
            else:
                print(data)
                continue



def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    user = Client(sockfd)
    while True:
        try:
            print("""
                1.注册
                2.登录
                3.退出
                """)
            cmd = int(input("请选择>>"))
            if cmd == 1:
                user.do_login()
            elif cmd == 2:
                user.do_register()
            elif cmd == 3:
                sys.exit("客户端退出")
        except KeyboardInterrupt:
            print("谢谢使用")


if __name__ == "__main__":
    main()