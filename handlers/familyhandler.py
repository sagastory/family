#!/usr/bin/env Python
# coding=utf-8

import tornado.web
from basehandler import BaseHandler
import os
import MySQLdb
import tornado.escape as es

picpath = "/home/naba/git-pro/netfamily/statics/pic/upload"

class FamilyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,fid):
        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        sql = "select fid,fname,ftxt,createid,fmainpic,completenum from familys where fid='"+fid+"'"
        cur.execute(sql)

        line = cur.fetchone()

        cur.close()
        conn.close()

        if not line: raise tornado.web.HTTPError(404)

        #piclist = os.listdir(picpath)
        #print mesglist
        self.render("family.html",user=self.current_user,family=line)

    def post(self):
        fid = self.get_argument("fid")
        cmd = self.get_argument("cmd")
        #print cmd

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        if(cmd=="getmesgs"):
            #find family messages
            sql = "select a.mid, a.fid, a.userid, a.txt,date_format(a.createtime,'%Y-%m-%d %H:%i'),b.pname,b.pphoto,b.pid from messages a,persons b where b.upid = a.userid and a.fid=b.fid and a.fid='"+fid+"' order by a.createtime desc"
            #print sql
            cur.execute(sql)       

            messages = cur.fetchall()

            mesglist=[]

            for message in messages:
                #mesg pics
                sql = "select picid,pname from pictures where fid='"+fid+"' and mid='"+message[0]+"'"
                cur.execute(sql)
                msgpics = cur.fetchall()

                #mesg comments date_format(time, '%Y%m%d%H%i%s')
                sql = "select a.cid, a.userid,a.txt,date_format(a.createtime, '%Y-%m-%d %H:%i'),b.pname,b.pphoto from comments a,persons b where a.userid=b.upid and b.fid='"+fid+"' and a.mid='"+message[0]+"' order by a.createtime desc"
                cur.execute(sql)
                mesgcomments = cur.fetchall()

                mesglist.append([message,msgpics,mesgcomments])

            self.write(es.json_encode(mesglist))

        elif(cmd=="getevents"):
            #events list
            sql = "select a.eid,a.txt,date_format(a.createtime,'%Y-%m-%d %H:%i'),a.etype,b.pname,b.pphoto,a.fid from events a, persons b where a.userid=b.upid and b.fid=a.fid and a.fid='"+fid+"'"

            cur.execute(sql)
            eventlist = cur.fetchall()
            #print eventlist
            eventpiclist=[]
            for event in eventlist:
                sql = "select pname from pictures where eid='"+event[0]+"'"
                cur.execute(sql)
                piclines = cur.fetchall()
                eventpiclist.append([event,piclines])

            self.write(es.json_encode(eventpiclist))

        elif(cmd=="getpics"):
            #ablum pics
            sql="select picid,fid,pname from pictures where fid='"+fid+"'"
            cur.execute(sql)
            ablumpics=cur.fetchall()

            self.write(es.json_encode(ablumpics))
        
        elif(cmd=="getpersons"):
            sql="select pid, relationship, pphoto,pname,date_format(birthday,'%Y-%m-%d') from persons where fid='"+fid+"'"
            cur.execute(sql)
            persons=cur.fetchall()

            personlist=[]
            for person in persons:
                #print person
                personlist.append([person[0],person[1],'/static/pic/'+fid+'/'+person[2],person[3],person[4]])
                #person[2] = '/static/pic/'+fid+'/'+person[2]
            
            self.write(es.json_encode(personlist))

        cur.close()
        conn.close()

        return
        