from neo4jUpload import Neo
from mongo import Mongo

#Create relationships
mongo = Mongo()
neo = Neo()

obj = mongo.findCountry()
while obj != None:
	neo.createCountry(obj)
	mongo.updateCountry(obj["_id"])
	obj = mongo.findCountry()

obj = mongo.findRegion()
while obj != None:
	neo.createRegion(obj)
	mongo.updateRegion(obj["_id"])
	obj = mongo.findRegion()

obj = mongo.findStyle()
while obj != None:
	neo.createStyle(obj)
	mongo.updateStyle(obj["_id"])
	obj = mongo.findStyle()

obj = mongo.findGrape()
while obj != None:
	neo.createGrape(obj)
	mongo.updateGrape(obj["_id"])
	obj = mongo.findGrape()

obj = mongo.findWinery()
while obj != None:
	neo.createWinery(obj)
	print("IM UPDATING")
	mongo.updateWinery(obj["_id"])
	obj = mongo.findWinery()

obj = mongo.findWine()
while obj != None:
	neo.createWine(obj)
	print("IM UPDATING")
	mongo.updateWine(obj["_id"])
	obj = mongo.findWine()
	
mongo.close()
neo.close()