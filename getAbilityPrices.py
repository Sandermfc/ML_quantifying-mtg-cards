import os
import json
import re
from collections import defaultdict


def main():
	#open the big json file containing our dataset, I'll refer to this as bigFile from here on out
	with open("AllSets-x.json") as file1:
		data = json.load(file1)
	keywords = {};
	#Create a dictionnary containing all the keyword abilities.
	with open('keywords.json') as file2:
		cards = json.load(file2)

	cp = {}
	for key, value in cards.items():
		cp[key] = getPrices(cards[key])

	AbilityPrices = {}
	for key, value in cp.items():
		for k, v in value.items():
			if k in AbilityPrices:
				AbilityPrices[k] = v + AbilityPrices[k]
			else:
				AbilityPrices[k] = v

	for word in AbilityPrices:
		somme = 0;
		for i in range(0, len(AbilityPrices[word])):
			somme += float(AbilityPrices[word][i][1:])
		AbilityPrices[word] = somme / len(AbilityPrices[word])

	#Write a json file that contains the prices for each ability.
	with open("kvals.json", 'w') as file3:
		json.dump(AbilityPrices, file3)
		file3.close()

def getPrices(abilities):
	prices = {}
	#for each file which has price data
	for fileName in os.listdir('price-by-set'):
		#substring the fileName to get setName
		pos = fileName.find('_');
		setName = fileName[pos+1:len(fileName)-5];

		#open the file
		with open("price-by-set/"+fileName) as file4:
			cardPrices = json.load(file4);

		for key, value in abilities.items():
			if key in cardPrices and len(abilities[key]) > 0:
				prices[key] = (value, cardPrices[key][0])
	ppa = defaultdict(list) #Price Per Ability
	for key, value in prices.items():
		for k in value[0]:
			ppa[k].append(value[1])
	return ppa



if __name__ == "__main__":
	main();
