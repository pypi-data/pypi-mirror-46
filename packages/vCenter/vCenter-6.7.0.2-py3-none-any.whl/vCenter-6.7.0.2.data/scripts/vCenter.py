'''
Adding a Virtual Center to AVE
'''
import json
import requests
from REST_Check import CloudRestAutomation as CR

def AddVirtualCenter(Av_ip, vCentername, vCenterpasswd, vCenterUsername, headers):
	
	
	payload={
	"cbtEnabled": "true",
	"contact": {
	"email": "admin@emc.com",
	"location": "176 South Street Hopkinton",
	"name": "admin",
	"notes": "Dell EMC",
	"phone": "1-866-438-3622"
	},
	"domain": "/",
	"name": vCentername,
	"password": vCenterpasswd,
	"port": 443,
	"ruleDomainMapping": {

	},
	"ruleEnabled": "false",
	"username": vCenterUsername
	}
	
	json_data = json.dumps(payload)
	
	print("Adding vCenter to AVE")
	apiUrl = 'https://'+Av_ip+'/api/v1/virtualcenters'
	response = CR.POST(apiUrl, headers, json_data)
  
	return response.status_code
	

def  AddVM(vmName,vCentername , vCenterSessionId, Av_ip, vCcid ,headers):
	
	sess_with_cred = requests.Session()
	user="administrator@vsphere.local"
	password="Emclegato!23"
	
	Sessionheaders = {'Content-Type': 'application/json', 'cache-control': "no-cache",
                   'vmware-api-session-id': vCenterSessionId}
				   
	apiUrl = 'https://'+vCentername+'/rest/vcenter/vm'
	response = sess_with_cred.get(apiUrl, auth=(user, password), headers=Sessionheaders, verify=False)
	temp = response.json()
	json_data = temp['value']
	print(json_data)
	
	for dict in json_data:
		if dict["name"] == vmName:
			vmId = dict["vm"]

	vmEntityId	= 'VirtualMachine:' + vmId
	
	# Adding Vm to client using the Entity Id
	
	payload = {
	"cbtEnabled": "true",
	"contact": {
    "email": "admin@emc.com",
    "location": "176 South Street Hopkinton",
    "name": "admin",
    "notes": "Dell EMC",
    "phone": "1-866-438-3622"
	},
	"containerInclusionType": "DYNAMIC",
	"domain": "/10.110.211.163/VirtualMachines",
	"entityIds": [
    vmEntityId
	],
	"recursiveProtection": "true",
	"viewType": "VM_TEMPLATE"
	}
	
	json_data = json.dumps(payload)
	apiUrl = 'https://'+Av_ip+'/api/v1/virtualcenters/'+vCcid+'/clients'
	response = CR.POST(apiUrl, headers, json_data)
  
	return response.status_code
	
	
	
	
	
	
	
