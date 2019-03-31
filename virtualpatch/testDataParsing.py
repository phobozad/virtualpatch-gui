import requests
import json

with open("config.json", "r") as configFile:
	config=json.load(configFile)
	deviceHost = config["deviceAccess"][0]["deviceHost"]
	devicePort = config["deviceAccess"][0]["devicePort"]
	deviceUser = config["deviceAccess"][0]["deviceUser"]
	devicePass = config["deviceAccess"][0]["devicePass"]


def parseLocalXconnects():
	xconnectParsedOutput = {}

	headers={"Content-Type": "application/yang-data+json",
	               "Accept": "application/yang-data+json"}
	
	url = "https://{host}:{port}/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context".format(host=deviceHost, port=devicePort)

	# Get list of current xconnects
	response = requests.get(url, auth=(deviceUser, devicePass), headers=headers, verify=False)
	# Parse JSON response into python dict
	responseDict = response.json()

	# Iterate through xconnects and build parsed output of xconnect pairs
	for xconnect in responseDict["Cisco-IOS-XE-l2vpn:context"]:
		aSide=""
		zSide=""

	# The below notes look to be inaccurate or possibly inconsistent
		# Only grab local xconnects
		# As of 16.8.1 any xconnect to an MPLS destination under an interface config
		# doesn't show up as a member but the l2vpn context still shows up without any config
		# We are verifying if the "xc-Mode-config-xconnect" node exists for this xconnect context
	#	if "xc-Mode-config-xconnect" in xconnect:
		
			# Additionally verify both xconnect members are local interfaces
			# As of 16.8.1 an xconnect configured with new "xconnect context" config to an MPLS
			# destination will not show that member under the xconnect context
	#		if len(xconnect["xc-Mode-config-xconnect"]["member"]["interface"]) == 2:
	#			aSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][0]["interface"]
	#			zSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][1]["interface"]
			
				# Ensure aSide and zSide are both defined and not empty strings
	#			if aSide and zSide:
	#				xconnectParsedOutput[xconnect["xc-name"]]={"a-side": aSide, "z-side": zSide}
		try:
			aSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][0]["interface"]
			zSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][1]["interface"]
		except (IndexError, KeyError):
			pass

		xconnectParsedOutput[xconnect["xc-name"]]={"a-side": aSide, "z-side": zSide}
	return xconnectParsedOutput

def interfaceList():
	
	interfaceList = []
	intTypes=["GigabitEthernet"]

	for intType in intTypes:
		headers={"Content-Type": "application/yang-data+json",
		               "Accept": "application/yang-data+json"}
	
		url = "https://{host}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface/{intType}?fields=name;description".format(host=deviceHost, port=devicePort, intType=intType)

		# Get list of interface names & descriptions
		response = requests.get(url, auth=(deviceUser, devicePass), headers=headers, verify=False)
		# Parse JSON response into python dict
		responseDict = response.json()

		# Iterate through interfaces and build parsed output of interface names
		for interface in responseDict["Cisco-IOS-XE-native:{}".format(intType)]:
			# If the description is set, take a closer look at it
			# Otherwise go to the next step if there isn't a description (avoids keyerror w/no description)
			if "description" in interface:
				# We filter out any interface that has a description starting with "$$NoVPP" (any case)
				# If the descripton starts with this, it won't get added to the list
				if not interface["description"].lower().startswith("$$novpp"):
					interfaceList.append({"intName": intType + interface["name"], "intDescription": interface["description"]})
			else:
				# If there isn't a description add interface to list with blank description
				interfaceList.append({"intName": intType + interface["name"], "intDescription": ""})

	return interfaceList;

def parseCdpNeighbors():
	cdpNeighborParsedOutput = {}

	headers={"Content-Type": "application/yang-data+json",
	               "Accept": "application/yang-data+json"}
	
	url = "https://{host}:{port}/restconf/data/Cisco-IOS-XE-cdp-oper:cdp-neighbor-details".format(host=deviceHost, port=devicePort)

	# Get CDP data
	response = requests.get(url, auth=(deviceUser, devicePass), headers=headers, verify=False)
	# Parse JSON response into python dict
	responseDict = response.json()

	# Iterate through the data and build parsed output using local interface name as key
	for neighbor in responseDict["Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"]["cdp-neighbor-detail"]:
		cdpNeighborParsedOutput[neighbor["local-intf-name"]]=neighbor

	return cdpNeighborParsedOutput;



