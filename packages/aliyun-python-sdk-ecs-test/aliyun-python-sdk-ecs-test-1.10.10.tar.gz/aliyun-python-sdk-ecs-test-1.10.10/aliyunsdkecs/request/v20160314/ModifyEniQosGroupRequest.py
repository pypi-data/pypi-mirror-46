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
class ModifyEniQosGroupRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2016-03-14', 'ModifyEniQosGroup')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_Tx(self):
		return self.get_query_params().get('Tx')

	def set_Tx(self,Tx):
		self.add_query_param('Tx',Tx)

	def get_Rx(self):
		return self.get_query_params().get('Rx')

	def set_Rx(self,Rx):
		self.add_query_param('Rx',Rx)

	def get_RxPps(self):
		return self.get_query_params().get('RxPps')

	def set_RxPps(self,RxPps):
		self.add_query_param('RxPps',RxPps)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_QosGroupName(self):
		return self.get_query_params().get('QosGroupName')

	def set_QosGroupName(self,QosGroupName):
		self.add_query_param('QosGroupName',QosGroupName)

	def get_TxPps(self):
		return self.get_query_params().get('TxPps')

	def set_TxPps(self,TxPps):
		self.add_query_param('TxPps',TxPps)