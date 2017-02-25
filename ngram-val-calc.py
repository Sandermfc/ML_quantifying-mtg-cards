import os
import json
import re #regular expressions

nGramDict = {};

def main():
	#open the big json file containing our dataset, I'll refer to this as bigFile from here on out
	with open("AllSets-x.json") as file1:
		data = json.load(file1)

	#create a conversion table from setName to setCode (setCode is the format used in AllSets-x.json)
	setCode = {};
	for set in data:
		setCode[data[set]["name"].encode('utf-8')] = set;

	#for each file which has price data
	for fileName in os.listdir('price-by-set'):
		#open the file
		with open("price-by-set/"+fileName) as file2:
			cardPrices = json.load(file2);

		#substring the fileName to get setName
		pos = fileName.find('_');
		setName = fileName[pos+1:len(fileName)-5];

		#if setCode exists in bigFile
		if setCode[setName] in data:
			###############################################
			###DO STUFF TO SCRAPE INFO FROM THE SET HERE###
			###############################################
			#for each card in the set
			for card in data[setCode[setName]]["cards"]:
				###########
				###PRICE###
				###########
				price = getCardPrice(card["name"], cardPrices);
				if(price > 0):
					print(price);
					########################################################
					###DO STUFF TO SCRAPE INFO FROM INDIVIDUAL CARDS HERE###
					########################################################
					#################
					###DESCRIPTION###
					#################
					if "originalText" in card:
						print(card["originalText"].encode('utf-8'));
						getNGramCount(card["name"].encode('utf-8'), price, card["originalText"].encode('utf-8'), setName);
					else:
						print("NO ORIGINAL TEXT, GIVING VALUE OF 0");
					#Converted manacost
					#if "cmc" in card:
						#getCMC(card["cmc"]);
					#else:
						#print("NO CONVERTED MANACOST, GIVING CMC OF 0");
					#if "manaCost" in card:
						#getManaCharacteristics(card["manaCost"]);
					#else:
						#print("NO MANACOST FOUND");
				else:
					if(price == -1):
						print(card["name"].encode('utf-8') + " was not found in " + fileName);
					elif(price == -2):
						print(card["name"].encode('utf-8') + " had a 0$ price   " + fileName);
		else:
			print("ERROR, "+setCode+" does not exist in bigFile");


def getCardPrice(cardName, cardPrices):
	#-1 for "card not found"
	#-2 for value = 0;
	if cardName in cardPrices:
		if(cardPrices[cardName][0] != 0):
			return cardPrices[cardName][0];
		else:
			return -2;
	elif cardName + " (1)" in cardPrices: #check for syntax of alternate artworks
		tot = 0;
		finalPrice = 0;
		i = 1;
		while((cardName + "(" + str(i) + ")") in cardPrices):
			price = cardPrices[cardName + "(" + str(i) + ")"][0];
			if price != "" and float(price) != 0:
				tot+=1;
				finalPrice += price;
			i+=1;
		if tot != 0:
			finalPrice/=tot;
		else:
			return -2;
		#print(finalPrice);
		return finalPrice;
	else:
		return -1;

def getNGramCount(cardName, cardPrice, originalText, setName):
	#subfunction
	def upToNGram(pos):
		temp = "";

		for i in range(pos, min(pos+numGram, len(words))): #upper bound is the smallest between (pos+numgram) OR the last word in the sentence.
			temp += words[i] + " ";
			print(temp);
			nGramDict.setdefault(temp[:-1],[]).append(cardPrice);
	#Example for numGram = 3
	#for each SENTENCE in the description, do 1 gram;2 gram;3gram on the first 1,2 and 3 words
	#then do 3 gram for the rest of the sentence (do not do 2gram and 1 gram on the last 2 and 1 words)
	numGram = 3;
	words = re.split("[ \n]", originalText);
	print(words);
	temp = "";
	upToNGram(0);
	for i in range(1,len(words)-numGram):
		temp = "";
		for j in range(i, i+numGram):
			temp+=words[j]+" ";
		nGramDict.setdefault(temp[:-1],[]).append(cardPrice); #pass in temp with last letter removed (space)

def getCMC(cmc):
	print("do the cmc thing");

def getManaCharacteristics(manaCost):
	print("do the mana thing");

if __name__ == "__main__":
	main();


#{T}{1}{B}: creature name gains flying until the end of the turn.
