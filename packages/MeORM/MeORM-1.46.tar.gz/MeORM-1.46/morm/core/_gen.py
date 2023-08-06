#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-12 09:45:24
# @Author  : Blackstone
# @to      :

import yaml,datetime,os,sys,shutil
from collections import namedtuple
from . import log,config_path,test_path,root_path,upcasefirst,Rule,lowcasefirst

from .dbhelper import DBHelper
from  . import get_connect_config
import warnings


class Gen:

	_Debug=True
	_rulefile=None


	@classmethod
	def set_debug(cls,b):
		cls._Debug=b

	@classmethod
	def log(cls,*msg,**kw):
		if cls._Debug:

			level="Debug"

			v=kw.get("level",None)
			if v:level=v
			cur=str(datetime.datetime.now())[:19]

			msg="".join([str(x) for x in msg])
			print("%s-[%s][M-orm]-|| %s"%(cur,level,msg))


	@classmethod
	def gen(cls,dao_file=None,rule_file=None):

		cls._rulefile=rule_file

		if dao_file is None:
			dao_file=os.sep.join([get_desktop(),"dao"])

		else:
			if not os.path.isdir(dao_file):
				raise TypeError("path路径是一个目录")

			dao_file=os.sep.join([dao_file,"dao"])

		if os.path.exists(dao_file):
			shutil.rmtree(dao_file)  


		log.debug("----------------------")
		log.debug("----开始生成Dao=>[%s]-----"%dao_file)
		log.debug("----------------------")
		os.mkdir(dao_file)

		#__init__.py

		with open(os.sep.join([dao_file,"__init__.py"]),"w"):
			pass


		#

		map_=cls._gen_rules_code()

		for _ in map_:
			
			daofile=os.sep.join([dao_file,_])
			with open(daofile,"w") as f:
				f.write(map_[_])


		log.debug("--生成dao结束.")



	@classmethod
	def _gen_rules_code(cls):

		res={}
		path=""

		rules=cls.get_dao_rules()
		for rule in rules:

			code=""
			prefix="\n".join([
				"from Lib.decorator import bind_sql,insert,update,delete,select",
				"from Lib._gen import Gen",
				"from Lib.dbhelper import DBHelper"

				])

			tablename=rule.tablename
			support=rule.support
			keys=rule.keys
			for s in support:

				method_name=lowcasefirst(tablename)
				bind_sql=""
				arg_str=""


				keystr="keys='%s'"%keys

				if isinstance(keys,(tuple,list)):
					keystr="keys=%s"%keys



				if s=="insert":
					bind_sql="@insert(keys='%s')"%keys
					method_heard="def add_%s(%s)"%(method_name,arg_str)

				elif s=="delete":
					bind_sql="@delete(keys='%s')"%keys
					method_heard="def remove_%s(%s)"%(method_name,arg_str)

				elif s=="update":
					bind_sql="@update(keys='%s')"%keys
					method_heard="def update_%s(%s)"%(method_name,arg_str)

				elif s=="select":
					bind_sql="@select(keys='%s')"%keys
					method_heard="def query_%s(%s)"%(method_name,arg_str)


				code+="\t"+bind_sql+"\n\t"+method_heard+":\n\t\tpass"+"\n\n"

			#add bind_sql code
			bind_sql="@bind_sql('select * from tablename where param0={0}')"
			method_heard="def func(*params)"
			code+="\t"+bind_sql+"\n\t"+method_heard+":\n\t\tpass"+"\n\n"


			res[".".join([tablename,"py"])]=prefix+"\n\nclass %s(object)\n"%tablename+ code


		return res



	@classmethod
	def _read_config(cls,path=None):

		config_file=None

		if path:
			config_file=path

		else:
			config_file=os.sep.join([config_path,"connect.yaml"])

		if not os.path.exists(config_file):
			warnings.warn("配置文件[%s]不存在,尝试模板方法连接库."%config_file)
			return None


		with open(config_file) as f:
			cls.config=yaml.load(f.read())


			log.debug("----------------------")
			log.debug("---通过配置文件[%s]连接库-----"%config_file)
			log.debug("----------------------")

			log.debug(cls.config)
		
			return cls.config

	@classmethod
	def get_config(cls,path=None):
		return Gen._read_config(path) if not hasattr(Gen,"config") else cls.config



	@classmethod
	def get_dao_rules(cls):

		d=[]

		log.debug("----------------------")
		log.debug("----获取dao生成规则-----")
		log.debug("----------------------")

		if hasattr(Gen,"rules"):
			return cls.rules


		else:
			if cls._rulefile is None:
				cls._rulefile= os.sep.join([config_path,"dao_gen.yaml"])

			if not os.path.exists(cls._rulefile):
				warnings.warn("规则文件[%s]不存在"%cls._rulefile,RuntimeWarning)

			with open(cls._rulefile) as f:
				for r in yaml.load(f.read())["rules"]:
					#print("rule=>",r)
					rule=Rule(r["tablename"], r["support"], r["keys"])

					d.append(rule)


			cls.rules=d

			return cls.rules


	@classmethod
	def get_tabel_column_map(cls):
		d={}
		rules=cls.get_dao_rules()

		if isinstance(rules,list):

			for x in rules:
				d[x.tablename]=Gen._get_table_columns(x.tablename)


		else:
			d[set_.tablename]=Gen._get_table_columns(set_.tablename)



		return d

	@classmethod
	def get_table_keys(cls,tablename):

		rules= cls.get_dao_rules()

		for r in rules:
			if tablename==r.tablename:
				return r.keys


		warnings.warn("表[%s]没有配置keys"%tablename)


		return None


	


	@classmethod
	def _get_table_columns(cls,tablename):


		dbname=get_connect_config().get("dbname")
		sql="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"%(tablename,dbname)

		log.debug("查找表字段 =>",sql)
		h=dbhelper.DBHelper()
		res=h.db_execute(sql)

		return [x[0] for x in res]




def get_desktop():
	import winreg
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')#利用系统的链表
	return str(winreg.QueryValueEx(key, "Desktop")[0] )#返回的是Unicode类型数据


if __name__=="__main__":
	print(get_desktop())



