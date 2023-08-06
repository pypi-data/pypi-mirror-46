# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class ModifyFCTriggerRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Rds', '2014-08-15', 'ModifyFCTrigger')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_TriggerId(self):
		return self.get_query_params().get('TriggerId')

	def set_TriggerId(self,TriggerId):
		self.add_query_param('TriggerId',TriggerId)

	def get_SubscriptionObjectss(self):
		return self.get_query_params().get('SubscriptionObjectss')

	def set_SubscriptionObjectss(self,SubscriptionObjectss):
		for i in range(len(SubscriptionObjectss)):	
			if SubscriptionObjectss[i] is not None:
				self.add_query_param('SubscriptionObjects.' + str(i + 1) , SubscriptionObjectss[i]);

	def get_SecurityToken(self):
		return self.get_query_params().get('SecurityToken')

	def set_SecurityToken(self,SecurityToken):
		self.add_query_param('SecurityToken',SecurityToken)

	def get_EventFormat(self):
		return self.get_query_params().get('EventFormat')

	def set_EventFormat(self,EventFormat):
		self.add_query_param('EventFormat',EventFormat)

	def get_Retry(self):
		return self.get_query_params().get('Retry')

	def set_Retry(self,Retry):
		self.add_query_param('Retry',Retry)

	def get_TriggerArn(self):
		return self.get_query_params().get('TriggerArn')

	def set_TriggerArn(self,TriggerArn):
		self.add_query_param('TriggerArn',TriggerArn)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_Concurrency(self):
		return self.get_query_params().get('Concurrency')

	def set_Concurrency(self,Concurrency):
		self.add_query_param('Concurrency',Concurrency)

	def get_InvocationRoleArn(self):
		return self.get_query_params().get('InvocationRoleArn')

	def set_InvocationRoleArn(self,InvocationRoleArn):
		self.add_query_param('InvocationRoleArn',InvocationRoleArn)

	def get_FunctionArn(self):
		return self.get_query_params().get('FunctionArn')

	def set_FunctionArn(self,FunctionArn):
		self.add_query_param('FunctionArn',FunctionArn)