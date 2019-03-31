from virtualpatch import app
from virtualpatch import testDataParsing
from virtualpatch import deviceCommands
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
	if not (("a-side" in request.json) and ("z-side" in request.json)):
		abort(400, "Invalid interface selection.")

	editResponse = deviceCommands.xcEdit(name, request.json["a-side"], request.json["z-side"])
	
	if (editResponse.get("iosxe_status_code", 0) >= 200) and (editResponse.get("iosxe_status_code", 0) < 300):
		return "IOS-XE says: {}".format(editResponse["iosxe_status_code"])
	else:
		abort(editResponse.get("iosxe_status_code",500), "IOS-XE says: \r\n{}".format(editResponse.get("iosxe_response", "")))

@app.route("/")
def mainPage():
	return template("mainPage", localXcList=testDataParsing.parseLocalXconnects(), xcIntOptions=testDataParsing.interfaceList())

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
	# Ensure we have both A and Z sides defined
	# We need to re-push both xconnect members at the same time when we update the device
	if not (("a-side" in request.forms) and ("z-side" in request.forms)):
		return xcEditPageGenerate(name, errorMessage="Invalid interface selection")
	
	editResponse = deviceCommands.xcEdit(name, request.forms["a-side"], request.forms["z-side"])

	if (editResponse.get("iosxe_status_code", 0) >= 200) and (editResponse.get("iosxe_status_code", 0) < 300):
		return xcEditPageGenerate(name, statusMessage="Change Saved. \r\nIOS-XE says: {}".format(editResponse.get("iosxe_status_code", "")))
	else:
		return xcEditPageGenerate(name, errorMessage="Error saving change. \r\nIOS-XE says: \r\n{}".format(editResponse.get("iosxe_response")))

@app.route("/ports")
def viewSwitchPorts(statusMessage="", errorMessage=""):
	return template("viewPorts", statusMessage=statusMessage, errorMessage=errorMessage, intList=testDataParsing.interfaceList(), cdpNeighbors=testDataParsing.parseCdpNeighbors())
