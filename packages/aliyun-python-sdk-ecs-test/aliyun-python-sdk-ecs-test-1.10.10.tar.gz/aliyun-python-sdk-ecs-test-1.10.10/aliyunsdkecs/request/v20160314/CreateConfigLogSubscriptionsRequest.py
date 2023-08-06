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
class CreateConfigLogSubscriptionsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2016-03-14', 'CreateConfigLogSubscriptions')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_Subscriptions(self):
		return self.get_query_params().get('Subscriptions')

	def set_Subscriptions(self,Subscriptions):
		for i in range(len(Subscriptions)):	
			if Subscriptions[i].get('Name') is not None:
				self.add_query_param('Subscription.' + str(i + 1) + '.Name' , Subscriptions[i].get('Name'))
			if Subscriptions[i].get('ResourceType') is not None:
				self.add_query_param('Subscription.' + str(i + 1) + '.ResourceType' , Subscriptions[i].get('ResourceType'))
			if Subscriptions[i].get('MnsQueueArn') is not None:
				self.add_query_param('Subscription.' + str(i + 1) + '.MnsQueueArn' , Subscriptions[i].get('MnsQueueArn'))


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