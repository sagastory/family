create table familys(
    fid varchar(64) primary key,
    fname varchar(200),
    ftxt varchar(200),
    createid varchar(50),
    createname varchar(50),
    createtime datetime,
    fmainpic varchar(100),
    completenum int,
    isdel int 
)default charset=utf8;
--0 no  1 yes

create table persons(
    pid varchar(64) primary key,
    fid varchar(64),
    relationship varchar(64),
    upid int,
    pname varchar(50),
    birthday date,
    deadday date,
    pphoto varchar(100),
    sex int,
    phone varchar(50),
    wechat varchar(50),
    qq varchar(20),
    isdel int ,
    createtime datetime
)default charset=utf8;
--0 no  1 yes

create table users(
    uid int primary key not null auto_increment,
    pid varchar(64),
    uname varchar(50),
    passwd varchar(50),
    nickname varchar(50),
    phone varchar(50),
    email varchar(50),
    photo varchar(100),
    isvip int,   
    creattime datetime
)default charset=utf8;
--0 no 1 yes


create table personIntro(
    seq int primary key auto_increment,
    pid varchar(64),
    title varchar(100),
    content varchar(2000),
    createid int,
    createname varchar(50),
    createtime datetime,
    isdel int 
)default charset=utf8;
--0 no  1 yes

create table FP(
    fid varchar(64) not null,
    pid varchar(64) not null,
    PRIMARY KEY (fid,pid),
    fpname varchar(50),
    ptype int,   
    relationship varchar(64)  
)default charset=utf8;
-- 0 owner 1 直系  2 旁系
-- 0父  1母  2夫 3妻  4儿  5女  6祖父 7祖母 8兄 9弟 10姐 11妹 12外祖父 13外祖母 14孙 15孙女 16外孙 17外孙女 18女婿 19 儿媳 20叔 21伯 22姑 23姑父  24侄 25侄女 26岳父 27岳母 28舅 29姨 30外甥 31外甥女 32曾祖父 33曾祖母 34婶婶 35伯母 36嫂 37弟妹 38小舅 39姐夫 40曾孙 41曾外孙 42孙婿 43孙媳 44侄孙 45表兄弟 46表姐妹 47堂兄弟 48堂姐妹  99 我 100 爱人


create table pictures(
    picid int primary key not null auto_increment,
    fid varchar(64),
    mid varchar(64),
    eid varchar(64),
    paths varchar(100),
    pname varchar(100),
    createid varchar(50),
    createtime datetime,
    isdel int 
)default charset=utf8;
--0 no  1 yes

create table messages(
    mid varchar(64) primary key not null,
    fid varchar(64),
    userid int,
    txt varchar(1000),
    createname varchar(50),
    createtime datetime,
    likenum int default 0,
    isdel int 
)default charset=utf8;

create table events(
    eid varchar(64) primary key not null,
    fid varchar(64),
    userid int,
    txt varchar(1000),
    eventtime datetime,
    createname varchar(50),
    createtime datetime,
    etype int  
)default charset=utf8;
--etype 0 create 1 birthday 

create table comments(
    cid int primary key not null auto_increment,
    mid varchar(64),
    userid int,
    txt varchar(1000),
    createname varchar(50),
    createtime datetime,
    isdel int 
)default charset=utf8;

create table notifys(
    nid int primary key not null auto_increment,
    fid varchar(64),
    targetuser int,
    ntype int,  -- 0 申请加入
    txt varchar(1000),
    createid int,
    createtime datetime,
    isread int default 0  -- 0 not read
)default charset=utf8;

create table invotes(
    iid int primary key not null auto_increment,
    fid varchar(64),
    targetpid varchar(64),
    targetphone varchar(50),
    invotetxt varchar(500),
    invotepid varchar(64),
    invotepname varchar(50),
    createtime datetime
)default charset=utf8;
