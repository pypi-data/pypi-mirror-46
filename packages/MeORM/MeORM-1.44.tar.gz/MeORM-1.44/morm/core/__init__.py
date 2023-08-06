
import os

from mt import lu
log=lu.getLogger("MeORM")

root_path=os.path.dirname(os.path.dirname(__file__))
config_path=os.sep.join([root_path,"config"])
test_path=os.sep.join([root_path,"test"])


#
from collections import namedtuple
Rule =namedtuple("Rule",['tablename','support','keys'])

def upcasefirst(str_):
	return str_[0].upper()+str_[1:]


def lowcasefirst(str_):
	return str_[0].lower()+str_[1:]




def get_connect_config():

	from ._gen import Gen
	from .dbhelper import DBHelper
	config=Gen.get_config()

	if config is None:
		config=DBHelper.get_config_template()

		Gen.log("--------------")
		Gen.log("正通过模板方法['get_config_template']连接库.")
		Gen.log("--------------")
		Gen.log("获得模板数据为=> ",config)


	return config


