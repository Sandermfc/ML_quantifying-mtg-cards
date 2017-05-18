import os
import json
import re #regular expressions
import datetime
import splitdesc as splitdesc
import math

nGramDict = {};
nGramVal = {};

keyword = {};
description = {};
cmc = {};
numOfColors = {};
dictPower = {};
dictToughness = {};
dictRarity = {};
numOfReprints = {};
releaseDateDict = {}


def main():
	#open the big json file containing our dataset, I'll refer to this as bigFile from here on out
	with open("AllSets-x.json") as file1:
		data = json.load(file1);

	#create a conversion table from setName to setCode (setCode is the format used in AllSets-x.json)
	setCode = {};
	for set in data:
		setCode[data[set]["name"].encode('utf-8')] = set;
	with open("setCodes.json", 'w') as fp:
		json.dump(setCode, fp);

	#for each file which has price data
	for fileName in os.listdir('price-by-set'):
		#open the file
		with open("price-by-set/"+fileName) as file2:
			cardPrices = json.load(file2);

		#substring the fileName to get setName
		pos = fileName.find('_');
		setName = fileName[pos+1:len(fileName)-5];
		print(setName);
		#if setCode exists in bigFile
		if setCode[setName] in data:
			if "releaseDate" in data[setCode[setName]]:
				releaseDate = data[setCode[setName]]["releaseDate"].encode('utf-8');
				releaseDateInt = int(releaseDate[:4])*365 + int(releaseDate[5:7])*30 + int(releaseDate[9:]); #int value of date = year*365 + month*30 + day
			else:
				#Something is wrong, shouldnt go here
				releaseDateInt = 0;
			#############################################################
			###DO STUFF TO SCRAPE INFO FROM THE SET HERE (if you want)###
			#############################################################
			tempDescription = {};
			tempCmc = {};
			tempNumOfColors = {};
			tempPower = {};
			tempToughness = {};
			tempRarity = {};
			tempNumberOfPrintings = {};
			tempReleaseDate = {};
			#for each card in the set
			for card in data[setCode[setName]]["cards"]:
				###########
				###PRICE###
				###########
				cardName = card["name"].encode('utf-8');
				price = getCardPrice(cardName, cardPrices);
				if(price > 0):
					########################################################
					###DO STUFF TO SCRAPE INFO FROM INDIVIDUAL CARDS HERE###
					########################################################
					#################
					###DESCRIPTION###
					#################
					if "originalText" in card:
						tempDescription[cardName.encode('utf-8')] = getDescription(card["name"].encode('utf-8'), price, card["originalText"].encode('utf-8'), setName);
					else:
						tempDescription[cardName] = "";
					########################
					###CONVERTED MANACOST###
					########################
					if "cmc" in card:
						#getCMC(cardName, card["cmc"]);
						tempCmc[cardName.encode('utf-8')] = card["cmc"];
					else:
						tempCmc[cardName.encode('utf-8')] = 0;
					##############
					###MANACOST###
					##############	
					if "colorIdentity" in card:
						tempNumOfColors[cardName] = len(card["colorIdentity"]);
						#getNumOfColors(cardName, card["colorIdentity"]);
					else:
						tempNumOfColors[cardName] = 0;
					###########
					###POWER###
					###########
					if "power" in card:
						tempPower[cardName] = getPt(card["power"]);
						#getPower(cardName, card["power"]);
					else:
						tempPower[cardName] = 0;
					###############
					###TOUGHNESS###
					###############
					if "toughness" in card:
						tempToughness[cardName] = getPt(card["toughness"]);
						#getToughness(cardName, card["toughness"]);
					else:
						tempToughness[cardName] = 0;
					############
					###RARITY###
					############
					if "rarity" in card:
						tempRarity[cardName] = getRarity(card["rarity"]);
					else:
						tempRarity[cardName]
					########################
					###NUMBER OF REPRINTS###
					########################
					if "printings" in card:
						tempNumberOfPrintings[cardName] = len(card["printings"]);
						#getNumberOfPrintings(cardName, card["printings"]);
					else:
						tempNumberOfPrintings[cardName] = 1;
					##################
					###RELEASE DATE###
					##################
					tempReleaseDate[cardName] = releaseDateInt;
				#else:
				#	if(price == -1):
				#		print(card["name"].encode('utf-8') + " was not found in " + fileName);
				#	elif(price == -2):
				#		print(card["name"].encode('utf-8') + " had a 0$ price   " + fileName);
			##############################################
			#####Save all dictionnaries to json files#####
			##############################################
			description[setCode[setName]] = tempDescription;
			cmc[setCode[setName]] = tempCmc;
			numOfColors[setCode[setName]] = tempNumOfColors;
			dictPower[setCode[setName]] = tempPower;
			dictToughness[setCode[setName]] = tempToughness;
			dictRarity[setCode[setName]] = tempRarity;
			numOfReprints[setCode[setName]] = tempNumberOfPrintings;
			releaseDateDict[setCode[setName]] = tempReleaseDate;
		else:
			print("ERROR, "+setCode+" does not exist in bigFile");

	#Heavily weighted average
	for ngram in nGramDict:
		minOccurences = 3;
		priceList = [];
		if(len(nGramDict[ngram]) >= minOccurences):
			for price in nGramDict[ngram]:
				priceList.append(price);
			priceList = sorted(priceList);
			val=priceList[len(priceList)/2] #mediane

			print(ngram + " --> "+str(val));
			nGramVal[ngram] = val;
			
	print("parsedData/ammount of ngram's = "+str(len(nGramVal)));
	with open("parsedData/ngramCount"+".json", 'w') as fp:
		json.dump(nGramDict, fp);
	with open("parsedData/descriptions"+".json", 'w') as fp:
		json.dump(description, fp);
	with open("parsedData/cmc"+".json", 'w') as fp:
		json.dump(cmc, fp);
	with open("parsedData/numOfColors"+".json", 'w') as fp:
		json.dump(numOfColors, fp);
	with open("parsedData/power"+".json", 'w') as fp:
		json.dump(dictPower, fp);
	with open("parsedData/toughness"+".json", 'w') as fp:
		json.dump(dictToughness, fp);
	with open("parsedData/rarity"+".json", 'w') as fp:
		json.dump(dictRarity, fp);
	with open("parsedData/numOfReprints"+".json", 'w') as fp:
		json.dump(numOfReprints, fp);
	with open("parsedData/releaseDate"+".json",'w') as fp:
		json.dump(releaseDateDict, fp);


def getCardPrice(cardName, cardPrices):
	#-1 for "card not found"
	#-2 for value = 0;
	if cardName in cardPrices:
		if(cardPrices[cardName][0][1:] != 0):
			return cardPrices[cardName][0][1:].replace(',','');
		else:
			return -2;
	elif cardName + " (1)" in cardPrices: #check for syntax of alternate artworks
		tot = 0;
		finalPrice = 0;
		i = 1;
		while((cardName + "(" + str(i) + ")") in cardPrices):
			price = cardPrices[cardName + "(" + str(i) + ")"][0][1:];
			if price != "" and float(price) != 0:
				tot+=1;
				finalPrice += price;
			i+=1;
		if tot != 0:
			finalPrice/=tot;
		else:
			return -2;
		#print(finalPrice);
		return finalPrice[1:].replace(',','');
	else:
		return -1;

def getDescription(cardName, cardPrice, originalText, setName):
	originalText = originalText.replace(cardName, "this")
	keywords = {}
	with open('keywords2.txt', 'r') as file2:
		for line in file2:
			keywords[line.strip('\n').split(' ')[0]] = line.strip('\n');
	[dummy, originalText] = splitdesc.clean_desc(originalText.encode('utf-8'), keywords)
	originalText = originalText.lower()
	getNGramCount(cardName,cardPrice,originalText, setName)
	return originalText

def getNGramCount(cardName, cardPrice, originalText, setName):
	#subfunction
	def upToNGram(sent):
		temp = "";
		numWords = numGram;
		for x in range(0, len(sent)):
			temp+=sent[x]+" ";
			nGramDict.setdefault(temp.strip(),[]).append(cardPrice);
			numWords-=1;
			if(numWords==0):
				break;
	#Example for numGram = 3
	#for each SENTENCE in the description, do 1 gram;2 gram;3gram on the first 1,2 and 3 words
	#then do 3 gram for the rest of the sentence (do not do 2gram and 1 gram on the last 2 and 1 words)
	numGram = 3;

	#seperate into sentences and words
	wordSeperators = [' ', '\n'];	
	sentenceSeperators = ['.','(',')',','];
	removeTheseFromFront = [' ','\n','\t'];

	word="";
	sentence = [];
	sentences = [];
	for i in range(0,len(originalText)):
		if(originalText[i] in wordSeperators and word != ""):
			sentence.append(word);
			word="";
		elif(originalText[i] in sentenceSeperators):
			if(word not in wordSeperators and word != ""):
				sentence.append(word);
				#print(sentence);
				sentences.append(sentence);
				sentence = [];
			word="";
		else:
			word+=originalText[i];

	for i in range(0,len(sentences)): #for each sentence
		upToNGram(sentences[i]);
		for j in range(1,len(sentences[i])-numGram+1): #for each word in the sentence starting at word number 2 (we already dealt with all instances of 1st word in upToNGram())
			temp="";
			for k in range(0,numGram): #get the next 3 words
				temp+=sentences[i][j+k]+" ";
			nGramDict.setdefault(temp.strip(),[]).append(cardPrice);

def getCMC(cardName, cmcVal):
	cmc[cardName.encode('utf-8')] = cmcVal;
	#print("cmc " +str(cmc[cardName.encode('utf-8')]));

def getNumOfColors(cardName, colorIdentity):
	numOfColors[cardName.encode('utf-8')] = len(colorIdentity);
	#print("numOfColors "+str(numOfColors[cardName.encode('utf-8')]));

def getPower(cardName, powerVal):
	dictPower[cardName.encode('utf-8')] = powerVal;
	#print("power "+str(dictPower[cardName.encode('utf-8')]));
def getToughness(cardName, toughnessVal):
	dictToughness[cardName.encode('utf-8')] = toughnessVal;
	#print("toughness "+str(dictToughness[cardName.encode('utf-8')]));

def getRarity(rarityVal):
	if(rarityVal == "Common"):
		#print("Common");
		return "Common";
	elif(rarityVal == "Uncommon"):
		#print("Uncommon");
		return "Uncommon";
	elif(rarityVal == "Rare"):
		#print("Rare");
		return "Rare";
	elif(rarityVal == "Mythic Rare"):
		#print("Mythic Rare");
		return "Mythic Rare";
	else:
		return "Nothing";
	#print("rarity "+str(dictRarity[cardName.encode('utf-8')]));

def getNumberOfPrintings(cardName, printings):
	numOfReprints[cardName.encode('utf-8')] = len(printings);
	#print("reprints "+str(numOfReprints[cardName.encode('utf-8')]));


def getPt(val):
	if "*" in val:
		return 4;
	else:
		return float(val);

if __name__ == "__main__":
	main();