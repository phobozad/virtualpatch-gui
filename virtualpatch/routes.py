from virtualpatch import app
from virtualpatch import testDataParsing
from bottle import abort, request, template
import requests
import json

@app.route("/api/physicalxc")
def getPhysicalXC():
	return testDataParsing.parseLocalXconnects()

@app.route("/api/physicalxc/<name>")
def getPhysicalXC(name):
	localXcList=testDataParsing.parseLocalXconnects()
	if name in localXcList:
		return localXcList[name]
	else:
		abort(400, "XC Name Not Found")


@app.route("/api/physicalxc/<name>", method="PATCH")
def setPhysicalXC(name):
	headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
	url="https://192.168.2.133/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context={context}".format(context=name)
	bodyDict = request.json
	

	restConfRequest = '{"context":[{"xc-name":"' + name + '","xc-Mode-config-xconnect":{"member":{"interface":[{"interface":"' + bodyDict["a-side"] + '"},{"interface":"' + bodyDict["z-side"] + '"}]}}}]}'
	
	restConfResponse = requests.put(url, auth=("admin","cisco"), headers=headers, verify=False, data=restConfRequest)

	if (restConfResponse.status_code >= 200) and (restConfResponse.status_code < 300):
		return "IOS-XE says: {}".format(restConfResponse.status_code)
	else:
		abort(restConfResponse.status_code, "IOS-XE says: \r\n{}".format(restConfResponse.text))

@app.route("/")
def mainPage():
	return template("mainPage", localXcList=testDataParsing.parseLocalXconnects())

@app.route("/xcedit/<name>")
def xcEditPage(name):
	return xcEditPageGenerate(name)

def xcEditPageGenerate(name, statusMessage="", errorMessage=""):
	localXcList=testDataParsing.parseLocalXconnects()
	curASide=localXcList[name]["a-side"]
	curZSide=localXcList[name]["z-side"]
	return template("editPage", xcName=name, statusMessage=statusMessage, errorMessage=errorMessage, curASide=curASide, curZSide=curZSide, xcIntOptions=testDataParsing.interfaceList())


@app.route("/xcedit/<name>", method="POST")
def xcEdit(name):
	headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
	url="https://192.168.2.133/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context={context}".format(context=name)
	bodyDict = request.forms

		
	if not (("a-side" in bodyDict) and ("z-side" in bodyDict)):
		return xcEditPageGenerate(name, errorMessage="Invalid interface selection")
	
	restConfRequest = '{"context":[{"xc-name":"' + name + '","xc-Mode-config-xconnect":{"member":{"interface":[{"interface":"' + bodyDict["a-side"] + '"},{"interface":"' + bodyDict["z-side"] + '"}]}}}]}'
	
	restConfResponse = requests.put(url, auth=("admin","cisco"), headers=headers, verify=False, data=restConfRequest)

	if (restConfResponse.status_code >= 200) and (restConfResponse.status_code < 300):
		return xcEditPageGenerate(name, statusMessage="Change Saved. \r\nIOS-XE says: {}".format(restConfResponse.status_code))
	else:
		return xcEditPageGenerate(name, errorMessage="Error saving change. \r\nIOS-XE says: \r\n{}".format(restConfResponse.text))

@app.route("/ports")
def viewSwitchPorts(statusMessage="", errorMessage=""):
	return template("viewPorts", statusMessage=statusMessage, errorMessage=errorMessage, intList=testDataParsing.interfaceList(), cdpNeighbors=testDataParsing.parseCdpNeighbors())
