#!/usr/bin/env python3

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

		# Only grab local xconnects
		# As of 16.8.1 any xconnect to an MPLS destination under an interface config
		# doesn't show up as a member but the l2vpn context still shows up without any config
		# We are verifying if the "xc-Mode-config-xconnect" node exists for this xconnect context
		if "xc-Mode-config-xconnect" in xconnect:
		
			# Additionally verify both xconnect members are local interfaces
			# As of 16.8.1 an xconnect configured with new "xconnect context" config to an MPLS
			# destination will not show that member under the xconnect context
			if len(xconnect["xc-Mode-config-xconnect"]["member"]["interface"]) == 2:
				aSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][0]["interface"]
				zSide = xconnect["xc-Mode-config-xconnect"]["member"]["interface"][1]["interface"]
			
			# Ensure aSide and zSide are both defined and not empty strings
			if aSide and zSide:
				xconnectParsedOutput[xconnect["xc-name"]]={"a-side": aSide, "z-side": zSide}
	return xconnectParsedOutput

localxc=parseLocalXconnects()

print(localxc["A"])

