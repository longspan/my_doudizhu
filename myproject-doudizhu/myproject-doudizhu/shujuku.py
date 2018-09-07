 create database gamehall;

 create table user(
    userid int primary key auto_increment,
    username varchar(20) not null unique,
    password varchar(50) not null,
    user_nicheng varchar(20) not null,
    telnum char(11),
    login_count int default 1)default charset=utf8;

 create table game(
    uid int,
    username varchar(20),
    total_count int default 0,
    win_count int default 0,
    lose_count int default 0,
    integration int default 0,
    level_flag tinyint default 0,
    gold int default 1000,
    vitality int default 100,
    expression_flag tinyint default 0,
    winerstreak_falg tinyint default 0,
    foreign key(username)
    references user(username)
    on update cascade
    on delete cascade)default charset=utf8;

