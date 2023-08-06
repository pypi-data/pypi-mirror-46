'''
Created by auto_sdk on 2018.07.26
'''
from top.api.base import RestApi
class TmallMeiCrmMemberSyncRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.extend = None
		self.level = None
		self.mix_nick = None
		self.mobile = None
		self.nick = None
		self.point = None
		self.version = None

	def getapiname(self):
		return 'tmall.mei.crm.member.sync'
