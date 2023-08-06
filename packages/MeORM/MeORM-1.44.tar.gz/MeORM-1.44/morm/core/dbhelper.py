#!/usr/bin/env python
# -*- coding: utf-8 -*
# @Date    : 2019-04-12 09:56:01
# @Author  : Blackstone
# @to      :

# coding=utf-8
import re
import time
import logging
import os
import cx_Oracle
import traceback
from . import Rule,get_connect_config,log


class DBHelper:

    _connect_pool={}
    _timeout=28800#8小时

    def __init__(self,config_path=None):

        self.config=get_connect_config()


        if not isinstance(self.config,dict):
            raise TypeError("config是字典=>",self.config)


  

    def _db_connect(self):

        

        log.debug("----------------------")
        log.debug("----尝试连接数据库-----")
        log.debug("----------------------")

        try:



            self.dbtype=self.config["dbtype"]
            self.dbname=self.config["dbname"]
            #oracle不需要这两项
            self.host=self.config["host"]
            self.port=self.config["port"]
            self.user=self.config["username"]
            self.pwd=self.config["password"]


            key="+".join([self.dbtype,self.dbname,str(self.host),str(self.port),self.user,str(self.pwd)])

            log.debug("数据库类型=>%s"%self.dbtype)

            log.debug("数据库名=>%s"%self.dbname)
            log.debug("数据库地址(仅mysql|db2)=>%s|%s"%(self.host,self.port))
            log.debug("数据库账号=>%s|%s"%(self.user,self.pwd))

            self.conn=self._connect_pool.get(key)

            need_connect=False

            if  self.conn  is not None:
                try:
                    self.conn.ping()
                except:
                    need_connect =True
            else:
                need_connect=True

             
            if need_connect==True:
                if self.dbtype.lower()=='mysql':
                    import pymysql
                  
                    self.conn = pymysql.connect(db=self.dbname, host=self.host,
                                                port=int(self.port),
                                                user=self.user,
                                                password=str(self.pwd),
                                                charset='utf8mb4',
                                                connect_timeout=self._timeout)

                elif self.dbtype.lower()=='oracle':
                    self.conn =cx_Oracle.connect(self.user+'/'+self.pwd+'@'+self.dbname)

                elif self.dbtype.lower()=='db2':
                    import ibm_db_dbi
                    self.conn = ibm_db_dbi.connect("PORT="+str(self.port)+";PROTOCOL=TCPIP;", 
                                                   user=self.user,
                                                   password=self.pwd, 
                                                   host=self.host, 
                                                   database=self.dbname)

                self._connect_pool[key]=self.conn


            log.debug("连接成功,获得=>%s"%self.conn)
           


        except cx_Oracle.DatabaseError:
            raise RuntimeError("配置不正确")

    def _db_commit(self):
        try:
            if self.conn:
                self.conn.commit()
        except:
            pass


    def db_close():
        try:
            [con.close() for con in DBHelper._connect_pool.values()]
         
        except  Exception as ee:
            log.debug(ee)

            raise DBError('关闭数据库连接出现异常，请确认')

                
    def db_execute(self, sql,error="ignore-"):

        res=0

        log.debug("执行sql=>%s"%sql)

        self._db_connect()
        cursor=self.conn.cursor()

        try:
            res=cursor.execute(sql)

            if not sql.split()[0].lower().startswith("select"):
                self.conn.commit()

            if sql.split()[0].lower().startswith("select"):
                res=cursor.fetchall()

        except Exception as e:
            if error=='ignore':
                return res

            log.debug("出现异常=>"+str(e))
            traceback.print_exc()

            # raise RuntimeError("sql执行结果报错.")
        finally:

            cursor.close()
            if isinstance(res,int):
                log.debug("执行结果=>%s(生效行数)"%(res,))
            else:
                log.debug("执行结果=>%s"%(res,))  
            log.debug("\n\n")

            return res
        #return sqlresult

  
    @classmethod
    def get_config_template(cls):
        return {

        'dbtype':'mysql',
        'dbname':'auto',
        'host':'127.0.0.1',
        'port':3306,
        'username':'root',
        'password':123456


        }



        

    @classmethod
    def get_dao_gen_rule(cls):
        pass


 
class DBError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__=="__main__":
    
    data={
    'dbtype':'mysql',
    'dbname':'auto',
    'host':'127.0.0.1',
    'port':'3306',
    'password':"123456",
    'username':'root',
    'password':'123456'

    }


    h=DBHelper(data)
    res=h.db_execute("select * from device")


