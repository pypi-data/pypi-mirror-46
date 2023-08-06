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
class RunInstancesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ecs', '2016-03-14', 'RunInstances')

	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_UniqueSuffix(self):
		return self.get_query_params().get('UniqueSuffix')

	def set_UniqueSuffix(self,UniqueSuffix):
		self.add_query_param('UniqueSuffix',UniqueSuffix)

	def get_HpcClusterId(self):
		return self.get_query_params().get('HpcClusterId')

	def set_HpcClusterId(self,HpcClusterId):
		self.add_query_param('HpcClusterId',HpcClusterId)

	def get_SecurityEnhancementStrategy(self):
		return self.get_query_params().get('SecurityEnhancementStrategy')

	def set_SecurityEnhancementStrategy(self,SecurityEnhancementStrategy):
		self.add_query_param('SecurityEnhancementStrategy',SecurityEnhancementStrategy)

	def get_NetworkType(self):
		return self.get_query_params().get('NetworkType')

	def set_NetworkType(self,NetworkType):
		self.add_query_param('NetworkType',NetworkType)

	def get_KeyPairName(self):
		return self.get_query_params().get('KeyPairName')

	def set_KeyPairName(self,KeyPairName):
		self.add_query_param('KeyPairName',KeyPairName)

	def get_MinAmount(self):
		return self.get_query_params().get('MinAmount')

	def set_MinAmount(self,MinAmount):
		self.add_query_param('MinAmount',MinAmount)

	def get_SpotPriceLimit(self):
		return self.get_query_params().get('SpotPriceLimit')

	def set_SpotPriceLimit(self,SpotPriceLimit):
		self.add_query_param('SpotPriceLimit',SpotPriceLimit)

	def get_DeletionProtection(self):
		return self.get_query_params().get('DeletionProtection')

	def set_DeletionProtection(self,DeletionProtection):
		self.add_query_param('DeletionProtection',DeletionProtection)

	def get_ResourceGroupId(self):
		return self.get_query_params().get('ResourceGroupId')

	def set_ResourceGroupId(self,ResourceGroupId):
		self.add_query_param('ResourceGroupId',ResourceGroupId)

	def get_HostName(self):
		return self.get_query_params().get('HostName')

	def set_HostName(self,HostName):
		self.add_query_param('HostName',HostName)

	def get_Password(self):
		return self.get_query_params().get('Password')

	def set_Password(self,Password):
		self.add_query_param('Password',Password)

	def get_Tags(self):
		return self.get_query_params().get('Tags')

	def set_Tags(self,Tags):
		for i in range(len(Tags)):	
			if Tags[i].get('Value') is not None:
				self.add_query_param('Tag.' + str(i + 1) + '.Value' , Tags[i].get('Value'))
			if Tags[i].get('Key') is not None:
				self.add_query_param('Tag.' + str(i + 1) + '.Key' , Tags[i].get('Key'))


	def get_BusinessInfo(self):
		return self.get_query_params().get('BusinessInfo')

	def set_BusinessInfo(self,BusinessInfo):
		self.add_query_param('BusinessInfo',BusinessInfo)

	def get_NodeControllerId(self):
		return self.get_query_params().get('NodeControllerId')

	def set_NodeControllerId(self,NodeControllerId):
		self.add_query_param('NodeControllerId',NodeControllerId)

	def get_DryRun(self):
		return self.get_query_params().get('DryRun')

	def set_DryRun(self,DryRun):
		self.add_query_param('DryRun',DryRun)

	def get_FromApp(self):
		return self.get_query_params().get('FromApp')

	def set_FromApp(self,FromApp):
		self.add_query_param('FromApp',FromApp)

	def get_Ipv6AddressCount(self):
		return self.get_query_params().get('Ipv6AddressCount')

	def set_Ipv6AddressCount(self,Ipv6AddressCount):
		self.add_query_param('Ipv6AddressCount',Ipv6AddressCount)

	def get_MaxAmount(self):
		return self.get_query_params().get('MaxAmount')

	def set_MaxAmount(self,MaxAmount):
		self.add_query_param('MaxAmount',MaxAmount)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_CapacityReservationPreference(self):
		return self.get_query_params().get('CapacityReservationPreference')

	def set_CapacityReservationPreference(self,CapacityReservationPreference):
		self.add_query_param('CapacityReservationPreference',CapacityReservationPreference)

	def get_VSwitchId(self):
		return self.get_query_params().get('VSwitchId')

	def set_VSwitchId(self,VSwitchId):
		self.add_query_param('VSwitchId',VSwitchId)

	def get_SpotStrategy(self):
		return self.get_query_params().get('SpotStrategy')

	def set_SpotStrategy(self,SpotStrategy):
		self.add_query_param('SpotStrategy',SpotStrategy)

	def get_RecycleBinResourceId(self):
		return self.get_query_params().get('RecycleBinResourceId')

	def set_RecycleBinResourceId(self,RecycleBinResourceId):
		self.add_query_param('RecycleBinResourceId',RecycleBinResourceId)

	def get_InstanceName(self):
		return self.get_query_params().get('InstanceName')

	def set_InstanceName(self,InstanceName):
		self.add_query_param('InstanceName',InstanceName)

	def get_InternetChargeType(self):
		return self.get_query_params().get('InternetChargeType')

	def set_InternetChargeType(self,InternetChargeType):
		self.add_query_param('InternetChargeType',InternetChargeType)

	def get_ZoneId(self):
		return self.get_query_params().get('ZoneId')

	def set_ZoneId(self,ZoneId):
		self.add_query_param('ZoneId',ZoneId)

	def get_Ipv6Addresss(self):
		return self.get_query_params().get('Ipv6Addresss')

	def set_Ipv6Addresss(self,Ipv6Addresss):
		for i in range(len(Ipv6Addresss)):	
			if Ipv6Addresss[i] is not None:
				self.add_query_param('Ipv6Address.' + str(i + 1) , Ipv6Addresss[i]);

	def get_InternetMaxBandwidthIn(self):
		return self.get_query_params().get('InternetMaxBandwidthIn')

	def set_InternetMaxBandwidthIn(self,InternetMaxBandwidthIn):
		self.add_query_param('InternetMaxBandwidthIn',InternetMaxBandwidthIn)

	def get_Affinity(self):
		return self.get_query_params().get('Affinity')

	def set_Affinity(self,Affinity):
		self.add_query_param('Affinity',Affinity)

	def get_ImageId(self):
		return self.get_query_params().get('ImageId')

	def set_ImageId(self,ImageId):
		self.add_query_param('ImageId',ImageId)

	def get_ClientToken(self):
		return self.get_query_params().get('ClientToken')

	def set_ClientToken(self,ClientToken):
		self.add_query_param('ClientToken',ClientToken)

	def get_SpotInterruptionBehavior(self):
		return self.get_query_params().get('SpotInterruptionBehavior')

	def set_SpotInterruptionBehavior(self,SpotInterruptionBehavior):
		self.add_query_param('SpotInterruptionBehavior',SpotInterruptionBehavior)

	def get_IoOptimized(self):
		return self.get_query_params().get('IoOptimized')

	def set_IoOptimized(self,IoOptimized):
		self.add_query_param('IoOptimized',IoOptimized)

	def get_InternetMaxBandwidthOut(self):
		return self.get_query_params().get('InternetMaxBandwidthOut')

	def set_InternetMaxBandwidthOut(self,InternetMaxBandwidthOut):
		self.add_query_param('InternetMaxBandwidthOut',InternetMaxBandwidthOut)

	def get_SecurityGroupId(self):
		return self.get_query_params().get('SecurityGroupId')

	def set_SecurityGroupId(self,SecurityGroupId):
		self.add_query_param('SecurityGroupId',SecurityGroupId)

	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_SystemDiskCategory(self):
		return self.get_query_params().get('SystemDisk.Category')

	def set_SystemDiskCategory(self,SystemDiskCategory):
		self.add_query_param('SystemDisk.Category',SystemDiskCategory)

	def get_CapacityReservationId(self):
		return self.get_query_params().get('CapacityReservationId')

	def set_CapacityReservationId(self,CapacityReservationId):
		self.add_query_param('CapacityReservationId',CapacityReservationId)

	def get_UserData(self):
		return self.get_query_params().get('UserData')

	def set_UserData(self,UserData):
		self.add_query_param('UserData',UserData)

	def get_PasswordInherit(self):
		return self.get_query_params().get('PasswordInherit')

	def set_PasswordInherit(self,PasswordInherit):
		self.add_query_param('PasswordInherit',PasswordInherit)

	def get_InstanceType(self):
		return self.get_query_params().get('InstanceType')

	def set_InstanceType(self,InstanceType):
		self.add_query_param('InstanceType',InstanceType)

	def get_NetworkInterfaces(self):
		return self.get_query_params().get('NetworkInterfaces')

	def set_NetworkInterfaces(self,NetworkInterfaces):
		for i in range(len(NetworkInterfaces)):	
			if NetworkInterfaces[i].get('VSwitchId') is not None:
				self.add_query_param('NetworkInterface.' + str(i + 1) + '.VSwitchId' , NetworkInterfaces[i].get('VSwitchId'))
			if NetworkInterfaces[i].get('SecurityGroupId') is not None:
				self.add_query_param('NetworkInterface.' + str(i + 1) + '.SecurityGroupId' , NetworkInterfaces[i].get('SecurityGroupId'))
			if NetworkInterfaces[i].get('PrimaryIpAddress') is not None:
				self.add_query_param('NetworkInterface.' + str(i + 1) + '.PrimaryIpAddress' , NetworkInterfaces[i].get('PrimaryIpAddress'))
			if NetworkInterfaces[i].get('Description') is not None:
				self.add_query_param('NetworkInterface.' + str(i + 1) + '.Description' , NetworkInterfaces[i].get('Description'))
			if NetworkInterfaces[i].get('NetworkInterfaceName') is not None:
				self.add_query_param('NetworkInterface.' + str(i + 1) + '.NetworkInterfaceName' , NetworkInterfaces[i].get('NetworkInterfaceName'))


	def get_DeploymentSetId(self):
		return self.get_query_params().get('DeploymentSetId')

	def set_DeploymentSetId(self,DeploymentSetId):
		self.add_query_param('DeploymentSetId',DeploymentSetId)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_Tenancy(self):
		return self.get_query_params().get('Tenancy')

	def set_Tenancy(self,Tenancy):
		self.add_query_param('Tenancy',Tenancy)

	def get_SystemDiskDiskName(self):
		return self.get_query_params().get('SystemDisk.DiskName')

	def set_SystemDiskDiskName(self,SystemDiskDiskName):
		self.add_query_param('SystemDisk.DiskName',SystemDiskDiskName)

	def get_AutoReleaseTime(self):
		return self.get_query_params().get('AutoReleaseTime')

	def set_AutoReleaseTime(self,AutoReleaseTime):
		self.add_query_param('AutoReleaseTime',AutoReleaseTime)

	def get_RamRoleName(self):
		return self.get_query_params().get('RamRoleName')

	def set_RamRoleName(self,RamRoleName):
		self.add_query_param('RamRoleName',RamRoleName)

	def get_RelationOrderId(self):
		return self.get_query_params().get('RelationOrderId')

	def set_RelationOrderId(self,RelationOrderId):
		self.add_query_param('RelationOrderId',RelationOrderId)

	def get_DedicatedHostId(self):
		return self.get_query_params().get('DedicatedHostId')

	def set_DedicatedHostId(self,DedicatedHostId):
		self.add_query_param('DedicatedHostId',DedicatedHostId)

	def get_ClusterId(self):
		return self.get_query_params().get('ClusterId')

	def set_ClusterId(self,ClusterId):
		self.add_query_param('ClusterId',ClusterId)

	def get_CreditSpecification(self):
		return self.get_query_params().get('CreditSpecification')

	def set_CreditSpecification(self,CreditSpecification):
		self.add_query_param('CreditSpecification',CreditSpecification)

	def get_SecurityGroupIdss(self):
		return self.get_query_params().get('SecurityGroupIdss')

	def set_SecurityGroupIdss(self,SecurityGroupIdss):
		for i in range(len(SecurityGroupIdss)):	
			if SecurityGroupIdss[i] is not None:
				self.add_query_param('SecurityGroupIds.' + str(i + 1) , SecurityGroupIdss[i]);

	def get_DataDisks(self):
		return self.get_query_params().get('DataDisks')

	def set_DataDisks(self,DataDisks):
		for i in range(len(DataDisks)):	
			if DataDisks[i].get('DiskName') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.DiskName' , DataDisks[i].get('DiskName'))
			if DataDisks[i].get('SnapshotId') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.SnapshotId' , DataDisks[i].get('SnapshotId'))
			if DataDisks[i].get('Size') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.Size' , DataDisks[i].get('Size'))
			if DataDisks[i].get('Encrypted') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.Encrypted' , DataDisks[i].get('Encrypted'))
			if DataDisks[i].get('Description') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.Description' , DataDisks[i].get('Description'))
			if DataDisks[i].get('Category') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.Category' , DataDisks[i].get('Category'))
			if DataDisks[i].get('KMSKeyId') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.KMSKeyId' , DataDisks[i].get('KMSKeyId'))
			if DataDisks[i].get('Device') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.Device' , DataDisks[i].get('Device'))
			if DataDisks[i].get('DeleteWithInstance') is not None:
				self.add_query_param('DataDisk.' + str(i + 1) + '.DeleteWithInstance' , DataDisks[i].get('DeleteWithInstance'))


	def get_SecurityGroupRules(self):
		return self.get_query_params().get('SecurityGroupRules')

	def set_SecurityGroupRules(self,SecurityGroupRules):
		for i in range(len(SecurityGroupRules)):	
			if SecurityGroupRules[i].get('NicType') is not None:
				self.add_query_param('SecurityGroupRule.' + str(i + 1) + '.NicType' , SecurityGroupRules[i].get('NicType'))
			if SecurityGroupRules[i].get('PortRange') is not None:
				self.add_query_param('SecurityGroupRule.' + str(i + 1) + '.PortRange' , SecurityGroupRules[i].get('PortRange'))
			if SecurityGroupRules[i].get('IpProtocol') is not None:
				self.add_query_param('SecurityGroupRule.' + str(i + 1) + '.IpProtocol' , SecurityGroupRules[i].get('IpProtocol'))
			if SecurityGroupRules[i].get('Priority') is not None:
				self.add_query_param('SecurityGroupRule.' + str(i + 1) + '.Priority' , SecurityGroupRules[i].get('Priority'))
			if SecurityGroupRules[i].get('Policy') is not None:
				self.add_query_param('SecurityGroupRule.' + str(i + 1) + '.Policy' , SecurityGroupRules[i].get('Policy'))


	def get_SystemDiskSize(self):
		return self.get_query_params().get('SystemDisk.Size')

	def set_SystemDiskSize(self,SystemDiskSize):
		self.add_query_param('SystemDisk.Size',SystemDiskSize)

	def get_DefaultVpc(self):
		return self.get_query_params().get('DefaultVpc')

	def set_DefaultVpc(self,DefaultVpc):
		self.add_query_param('DefaultVpc',DefaultVpc)

	def get_SystemDiskDescription(self):
		return self.get_query_params().get('SystemDisk.Description')

	def set_SystemDiskDescription(self,SystemDiskDescription):
		self.add_query_param('SystemDisk.Description',SystemDiskDescription)