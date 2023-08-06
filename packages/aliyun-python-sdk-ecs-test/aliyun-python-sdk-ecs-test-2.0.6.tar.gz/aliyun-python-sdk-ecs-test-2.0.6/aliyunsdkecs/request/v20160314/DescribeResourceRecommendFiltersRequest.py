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
class DescribeResourceRecommendFiltersRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2016-03-14', 'DescribeResourceRecommendFilters')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_AttributeValue(self):
		return self.get_query_params().get('AttributeValue')

	def set_AttributeValue(self,AttributeValue):
		self.add_query_param('AttributeValue',AttributeValue)

	def get__Global(self):
		return self.get_query_params().get('Global')

	def set__Global(self,_Global):
		self.add_query_param('Global',_Global)

	def get_AttributeName(self):
		return self.get_query_params().get('AttributeName')

	def set_AttributeName(self,AttributeName):
		self.add_query_param('AttributeName',AttributeName)

	def get_TemplateTags(self):
		return self.get_query_params().get('TemplateTags')

	def set_TemplateTags(self,TemplateTags):
		for i in range(len(TemplateTags)):	
			if TemplateTags[i].get('Key') is not None:
				self.add_query_param('TemplateTag.' + str(i + 1) + '.Key' , TemplateTags[i].get('Key'))
			if TemplateTags[i].get('Value') is not None:
				self.add_query_param('TemplateTag.' + str(i + 1) + '.Value' , TemplateTags[i].get('Value'))


	def get_Product(self):
		return self.get_query_params().get('Product')

	def set_Product(self,Product):
		self.add_query_param('Product',Product)

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

	def get_ResourceType(self):
		return self.get_query_params().get('ResourceType')

	def set_ResourceType(self,ResourceType):
		self.add_query_param('ResourceType',ResourceType)

	def get_RegionNo(self):
		return self.get_query_params().get('RegionNo')

	def set_RegionNo(self,RegionNo):
		self.add_query_param('RegionNo',RegionNo)

	def get_MaxItems(self):
		return self.get_query_params().get('MaxItems')

	def set_MaxItems(self,MaxItems):
		self.add_query_param('MaxItems',MaxItems)