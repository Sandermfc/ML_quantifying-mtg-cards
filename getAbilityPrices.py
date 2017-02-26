import os
import json
import re

def main():
	#open the big json file containing our dataset, I'll refer to this as bigFile from here on out
	with open("AllSets-x.json") as file1:
		data = json.load(file1)
	keywords = {};
	#Create a dictionnary containing all the keyword abilities.
	with open('keywords.txt', 'r') as file2:
		for line in file2:
			keywords[line.strip('\n')] = 0;

	#Get the dictionnary of single keywords by card name.
	key_abilities = dict(parse_keywords(data, keywords))
	#Write a JSON file that contains the prices of each ability.
	with open("Price-Per-Ability.json", 'w') as file3:
		json.dump(getPrices(key_abilities), file3)

def getPrices(abilities):
	prices = {}
	#for each file which has price data
	for fileName in os.listdir('price-by-set'):
		#substring the fileName to get setName
		pos = fileName.find('_');
		setName = fileName[pos+1:len(fileName)-5];

		#open the file
		with open("price-by-set/"+fileName) as file2:
			cardPrices = json.load(file2);
		for key, value in abilities.items():
			if key in cardPrices:
				prices[key] = (value, cardPrices[key][0])
	ppa = {} #Price Per Ability
	for key, value in prices.items():
		ppa.setdefault(value[0][0],[]).append(value[1]);
	print('Unique abilities', len(ppa))
	return ppa

def parse_keywords(data, keywords):
	sets = {};
	#Get the JSON file
	for setN in data:
		sets[(data[setN]["name"].encode('utf-8'))] = setN;
	#open a text file to write stuff
	writeF = open('abilities.txt', 'w');

	OT = {};  #Dictionnary of originalText : Key = card name, value = originalText
	for key, value in sets.items():
		if value in data:
			for card in data[value]["cards"]:
				if "originalText" in card:
					OT[card["name"].encode('utf-8')] = (card["originalText"].encode('utf-8').splitlines()[0]);
		else:
			print("Set not in dataset.");

	#Create dictionnaries for key abilities and other abilities
	#key = card name, value = ability
	key_abilities = dict(OT);
	other_abilities = dict(OT);
	
	#Now we divid OT in two dictionnaries : keyword abilities and other abilities.
	for key, value in OT.items():
		if value.split()[0] not in keywords:
			del key_abilities[key];
		else:
			if value.split()[0] != "Enchant":
				del other_abilities[key];
			else:
				del key_abilities[key];

	#Remove stuff that isn't keyword abilities
	for key, value in key_abilities.items():
		key_abilities[key] = remove_brackets(key_abilities[key])
		key_abilities[key] = key_abilities[key].replace('and/or', '')
		key_abilities[key] = remove_parentheses(key_abilities[key])
		key_abilities[key] = remove_numbers(key_abilities[key])

	#Divide key_abilities in one word abilities and multiple word abilities.
	one_word = dict(key_abilities)
	more_word = dict(key_abilities)
	for key, value in key_abilities.items():
		if len(list(filter(None, value.split(' ')))) > 1:
			del one_word[key]
			more_word[key] = more_word[key].split(' ')
		else:
			del more_word[key]
			one_word[key] = list(filter(None, one_word[key].split(' ')))


	#Printing factory
	print('One word', len(one_word))
	print('More word', len(more_word))
	print("Keywords", len(key_abilities))
	print("Other", len(other_abilities))
	print("Total", len(OT))

	return one_word


def remove_parentheses(s):
	s = re.sub('\(.*?\)',' ', s);
	return s

def remove_brackets(s):
	s = re.sub('\{.*?\}','', s);
	return s

def remove_numbers(s):
	s = re.sub('[0-9]','', s);
	return s

if __name__ == "__main__":
	main();
