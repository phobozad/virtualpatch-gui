from virtualpatch import app
from virtualpatch import testDataParsing

@app.route("/api/physicalxc")
def getPhysicalXC():
	return testDataParsing.parseLocalXconnects()


