import os
import json

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
		#substring the fileName to get setName
		pos = fileName.find('_');
		setName = fileName[pos+1:len(fileName)-5];

		#open the file
		with open("price-by-set/"+fileName) as file2:
			cardPrices = json.load(file2);

		#if setCode exists in bigFile
		if setCode[setName] in data:
			
			###############################################
			###DO STUFF TO SCRAPE INFO FROM THE SET HERE###
			###############################################
			#for each card in the set
			for card in data[setCode[setName]]["cards"]:
				########################################################
				###DO STUFF TO SCRAPE INFO FROM INDIVIDUAL CARDS HERE###
				########################################################
				#if card has an originalText (description), do ngram, otherwise, value becomes 0
				if "originalText" in card:
					#print(card["originalText"].encode('utf-8'));
					getNGramCount(card["originalText"].encode('utf-8'), setName);
				else:
					print("NO ORIGINAL TEXT, GIVING VALUE OF 0");
		else:
			print("ERROR, "+setCode+" does not exist in bigFile");


def getNGramCount(originalText, setName):
	print("do the ngram thing");



if __name__ == "__main__":
	main();