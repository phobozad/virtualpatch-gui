import requests
import json

with open("config.json", "r") as configFile:
	config=json.load(configFile)
	deviceHost = config["deviceAccess"][0]["deviceHost"]
	devicePort = config["deviceAccess"][0]["devicePort"]
	deviceUser = config["deviceAccess"][0]["deviceUser"]
	devicePass = config["deviceAccess"][0]["devicePass"]


def xcEdit(xcName,aSide,zSide):
	resultOutput={}

	headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
	url = "https://{host}:{port}/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context={context}".format(host=deviceHost, port=devicePort, context=xcName)

	# We need to update the xconnect by specifying both members (a & z) in a PUT transaction
	restConfRequest = '{"context":[{"xc-name":"' + xcName + '","xc-Mode-config-xconnect":{"member":{"interface":[{"interface":"' + aSide + '"},{"interface":"' + zSide + '"}]}}}]}'
	
	restConfResponse = requests.put(url, auth=(deviceUser, devicePass), headers=headers, verify=False, data=restConfRequest)

	resultOutput["iosxe_status_code"]=restConfResponse.status_code
	resultOutput["iosxe_response"]=restConfResponse.text

	return resultOutput	

def xcDelete(xcName):
	resultOutput={}

	headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
	url = "https://{host}:{port}/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context={context}".format(host=deviceHost, port=devicePort, context=xcName)

	# We delete the xconnect by specifying the xconnect context name in a DELETE transaction
	restConfResponse = requests.delete(url, auth=(deviceUser, devicePass), headers=headers, verify=False)

	resultOutput["iosxe_status_code"]=restConfResponse.status_code
	resultOutput["iosxe_response"]=restConfResponse.text

	# Do some parsing of any 2xx code to summarize to a single good/bad result output
	if (restConfResponse.status_code >= 200) and (restConfResponse.status_code < 300):
		resultOutput["status"]="ok"
	else:
		resultOutput["status"]="failed"

	return resultOutput	

