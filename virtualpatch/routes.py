from virtualpatch import app
from virtualpatch import dataParsing
from virtualpatch import deviceCommands
from bottle import abort, request, template, redirect
import requests
import json

@app.route("/api/physicalxc")
def getPhysicalXC():
	return dataParsing.parseLocalXconnects()

@app.route("/api/physicalxc/<name>")
def getPhysicalXC(name):
	localXcList=dataParsing.parseLocalXconnects()
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
	errorMessage=request.params.get("errorMessage","")
	statusMessage=request.params.get("statusMessage","")
	return template("mainPage", localXcList=dataParsing.parseLocalXconnects(), xcIntOptions=dataParsing.interfaceList(), errorMessage=errorMessage, statusMessage=statusMessage)

@app.route("/xc/edit/<name>")
def xcEditPage(name):
	errorMessage=request.params.get("errorMessage","")
	statusMessage=request.params.get("statusMessage","")
	return xcEditPageGenerate(name, errorMessage=errorMessage, statusMessage=statusMessage)

def xcEditPageGenerate(name, statusMessage="", errorMessage=""):
	localXcList=dataParsing.parseLocalXconnects()
	curASide=localXcList[name]["a-side"]
	curZSide=localXcList[name]["z-side"]
	return template("editPage", xcName=name, statusMessage=statusMessage, errorMessage=errorMessage, curASide=curASide, curZSide=curZSide, xcIntOptions=dataParsing.interfaceList())


@app.route("/xc/edit/<name>", method="POST")
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

@app.route("/xc/delete/<name>", method="POST")
def xcDelete(name):
	deleteResponse = deviceCommands.xcDelete(name)
	if deleteResponse["status"]=="ok":
		redirect("/?statusMessage=Success: Deleted Patch {name}.".format(name=name))
	else:
		redirect("/xc/edit/{name}?errorMessage=Error: Delete Failed.".format(name=name))

def xcAddPageGenerate(statusMessage="", errorMessage=""):
	localXcList=dataParsing.parseLocalXconnects()
	return template("addPage", statusMessage=statusMessage, errorMessage=errorMessage, xcIntOptions=dataParsing.interfaceList())

@app.route("/xc/add")
def xcAddPage():
	errorMessage=request.params.get("errorMessage","")
	statusMessage=request.params.get("statusMessage","")
	return xcAddPageGenerate(statusMessage=statusMessage, errorMessage=errorMessage)

@app.route("/xc/add", method="POST")
def xcAdd():
	# Ensure we have both A and Z sides defined
	if not (("a-side" in request.forms) and ("z-side" in request.forms) and ("xcName" in request.forms)):
		return xcAddPageGenerate(errorMessage="Invalid interface selection or Name")

	aSide = request.forms["a-side"]
	zSide = request.forms["z-side"]
	xcName = request.forms["xcName"]

	addResponse = deviceCommands.xcAdd(xcName,aSide,zSide)
	
	if addResponse["status"]=="ok":
		redirect("/?statusMessage=Success: Added Patch {name}.".format(name=xcName))
	else:
		return xcAddPageGenerate(errorMessage="Error: Add Failed.")


@app.route("/ports")
def viewSwitchPorts(statusMessage="", errorMessage=""):
	return template("viewPorts", statusMessage=statusMessage, errorMessage=errorMessage, intList=dataParsing.interfaceList(), cdpNeighbors=dataParsing.parseCdpNeighbors())
