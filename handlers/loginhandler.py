#!/usr/bin/env Python
# coding=utf-8

import tornado.web
from basehandler import BaseHandler
import os
import commands
import MySQLdb

class InvoteHandler(BaseHandler):
    def get(self, fid,phone):
        #print fid
        #print phone
        return
    
    def post(self):
        fid = self.get_argument("fid")
        phone = self.get_argument("phone")
        targetpid = self.get_argument("targetpid")
        invotepid = self.get_argument("invotepid")
        invotename = self.get_argument("invotename")

        #print fid
        #print phone
        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")  # 连接对象

        cur = conn.cursor()  # 游标对象

        sql = "insert into invotes (fid,targetpid,targetphone,invotepid,invotepname,createtime) value ('"+fid+"','"+targetpid+"','"+phone+"','"+invotepid+"','"+invotename+"', now())"

        cur.execute(sql)
        conn.commit()


        cur.close()
        conn.close()
        return

class PersonHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, pid):
        #print self.request.headers
        userid = self.get_secure_cookie("userid")

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")  # 连接对象

        cur = conn.cursor()  # 游标对象

        sql = "select a.fid, a.upid, a.relationship, a.pphoto, a.birthday,a.pname,b.fname,b.createtime,b.completenum,a.pid from persons a,familys b where a.fid=b.fid and a.pid='"+pid+"'"

        cur.execute(sql)
        pinfo=cur.fetchone()

        #判断是否有权利访问该用户身份
        sql = "select pid,pname from persons where upid='"+userid+"' and fid='"+pinfo[0]+"'"
        cur.execute(sql)

        user_code = cur.fetchone()
        if not user_code:
            cur.close()
            conn.close()
            #print ("no right!")
            
            if 'referer' in self.request.headers.keys():
                self.redirect(self.request.headers['referer'])
            else:
                self.redirect('/')

        userinfo = [userid,user_code[0],user_code[1]]

        #uid=str(pinfo[1])
        #if not pinfo[1]:

         #   sql = "select b.fid, b.fname, b.createtime,b.completenum from persons a, familys b where a.fid=b.fid and a.pid='"+pid+"'"
        #else:
         #   sql = "select b.fid, b.fname, b.createtime,b.completenum from persons a, familys b where a.fid=b.fid and a.upid='"+uid+"'"
            
        #cur.execute(sql)
        #lines=cur.fetchall()
        #print sql

        #familylist = []

        sql = "select pid, pname,pphoto from persons where fid='"+pinfo[0]+"'"
        cur.execute(sql)

        persons = cur.fetchall()

        sql = "select upid from persons where upid<>'0' and fid='"+pinfo[0]+"'"
        cur.execute(sql)
        users=cur.fetchall()
            
        familyinfo=[pinfo[0],persons,users]
        #familylist.append(familyinfo)

        cur.close()
        conn.close()
        self.render("person.html",currentuser=userinfo,person=pinfo,family=familyinfo)


class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        
        self.redirect("/")


class LoginHandler(BaseHandler):
    def get(self):
        
        print self.application.settings['static_path']
        #picpath = "/home/naba/git-pro/netfamily/statics/pic/upload"
        self.set_secure_cookie("next", self.get_argument('next', '/'))
        #print self.get_argument('next', '/')
        #piclist = os.listdir(picpath)
        # print(piclist)
        self.render("login.html")

    def post(self):
        type = self.get_argument('type')

        if(type == 'register'):
            name = self.get_argument('name')
            email = self.get_argument('email')
            passwd = self.get_argument('passwd')

            conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")  # 连接对象

            cur = conn.cursor()  # 游标对象

            sql = "insert into users (uname,email,passwd) values ('" + \
                name+"','"+email+"','"+passwd+"')"

            cur.execute(sql)
            conn.commit()

            cur.close()
            conn.close()
            self.render("login.html")
        else:
            name = self.get_argument('name')
            passwd = self.get_argument('passwd')

            conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")  # 连接对象

            cur = conn.cursor()  # 游标对象

            sql = "select uid,uname,pid from users where uname='" + \
                name+"' and passwd='"+passwd+"'"

            cur.execute(sql)
            line = cur.fetchone()

            if line:
                self.set_secure_cookie("userid", str(line[0]))
                self.set_secure_cookie("user", line[1])
                #self.set_secure_cookie("person", line[2] if line[2] else "")
                #self.redirect("/")
                
                self.redirect(self.get_secure_cookie("next"))
            else:
                self.render("login.html")

            cur.close()
            conn.close()
