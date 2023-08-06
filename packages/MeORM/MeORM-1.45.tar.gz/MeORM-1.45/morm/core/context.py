#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-25 13:40:44
# @Author  : Blackstone
# @to      :
from contextlib import contextmanager
import os,sys

from warnings import warn
from . import log


class context(object):
	_service_map={}

	_ready=False#true才能注册
	_ok=False#ok才能获取


	@classmethod
	def _set_ready(cls,bool_=None):

		if bool_ is None:
			cls._ready=True

		else:
			cls._ready=bool_



	@classmethod
	def _is_ready(cls):
		return cls._ready


	@classmethod
	def _is_ok(cls):
		return cls._ok

	@classmethod
	def _set_ok(cls):
		cls._ok=True



	@classmethod
	def getService(cls,name):

		if not cls._is_ok():
			return

		serivce=cls._service_map.get(name,None)
		if serivce is None:
			# raise KeyError("通过[%s]查询服务实例 实例不存在."%name)
			pass

		log.debug("通过[名称-%s]获取到服务实例=>  %s"%(name,serivce))

		return serivce


	@classmethod
	def register_service(cls,name,service):

		if not cls._is_ready():
			return

		log.debug("注册服务实例%s 名称=%s"%(service,name))
		old=cls._service_map.get(name)
		if old is not None:
			warn("服务名已被注册=>%s"%name)

		cls._service_map[name]=service

	@classmethod
	def init(cls,service_root=None):
		"""
		service_root:服务发现位置 默认init调用模块平行目录

		"""

		if service_root is None:
			service_root=os.path.dirname(sys._getframe(1).f_code.co_filename)

		print("---------------")


		log.debug("=============容器开始初始化...")

	


		res=cls._scan_service(service_root)

		cls._set_ready()
		#烧苗结束 注册服务
		for m in res:
			try:
				log.debug("载入服务模块=> %s "%m)
				__import__(m)
			except ImportError as e:
				log.error("容器初始化失败..")
				log.error("%s处未发现模块 %s，载入失败."%(__file__,service_root))

				log.error(str(e))

				return

		cls._set_ready(False)

		cls._set_ok()

		log.debug("==========容器初始化结束..\n")


		#可以获取服务

	@classmethod
	def _scan_service(cls,path,*args,**kw):

		def _scan(file_path):
			#print("file=>",file_path,os.path.isdir(file_path))

			abspath=os.path.abspath(file_path)

			#print("full_name=>",file_path)

			if os.path.isdir(file_path):

				package_sep.append(os.path.splitext(file_path)[0].split(os.sep)[-1])

				#print("package_sep=>",package_sep)

				for f in os.listdir(file_path) :
					
					full_name=abspath+os.sep+f

					if full_name.__contains__("service"):
						_scan(full_name)

				#
				package_sep.clear()
				
			else:
				ext=os.path.splitext(file_path)[-1]
				#print("ext=>",ext)


				packagename=".".join(package_sep)

				modulename=os.path.splitext(file_path)[0].split(os.sep)[-1]

				if ext==".py":
					result.append(packagename+"."+ modulename)


		#_scan_path=(lambda path:os.path.dirname(__file__) if path is None else path)(path)

		log.debug("开始serivce扫描.")
		log.debug("扫描位置 => %s"%path)

		result=[]

		package_sep=[]

		_scan(path)
		result=[".".join(x.split(".")[1:]) for x in result]
		log.debug("扫描结果 =>%s"%result)

		if len(result)==0:
			log.debug("未发现任何可载入的服务 请检查配置.")

		return result



if __name__=="__main__":

	context.init(r"C:\Users\F\Desktop\test")
	
	#print(dot_name_to_object("."))

