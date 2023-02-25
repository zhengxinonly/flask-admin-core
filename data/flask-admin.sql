drop database if exists `flask_admin`;
create database `flask_admin` character set `utf8mb4`;

use `flask_admin`;

create table `ums_user`
(
    id            int primary key auto_increment,
    nickname      varchar(255) not null,
    username      varchar(255) not null,
    password_hash varchar(255) not null,
    no            char(6)      null
);

insert into `ums_user`
values (1,
        '正心',
        '正心全栈编程',
        'pbkdf2:sha256:260000$YYQ0IYwRgiHz23bv$4543b6e3887b7452cb1995cdb8fb67c53b7ee0429142f93fd980c1b89335ed56',
        null);
