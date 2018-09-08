
#游戏库
create database gamehall;
#用户表
create table user(
    userid int primary key auto_increment,
    username varchar(20) not null unique,
    password varchar(50) not null,
    user_nicheng varchar(20) not null,
    telnum char(11),
    login_count int default 0)default charset=utf8;


#game表
create table game(
    uid int,
    username varchar(20),
    total_count int default 0,
    win_count int default 0,
    lose_count int default 0,
    integration int default 0,
    level_flag int default 0,
    gold int default 1000,
    vitality int default 100,
    expression_flag tinyint default 0,
    winerstreak_flag tinyint default 0,
    foreign key(username)
    references user(username)
    on update cascade
    on delete cascade)default charset=utf8;

#好友表
create table friends_list(
    f_id int primary key auto_increment,
    username varchar(20) ,
    friends_name varchar(20) not null,
    foreign key(username)
    references user(username)
    on update cascade
    on delete cascade)default charset=utf8;

#邮件暂存表
create table e_mail(
    e_id int primary key auto_increment,
    recv_name varchar(20),
    send_name varchar(20),
    message text,
    datetime varchar(30),
    foreign key(recv_name)
    references user(username)
    on update cascade
    on delete cascade)default charset=utf8;
    