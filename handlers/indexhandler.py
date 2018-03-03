#!/usr/bin/env Python
# coding=utf-8

import tornado.web
from basehandler import BaseHandler
import os
import tornado.escape as es
import MySQLdb

static_pic_path="/home/naba/git-pro/netfamily/statics/pic/upload"

class GetrelaHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        userid = self.get_secure_cookie("userid")

        nodes=[]
        edges=[]

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        sql = "select fid,pid from persons where upid='"+userid+"' order by createtime"
        cur.execute(sql)
        lines= cur.fetchall()

        for line in lines:
            sql="select pid from persons where fid='"+line[0]+"' and relationship='我'"
            cur.execute(sql)
            creator = cur.fetchone()

            sql="select pid,pname,relationship,pphoto,fid,upid from persons where fid='"+line[0]+"'"
            cur.execute(sql)
            persons=cur.fetchall()

            for person in persons:
                
                node={'id':person[0],'label':person[1], 'shape':'circularImage','image':'/static/pic/'+person[4]+'/'+person[3],'group':person[4]}
                nodes.append(node)
 
                if str(person[5])==str(userid) and person[0] != lines[0][1]:
                    edge={'from':person[0],'to':lines[0][1],'label':'我'}
                    edges.append(edge)

                if person[2] != '我':
                    edge={'from':person[0],'to':creator[0],'label':person[2]}
                    edges.append(edge)

        returndic=[nodes,edges]

        self.write(es.json_encode(returndic))
        return

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        userid = self.get_secure_cookie("userid")

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象
        sql = "select a.fid,c.fname,c.ftxt from persons a, familys c where a.upid='"+userid+"' and c.fid=a.fid"
        cur.execute(sql)

        lines = cur.fetchall()
        #print lines

        persondict={}
        
        for line in lines:
            sql="select pid,pphoto from persons where fid='"+line[0]+"'"
            cur.execute(sql)

            persondict[line[0]]=cur.fetchall()       

            

        cur.close()
        conn.close()
                
        self.render("index.html",user=userid,familys=lines,persons=persondict)

    #@tornado.web.authenticated
    def post(self):
        cmd = self.get_argument("cmd")
        tmpf = self.get_argument("tmpf")
        
        #print(family)
        #password = self.get_argument("password")
        #user_infos = mrd.select_table(table="users",column="*",condition="uname",value=username)
        picpath = os.path.join(static_pic_path,tmpf)
        piclist = os.listdir(picpath)

        returndic={}
        dirlist=[]
        for pic in piclist:
            pic='static/pic/upload/'+tmpf+'/'+pic
            dirlist.append(pic)

        returndic['pic']=dirlist
        if (cmd=="create"):
            #self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(es.json_encode(dirlist)) 
        elif(cmd=="Add"):
            family = self.get_argument("family")

            conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
            cur = conn.cursor()    #游标对象

            sql = "select pid, pphoto,relationship from persons  where fid='"+family+"'"
            cur.execute(sql)

            lines=cur.fetchall()

            cur.close()
            conn.close()

            returndic['member'] = lines

            #print returndic
            
            self.write(es.json_encode(returndic))
            return

        else:
            #self.write("There is no thi user.")
            raise tornado.web.HTTPError(404)
    
    def put(self):
        userid = self.get_secure_cookie("userid")

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象
        sql = "select fid from persons where upid='"+userid+"'"
        cur.execute(sql)

        lines = cur.fetchall()

        sql = "select a.mid, a.fid, a.userid, a.txt,date_format(a.createtime,'%Y-%m-%d %H:%i'),b.pname,b.pphoto,d.fname,b.pid from messages a,persons b,familys d where d.fid=a.fid and b.upid = a.userid and a.fid=b.fid and a.fid in ( select fid from persons where upid='"+userid+"') order by a.createtime desc"
        
        #print sql
        cur.execute(sql)
        fmsgs=cur.fetchall()

        mesglist=[]

            #get msg recomments and photos
        for msg in fmsgs:
            sql = "select picid,pname from pictures where fid='"+msg[1]+"' and mid='"+msg[0]+"'"
            cur.execute(sql)
            msgpics = cur.fetchall()

            sql = "select a.cid, a.userid,a.txt,date_format(a.createtime,'%Y-%m-%d %H:%i'),b.pname,b.pphoto from comments a,persons b  where a.userid=b.upid and b.fid='"+msg[1]+"' and  a.mid='"+msg[0]+"' order by a.createtime desc"
            cur.execute(sql)
            mesgcomments = cur.fetchall()
            #print mesgcomments

            mesglist.append([msg,msgpics,mesgcomments])
        
        self.write(es.json_encode(mesglist))

        cur.close()
        conn.close()
        return