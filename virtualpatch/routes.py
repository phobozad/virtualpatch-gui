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

@app.route("/edit/<name>")
def editPage(name):
	return editPageGenerate(name)

def editPageGenerate(name, statusMessage=""):
	localXcList=testDataParsing.parseLocalXconnects()
	curASide=localXcList[name]["a-side"]
	curZSide=localXcList[name]["z-side"]
	return template("editPage", xcName=name, statusMessage=statusMessage, curASide=curASide, curZSide=curZSide, xcIntOptions=testDataParsing.interfaceList())


@app.route("/edit/<name>", method="POST")
def xcEdit(name):
	headers={"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}
	url="https://192.168.2.133/restconf/data/Cisco-IOS-XE-native:native/l2vpn/xconnect/context={context}".format(context=name)
	bodyDict = request.forms

	restConfRequest = '{"context":[{"xc-name":"' + name + '","xc-Mode-config-xconnect":{"member":{"interface":[{"interface":"' + bodyDict["a-side"] + '"},{"interface":"' + bodyDict["z-side"] + '"}]}}}]}'
	
	restConfResponse = requests.put(url, auth=("admin","cisco"), headers=headers, verify=False, data=restConfRequest)

	if (restConfResponse.status_code >= 200) and (restConfResponse.status_code < 300):
		return editPageGenerate(name, statusMessage="Change Saved.  IOS-XE says: {}".format(restConfResponse.status_code))
	else:
		return editPageGenerate(name, statusMessage="Error saving change.  IOS-XE says: \r\n{}".format(restConfResponse.text))

