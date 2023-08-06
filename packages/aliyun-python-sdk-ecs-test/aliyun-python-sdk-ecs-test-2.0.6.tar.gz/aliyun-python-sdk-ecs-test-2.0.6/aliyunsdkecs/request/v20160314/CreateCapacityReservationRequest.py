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
class CreateCapacityReservationRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2016-03-14', 'CreateCapacityReservation')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_NetworkType(self):
		return self.get_query_params().get('NetworkType')

	def set_NetworkType(self,NetworkType):
		self.add_query_param('NetworkType',NetworkType)

	def get_ResourceGroupId(self):
		return self.get_query_params().get('ResourceGroupId')

	def set_ResourceGroupId(self,ResourceGroupId):
		self.add_query_param('ResourceGroupId',ResourceGroupId)

	def get_InstanceCount(self):
		return self.get_query_params().get('InstanceCount')

	def set_InstanceCount(self,InstanceCount):
		self.add_query_param('InstanceCount',InstanceCount)

	def get_InstanceType(self):
		return self.get_query_params().get('InstanceType')

	def set_InstanceType(self,InstanceType):
		self.add_query_param('InstanceType',InstanceType)

	def get_Tags(self):
		return self.get_query_params().get('Tags')

	def set_Tags(self,Tags):
		for i in range(len(Tags)):	
			if Tags[i].get('Key') is not None:
				self.add_query_param('Tag.' + str(i + 1) + '.Key' , Tags[i].get('Key'))
			if Tags[i].get('Value') is not None:
				self.add_query_param('Tag.' + str(i + 1) + '.Value' , Tags[i].get('Value'))


	def get_InstancePlatform(self):
		return self.get_query_params().get('InstancePlatform')

	def set_InstancePlatform(self,InstancePlatform):
		self.add_query_param('InstancePlatform',InstancePlatform)

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

	def get_EndDateType(self):
		return self.get_query_params().get('EndDateType')

	def set_EndDateType(self,EndDateType):
		self.add_query_param('EndDateType',EndDateType)

	def get_InstanceMatchCriteria(self):
		return self.get_query_params().get('InstanceMatchCriteria')

	def set_InstanceMatchCriteria(self,InstanceMatchCriteria):
		self.add_query_param('InstanceMatchCriteria',InstanceMatchCriteria)

	def get_TimeSlot(self):
		return self.get_query_params().get('TimeSlot')

	def set_TimeSlot(self,TimeSlot):
		self.add_query_param('TimeSlot',TimeSlot)

	def get_CapacityReservationName(self):
		return self.get_query_params().get('CapacityReservationName')

	def set_CapacityReservationName(self,CapacityReservationName):
		self.add_query_param('CapacityReservationName',CapacityReservationName)

	def get_ZoneId(self):
		return self.get_query_params().get('ZoneId')

	def set_ZoneId(self,ZoneId):
		self.add_query_param('ZoneId',ZoneId)