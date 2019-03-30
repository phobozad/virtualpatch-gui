from bottle import Bottle

app = Bottle()

from virtualpatch import testDataParsing
from virtualpatch import routes


#if __name__ == "__main__":
	#localxc=testDataParsing.parseLocalXconnects()
	#print(localxc["A"])
#	virtualpatch.run(host="localhost", port=8081, debug=True, reloader=True)
