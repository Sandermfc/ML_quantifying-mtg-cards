import json 			#parse dataset
import datetime
from bs4 import BeautifulSoup	#parsing html
from selenium import webdriver #get html from url

def getCardList(setName):
	cards = {}
	setName = setName.replace(' ', '_') #replace spaces with underscores for url
	setName = setName.replace('.','') #remove dots
	setName = setName.replace('\'', '') #remove apostrophes
	setName = setName.replace(':','') #remove colons

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
	return cards;


##########
###MAIN###
##########
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

#only necessary as it would sometimes crash, remove the ones already done
numOfAlreadyDone = raw_input("How many sets are already downloaded?");
for i in range(0,int(numOfAlreadyDone)):
	setByYear.pop(0);

cards = {}
setNum = int(numOfAlreadyDone);
for mySet in setByYear:
	setNum = setNum + 1;
	setName = mySet[0];
	cards = getCardList(setName);
	if len(cards) == 0 :
		newSetName = raw_input("Is "+setName+" right?");
		cards = getCardList(newSetName);

	with open("price-by-set/" + str(setNum) +"_"+ setName+".json", 'w') as fp:
		json.dump(cards, fp)
    	print(str(setNum) + "created json file for "+setName+" which has "+str(len(cards))+" unique cards")
    	cards.clear()