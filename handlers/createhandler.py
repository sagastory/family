#!/usr/bin/env Python
# coding=utf-8

import tornado.web
from basehandler import BaseHandler
import os
import commands
import MySQLdb
import uuid
import tornado.escape as es
import time



class addFinishHandler(BaseHandler):
    def post(self):
        #print self.request.body
        returndic={'status':'success'}
        static_pic_path= os.path.join(self.application.settings['static_path'], 'pic')

        fid = self.get_argument("fid")
        userid=self.get_secure_cookie("userid")
        
        pids = self.get_arguments("pid")
        pnames = self.get_arguments("pname")
        prelations = self.get_arguments("relationship")
        pbdays = self.get_arguments("pbirthday")
        photos = self.get_arguments("photo")

        matrixA = [pids,pnames,prelations,pbdays,photos]
        lines = zip(*matrixA)

        #print lines

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        #update personinfo
        for line in lines:
            #print line[0]
            filestr = line[4].split("/")           
            img_name=filestr[len(filestr)-1]
            #print img_name

            if (line[0] != '0'):
                sql = "update persons set pname='"+line[1]+"', birthday='"+line[3]+"', pphoto='"+img_name+"', relationship='"+line[2]+"' where pid='"+line[0]+"'"
            else:
                pid = str(uuid.uuid1())
                createid=''
                if(line[2]=='我'):createid=userid
                sql = "insert into persons (pid,fid,relationship,upid,pname,birthday,pphoto,createtime) value('"+pid+"','"+fid+"','"+line[2]+"','"+createid+"','"+line[1]+"','"+line[3]+"','"+img_name+"',now())"

            cur.execute(sql)
            conn.commit()

            #move head photo
            temp_head_path=os.path.join(static_pic_path, 'upload/'+fid)
            family_head_path=os.path.join(static_pic_path, fid)

            commands.getoutput("cp -f "+temp_head_path+"/*.png "+family_head_path)
            commands.getoutput("rm -fr "+temp_head_path)

        #update complete num
        sql = "select count(*) from persons where fid='"+fid+"' and upid <>'0'"
        cur.execute(sql)
        notnullnum=cur.fetchone()
        #print notnullnum[0]

        sql = "select count(*) from persons where fid='"+fid+"'"
        cur.execute(sql)
        allnum=cur.fetchone()
            #print allnum[0]

        if allnum[0]:
            completenum=int(notnullnum[0])*100/int(allnum[0])
                #print completenum
            sql = "update familys set completenum='"+str(completenum)+"' where fid='"+fid+"'"
            cur.execute(sql)
            conn.commit()

        cur.close()
        conn.close()

        self.write(es.json_encode(returndic))

        return

class addMemberHandler(BaseHandler):
    def post(self):
        createtype=self.get_argument("cmd")

        static_pic_path= os.path.join(self.application.settings['static_path'], 'pic')
        
        if(createtype=='create'):
            print("create family:")
            fid = str(uuid.uuid1())
            print fid
        else:
            print("add member:")
            fid = self.get_argument("fid")
            print fid

        msgid=str(uuid.uuid1())
        userid=self.get_secure_cookie("userid")

        file_metas = self.request.files.get('file', None)
        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        returndic={'status':'fail'}

        meta = file_metas[0]
        if meta:
            filename = meta['filename']
            rfpath = fid+'/ablum'
            to_path = os.path.join(static_pic_path, rfpath)

            if not os.path.exists(to_path):
                os.makedirs(to_path)
            
            file_path = os.path.join(to_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])

            #insert pic data
            sql = "insert into pictures (fid,mid,pname,createid,createtime) values('"+fid+"','"+msgid+"','"+filename+"','"+userid+"',now())"
            cur.execute(sql)
            conn.commit()

            sql = "insert into messages (mid,fid,userid,txt,createtime) values ('"+msgid+"','"+fid+"','"+userid+"','添加了相片',now())"
            cur.execute(sql)
            conn.commit()

            tfpath = fid+'/ablum/'+fid
            temp_file_path=os.path.join(static_pic_path, tfpath)
            

            if not os.path.exists(temp_file_path):
                os.makedirs(temp_file_path)
             
            commands.getoutput("cp -f "+file_path+" "+temp_file_path)

            detect_out_path=os.path.join(static_pic_path, 'upload')
            detect_src_path =  os.path.join(static_pic_path, fid+'/ablum')
            
            a,b = commands.getstatusoutput("python /home/naba/git-pro/facenet/src/align/align_dataset_mtcnn.py "+detect_src_path+" "+detect_out_path+" --detect_multiple_faces true")

            if(a==0):
                temp_out_file_path=os.path.join(static_pic_path, 'upload/'+fid)
                piclist = os.listdir(temp_out_file_path)

                
                dirlist=[]
                for pic in piclist:
                    pic='/static/pic/upload/'+fid+'/'+pic
                    dirlist.append(pic)

                returndic['pic']=dirlist
                returndic['status']="success"
                returndic['fid']=fid
                returndic['fphoto'] = filename

                
            else:
                print("failed for align")

        commands.getoutput("rm -fr "+temp_file_path)
        #print returndic
        self.write(es.json_encode(returndic))

        cur.close()
        conn.close()

        return

class writeTxtHandler(BaseHandler):
    def post(self):
        #print self.request.body
        mid=self.get_argument("mid")
        fid = self.get_argument("fid")
        txt = self.get_argument("txt")
        userid=self.get_secure_cookie("userid")

        #insert pic data
        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        sql = "insert into messages (mid,fid,txt,userid,createtime) values('"+mid+"','"+fid+"','"+txt+"','"+userid+"',now())"
        cur.execute(sql)
        conn.commit()

        cur.close()
        conn.close()
        return


class writeMsgHandler(BaseHandler):
    def post(self):
        #print self.request.body
        #print("write msg:")
        msgid=self.get_argument("evid")
        fid = self.get_argument("fid")
        userid=self.get_secure_cookie("userid")

        static_pic_path= os.path.join(self.application.settings['static_path'], 'pic')

        file_metas = self.request.files.get('file', None)
        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        for meta in file_metas:
            filename = meta['filename']
            rfpath = fid+'/ablum/'+filename
            file_path = os.path.join(static_pic_path, rfpath)
            

            with open(file_path, 'wb') as up:
                up.write(meta['body'])

            #insert pic data
            sql = "insert into pictures (fid,mid,pname,createid,createtime) values('"+fid+"','"+msgid+"','"+filename+"','"+userid+"',now())"
            cur.execute(sql)
            conn.commit()

        cur.close()
        conn.close()

        return

class writeCommentHandler(BaseHandler):
    def post(self):
        #print self.request.body
        mid=self.get_argument("mid")
        fid = self.get_argument("fid")
        txt=self.get_argument('con')
        userid=self.get_secure_cookie("userid")

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")    #连接对象
        cur = conn.cursor()    #游标对象

        #insert comments
        sql = "insert into comments (mid,userid,txt,createtime) values('"+mid+"','"+userid+"','"+txt+"',now())"
        cur.execute(sql)
        conn.commit()

        sql = "select pname,pphoto from persons where fid='"+fid+"'  and upid='"+userid+"'"

        cur.execute(sql)
        person = cur.fetchone()

        newcomm=['0',userid,txt,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),person[0],person[1]]

        cur.close()
        conn.close()

        self.write(es.json_encode(newcomm))

        return



class CreateHandler(BaseHandler):
    def get(self):

        self.render("create.html")

    def post(self):
        #ret = {'result': 'OK'}
        #print self.request.body
        returndic={'status':'success'}

        static_pic_path= os.path.join(self.application.settings['static_path'], 'pic')

        fid = self.get_argument("fid")
        fname = self.get_argument("fname")
        ftxt = self.get_argument("ftxt")
        fdate = self.get_argument("fdate")
        fphoto = self.get_argument("fphoto")
        userid=self.get_secure_cookie("userid")
        
        pids = self.get_arguments("pid")
        pnames = self.get_arguments("pname")
        prelations = self.get_arguments("relationship")
        pbdays = self.get_arguments("pbirthday")
        photos = self.get_arguments("photo")

        matrixA = [pids,pnames,prelations,pbdays,photos]
        lines = zip(*matrixA)

        #print lines

        conn = MySQLdb.connect(host=self.application.settings['dbhost'], user=self.application.settings['dbuser'], passwd=self.application.settings['dbpasswd'],db=self.application.settings['dbname'], port=3306, charset="utf8")   #连接对象
        cur = conn.cursor()    #游标对象

        #create family data
        sql = "insert into familys (fid,fname,ftxt,createid,createtime,fmainpic) value('"+fid+"','"+fname+"','"+ftxt+"','"+userid+"', now(), '"+fphoto+"')"
        #set fname='"+fname+"',ftxt='"+ftxt+"' where fid='"+fid+"'"
        print sql
        cur.execute(sql)
        conn.commit()

        #update personinfo
        for line in lines:
            #print line[0]
            filestr = line[4].split("/")           
            img_name=filestr[len(filestr)-1]

            pid = str(uuid.uuid1())
            createid=''
            if(line[2]=='我'):createid=userid
            sql = "insert into persons (pid,fid,relationship,upid,pname,birthday,pphoto,createtime) value('"+pid+"','"+fid+"','"+line[2]+"','"+createid+"','"+line[1]+"','"+line[3]+"','"+img_name+"',now())"

            #print sql
            cur.execute(sql)
            conn.commit()
           
            if line[3]:
                eid = str(uuid.uuid1())
                txt=line[1]+'诞生于'+line[3]
                sql="insert into events (eid,fid,userid,txt,eventtime,createtime,etype) values ('"+eid+"','"+fid+"','"+userid+"','"+txt+"','"+ line[3]+"',now(), 1)"
                cur.execute(sql)
                conn.commit()

            #move head photo
            temp_head_path=os.path.join(static_pic_path, 'upload/'+fid)
            family_head_path=os.path.join(static_pic_path, fid)

            commands.getoutput("cp -f "+temp_head_path+"/*.png "+family_head_path)
            commands.getoutput("rm -fr "+temp_head_path)

        #create events
        eid = str(uuid.uuid1())
        sql = "insert into events (eid,fid,userid,txt,eventtime,createtime,etype) values ('"+eid+"','"+fid+"','"+userid+"','创建了家庭"+fname+"', now(),now(), 0)"
        cur.execute(sql)
        conn.commit()

        #update complete num
        sql = "select count(*) from persons where fid='"+fid+"' and upid <>'0'"
        cur.execute(sql)
        notnullnum=cur.fetchone()
        #print notnullnum[0]

        sql = "select count(*) from persons where fid='"+fid+"'"
        cur.execute(sql)
        allnum=cur.fetchone()
        #print allnum[0]

        if allnum[0]:
            completenum=int(notnullnum[0])*100/int(allnum[0])
            #print completenum
            sql = "update familys set completenum='"+str(completenum)+"' where fid='"+fid+"'"
            cur.execute(sql)
            conn.commit()


        cur.close()
        conn.close()

        self.write(es.json_encode(returndic))

        return

   