import dirtyjson, requests
from bs4 import BeautifulSoup

def queryNI(pn):
	'''Gets first link result from searching part number'''
	response = requests.get("http://search.ni.com/nisearch/app/main/p/bot/no/ap/global/lang/en/pg/1/q/%22"+pn+"%22/")
	soup = BeautifulSoup(response.content,"html.parser")
	search = soup.find("a",{"class":"resultClickTracking"})
	
	'''Gets dictionary info of part by part number'''
	response = requests.get(search["href"])
	soup = BeautifulSoup(response.content,"html.parser")
	search = soup.find_all("script")
	for item in search:
		if "var pnTableItem" in item.text[:17]:
			dictFound = item
			break
	data = dictFound.text.split("var pnTableItem = ")[1]
	data = data.split("digitalData.product[0]")[0]
	hwData = dirtyjson.loads(data)
	for item in hwData["tableItems"]:
		if item["partNumber"] == pn:
			found = item
			break
	print(found["modelName"])
	return found

'''Downloads Dimensional Drawing of part named after part number'''
def getImageMarway(link,pn):
	response = requests.get(link)
	soup = BeautifulSoup(response.content,"html.parser")
	search = soup.find("img",{"class":"MPSDetailsDefaultImage"})
	filename = pn
	image_link = "http://www.marway.com" + search["src"]
	print(image_link)
	image_content = requests.get(image_link,verify=False).content
	with open(filename+".jpg", 'wb') as handler:
		handler.write(image_content)

def queryMarway(pn):
	'''Creates a dictionary of all table elements on the given page'''
	link = "http://www.marway.com/mpd/specs/"+pn
	response = requests.get(link)
	soup = BeautifulSoup(response.content,"html.parser")
	marwayInfo = dict()
	search = soup.find_all("div",{"class":["MPSDetailsPanelRow","cf"]})
	for item in search:
		if item.find("div",{"class":"MPSDetailsPanelLabel"}) is not None:
			key = item.find("div",{"class":"MPSDetailsPanelLabel"}).text
			value = item.find("div",{"class":"MPSDetailsPanelField"}).text
			marwayInfo[key] = value
			print(key,value)
	print(marwayInfo["Dimensions"])
	getImageMarway(link,pn)
	return marwayInfo
	
	
def queryBloomy(pn):
	response = requests.get("http://www.bloomy.com/search/node/"+pn)
	soup = BeautifulSoup(response.content,"html.parser")
	search = soup.find("article",{"class":"search-result"})
	link = search.find("a")["href"]
	response = requests.get(link)
	soup = BeautifulSoup(response.content,"html.parser")
	bloomyInfo = dict()
	search = soup.find_all("tbody")
	for table in search:
		for row in table.find_all("tr"):
			rowget = row.find_all("td")
			if len(rowget) == 2:
				print(rowget[0].text,rowget[1].text)
				bloomyInfo[rowget[0].text] = rowget[1].text
	return bloomyInfo
