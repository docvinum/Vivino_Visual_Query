from neo4j import GraphDatabase
import re
class Neo():
	def __init__(self):
	    self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))

	def relateCountry(self, obj, session):
		# country and region
	    inp = ("MATCH (r:Region {country:'" + re.sub("[']", "\\'",obj["country"]) + "'})"
	    	+ "MATCH (c:Country {name: '" + re.sub("[']", "\\'",obj["country"]) + "'}) "
	    	+ "MERGE (r)-[:IsIn]->(c)")
	    session.run(inp)
	    # country and grape
	    inp = ("MATCH (c:Country {name: '" + re.sub("[']", "\\'",obj["country"]) + "'}) MATCH (g:Grape) " 
	    	+ "WHERE g.origin =~ '.*" + re.sub("[']", "\\'",obj["country"]) + "' "
	    	+ "MERGE (g)-[:OriginCountry]->(c)")
	    session.run(inp)
	    # style and country
	    inp = ("MATCH (c:Country {name: '" + re.sub("[']", "\\'",obj["country"]) + "'}) "
	    	+ "MATCH (s:Style) " 
	    	+ "WHERE s.region =~ '.*" + re.sub("[']", "\\'",obj["country"]) + "' "
	    	+ "MERGE (s)-[:StyleRegion]->(r)")
	    session.run(inp)

	def relateGrape(self, obj, session):
		splitStr = obj["origin"].split(',')
		if len(splitStr) == 2:
			country = splitStr[1].lstrip()
			region = splitStr[0]
			# grape and region
			inp = ("MATCH (g:Grape {origin:'" + re.sub("[']", "\\'",obj["origin"]) + "'}) "
				+ "MATCH (r:Region {region:'" + re.sub("[']", "\\'",region) + "'}) "
				+ "MERGE (g)-[:OriginRegion]->(r)")
			session.run(inp)
			# grape and country
			inp = ("MATCH (g:Grape {origin:'" + re.sub("[']", "\\'",obj["origin"]) + "'}) "
				+ "MATCH (c:Country {name:'" + re.sub("[']", "\\'",country) + "'}) "
				+ "MERGE (g)-[:OriginCountry]->(c)")
			session.run(inp)
		else:
			strOut = splitStr[0].strip()
			# grape and region
			inp = ("MATCH (g:Grape {origin:'" + re.sub("[']", "\\'",obj["origin"]) + "'}) "
				+ "MATCH (r:Region {region:'" + re.sub("[']", "\\'",strOut) + "'}) "
				+ "MERGE (g)-[:OriginRegion]->(r)")
			session.run(inp)
			# grape and country
			inp = ("MATCH (g:Grape {origin:'" + re.sub("[']", "\\'",obj["origin"]) + "'}) "
				+ "MATCH (c:Country {name:'" + re.sub("[']", "\\'",strOut) + "'}) "
				+ "MERGE (g)-[:OriginCountry]->(c)")
			session.run(inp)

	def relateRegion(self, obj, session):
	    # region and grape
	    inp = ("MATCH (r:Region {region: '" + re.sub("[']", "\\'",obj["region"]) + "'}) "
	    	+ "MATCH (g:Grape) "
	    	+ "WHERE g.origin =~ '" + re.sub("[']", "\\'",obj["region"]) + ".*' "
	    	+ "MERGE (r)-[:origin]->(g)")
	    session.run(inp)
	    # region and country
	    inp = ("MATCH (r:Region {country:'" + re.sub("[']", "\\'",obj["country"]) + "'})"
	    	+ "MATCH (c:Country {name: '" + re.sub("[']", "\\'",obj["country"]) + "'}) "
	    	+ "MERGE (r)-[:IsIn]->(c)")
	    session.run(inp)
	    inp = ("MATCH (a:Region {region:'" + re.sub("[']", "\\'",obj["region"]) + "'}), (b:Style), (a)-[r]-(b)" 
	    	+ "WHERE b.region <> 'N/A' WITH a,b MATCH (c:Country) "
	    	+ "WHERE b.region CONTAINS c.name MERGE (a)-[:RegionOf]->(c)")
	    session.run(inp)

	def relateStyle(self, obj, session):
		splitStr = obj["region"].split(',')
		if len(splitStr) == 2:
			country = splitStr[1].lstrip()
			region = splitStr[0]
			# grape and region
			inp = ("MATCH (s:Style {style:'" + re.sub("[']", "\\'",obj["style"]) + "'}) "
				+ "MATCH (r:Region {region:'" + re.sub("[']", "\\'",region) + "'}) "
				+ "MERGE (s)-[:StyleRegion]->(r)")
			session.run(inp)
			# grape and country
			inp = ("MATCH (s:Style {style:'" + re.sub("[']", "\\'",obj["style"]) + "'}) "
				+ "MATCH (c:Country {name:'" + re.sub("[']", "\\'",country) + "'}) "
				+ "MERGE (s)-[:StyleCountry]->(c)")
			session.run(inp)
			inp = ("MATCH (a:Style {style:'" + re.sub("[']", "\\'",obj["style"]) + "'}), (b:Region), (a)-[]-(b) "
				+ "WITH a,b MATCH (c:Country), (c)-[]-(a) "
				+ "MERGE (b)-[:RegionOf]->(c)")
		else:
			strOut = splitStr[0].strip()
			# grape and region
			inp = ("MATCH (s:Style {style:'" + re.sub("[']", "\\'",obj["style"]) + "'}) "
				+ "MATCH (r:Region {region:'" + re.sub("[']", "\\'",strOut) + "'}) "
				+ "MERGE (s)-[:StyleRegion]->(r)")
			session.run(inp)
			# grape and country
			inp = ("MATCH (s:Style {style:'" + re.sub("[']", "\\'",obj["style"]) + "'}) "
				+ "MATCH (c:Country {name:'" + re.sub("[']", "\\'",strOut) + "'}) "
				+ "MERGE (s)-[:StyleCountry]->(c)")
			session.run(inp)

	def relateWine(self, obj, session):
		# wine and winery
		inp = ("MATCH (wy:Winery {name: '" + re.sub("[']", "\\'",obj["winery"]) + "'}) "
			+ "MATCH (we:Wine {name: '" + re.sub("[']", "\\'",obj["name"]) + "', winery: '" + re.sub("[']", "\\'",obj["winery"]) + "'}) "
			+ "MERGE (we)-[:BelongsTo]->(wy)")
		session.run(inp)
	    # wine and style
		inp = ("MATCH (s:Style {style: '" + re.sub("[']", "\\'",obj["style"]) + "'}) "
			+ "MATCH (w:Wine {name: '" + re.sub("[']", "\\'",obj["name"]) + "', style: '" + re.sub("[']", "\\'",obj["style"]) + "'}) "
			+ "MERGE (w)-[:StyleOf]->(s)")
		session.run(inp)
	    # wine and grapes
		for i in obj["grapes"]:
			inp = ("MATCH (g:Grape {name: '" + re.sub("[']", "\\'",i) + "'}) "
				+ "MATCH (w:Wine {name: '" + re.sub("[']", "\\'",obj["name"]) + "', grapes: '"
				+ str(obj["grapes"]).replace("'", '"') + "'}) "
				+ "MERGE (w)-[:GrapeUsed]->(g)")
			session.run(inp)
		# winery and region through wine
		inp = ("MATCH (wy:Winery {name:'" + re.sub("[']", "\\'",obj["winery"]) + "'}) "
			+ "MATCH (r:Region {region:'" + re.sub("[']", "\\'",obj["region"]) + "'}) "
			+ "MERGE (wy)-[:WineryRegion]->(r)")
		session.run(inp)

	def relateWinery(self, obj, session):
		# winery and wines
	    inp = ("MATCH (wy:Winery {name: '" + re.sub("[']", "\\'",obj["name"]) + "'}) "
	    	+ "MATCH (we:Wine {winery: '" + re.sub("[']", "\\'",obj["name"]) + "'}) "
	    	+ "MERGE (we)-[:BelongsTo]->(wy)")
	    session.run(inp)
	    # winery and region
	    inp = ("MATCH (wy:Winery {name: '" + re.sub("[']", "\\'",obj["name"]) + "'}) "
	    	+ "MATCH (we:Wine {winery: '" + re.sub("[']", "\\'",obj["name"]) + "'}) "
	    	+ "WITH we,wy "
	    	+ "MATCH (r:Region {region: we.region}) "
	    	+ "MERGE (wy)-[:WineryRegion]->(r)")
	    session.run(inp)

	def createCountry(self, obj):
		session = self.driver.session()
		inp = ("CREATE (c:Country {name:'" + re.sub("[']", "\\'",obj["country"]) 
			+ "', url:'" + obj["url"] + "'})")
		print(inp)
		session.run(inp)
		print("Created country: " + str(obj["_id"]))
		self.relateCountry(obj, session)
		print("Created relationships")
		session.close()

	def createGrape(self, obj):
		session = self.driver.session()
		inp = ("CREATE (g:Grape {name:'" + re.sub("[']", "\\'",obj["grape"]) +
		"', description:'" + re.sub("[']", "\\'",(re.sub("[^a-zA-Z'\- ]+", '', obj["description"]))) + "', characteristics:'" 
		+ obj["characteristics"] + "', acidity:'" + obj["acidity"] 
		+ "', body:'" + obj["body"] + "', origin:'" + obj["origin"] 
		+ "', url:'" + obj["url"] + "'})")
		print(inp)
		session.run(inp)
		print("Created grape: " + str(obj["_id"]))
		self.relateGrape(obj, session)
		print("Created relationships")
		session.close()

	def createRegion(self, obj):
		session = self.driver.session()
		inp = ("CREATE (r:Region {region:'" + re.sub("[']", "\\'",obj["region"])
			+ "', country:'" + re.sub("[']", "\\'",obj["country"])
			+ "', description:'" 
			+ re.sub("[']", "\\'",(re.sub("[^a-zA-Z'\- ]+", '', obj["description"]))) 
			+ "', url:'" + obj["url"] + "'})")
		print(inp)
		session.run(inp)
		print("Created region: " + str(obj["_id"]))
		self.relateRegion(obj, session)
		print("Created relationships")
		session.close()

	def createStyle(self, obj):
		session = self.driver.session()
		inp = ("CREATE (s:Style {style:'" + re.sub("[']", "\\'",obj["style"]) 
			+ "', region:'" + re.sub("[']", "\\'",obj["region"]) + "', description:'" 
			+ re.sub("[']", "\\'",(re.sub("[^a-zA-Z'\- ]+", '', obj["description"]))) + "', acidity:'" + obj["acidity"]
			+ "', body:'" + re.sub("[']", "\\'",obj["body"]) 
			+ "', url:'" + obj["url"] + "'})")
		print(inp)
		session.run(inp)
		print("Created style: " + str(obj["_id"]))
		self.relateStyle(obj, session)
		print("Created relationships")
		session.close()


	def createWinery(self, obj):
		session = self.driver.session()
		inp = ("CREATE (w:Winery {name:'" + re.sub("[']", "\\'",obj["name"]) + "', avgRate:'" 
			+ obj["avgRate"] + "', numWines:'" + re.sub("[']", "\\'",obj["numWines"]) 
			+ "', address:'" 
			+ re.sub("[']", "\\'",obj["address"].replace("\\", "").replace("N/A", "").replace("\\'", "'"))
			+ "', latitude:'" + obj["latitude"]
			+ "', longitude:'" + obj["longitude"] + "', website:'" + re.sub("[']", "\\'",obj["companyWebsite"]) 
			+ "', email:'" + obj["email"] 
			+ "', url: '" + re.sub("[']", "\\'",obj["url"]) 
			+ "', companyWebsite: '" + re.sub("[']", "\\'",obj["companyWebsite"]) + "'})")
		print(inp)
		session.run(inp)
		print("Created winery: " + str(obj["_id"]))
		self.relateWinery(obj, session)
		print("Created relationships")
		session.close()

	def createWine(self, obj):
		session = self.driver.session()
		inp = ("CREATE (w:Wine {name:'" + re.sub("[']", "\\'",obj["name"]) 
			+ "', winery:'" + re.sub("[']", "\\'",obj["winery"]) + "', region:'" 
			+ re.sub("[']", "\\'",obj["region"]) + "', style:'" + re.sub("[']", "\\'",obj["style"])
			+ "', rating:'" + re.sub("[']", "\\'",obj["rating"]) + "', grapes:'" 
			+ str(obj["grapes"]).replace("'", '"') 
			+ "', pairings:'" + re.sub("[']", "\\'",obj["pairings"]) 
			+ "', img:'" + obj["img"] 
			+ "', url:'" + obj["url"] + "'})")
		print(inp)
		session.run(inp)
		print("Created wine: " + str(obj["_id"]))
		self.relateWine(obj, session)
		print("Created relationships")
		session.close()

	#close driver
	def close(self):
		self.driver.close()

