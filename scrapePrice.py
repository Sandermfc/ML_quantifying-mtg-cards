import json 			#parse dataset
import datetime
from bs4 import BeautifulSoup	#parsing html
from selenium import webdriver #get html from url


driver = webdriver.Firefox()

html = driver.page_source
soup = BeautifulSoup(html)

fileName = "AllSets-x.json"

with open(fileName) as file:
	data = json.load(file)
print("Done reading json file for set names.")

#BLACKLIST maybe
#planechase
#promo
#reprint
#from the vault
#duel deck
#masters
#starter

setByYear = [] #key=set name; value=releaseDate

for key in data:
	setByYear.append((data[key]["name"].encode('utf-8'), data[key]["releaseDate"].encode('utf-8'))) #mkm_id used for sort by release date. Easier than converting release_date to sortable type

setByYear.sort(key=lambda x: x[1], reverse=True) #by newest to oldest set


cards = {}
for mySet in setByYear:
	setName = mySet[0];
	setName = setName.replace(' ', '_') #replace spaces with underscores for url
	setName = setName.replace('.','')
	setName = setName.replace(':','') #remove dots
	driver.get('http://www.mtgprice.com/spoiler_lists/'+setName)

	html_doc = driver.page_source
	soup = BeautifulSoup(html_doc)

	soup = soup.find(id="setTable").tbody.find_all("tr")

	for card in soup:
		infos = card.findAll('td')
		#print(infos[0].a.text)  #card name
		#print(infos[1].text)	 #fair trade price
		#print(infos[2].text)	 #actual (best) buy price
		cards[infos[0].a.text] = (infos[1].text, infos[2].text);

	with open(setName+".json", 'w') as fp:
		json.dump(cards, fp)
    	print("created json file for "+setName+" which has "+str(len(cards))+" unique cards")
    	cards.clear()