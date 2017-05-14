import os
import json
import re
import operator
import splitdesc as splitd

def main():
	keywords = {}
	with open('keywords2.txt', 'r') as file2:
		for line in file2:
			keywords[line.strip('\n').split(' ')[0]] = line.strip('\n');
	with open("AllSets-x.json") as file2:
		data = json.load(file2)

	[OTD, OTD2] = get_data(data, keywords)

	#Put keywords in a json file.
	with open("keywords.json", 'w') as file4:
		json.dump(OTD, file4)
	#Put descriptions in a json file.
	with open("descriptions.json", 'w') as descfile:
		json.dump(OTD2, descfile)

def get_data(data, keywords):
	sets = {};
	#Get the JSON file
	originalText = ""
	for setN in data:
		if (data[setN]["name"].encode('utf-8') != "Unhinged") and (data[setN]["name"].encode('utf-8') != "Unglued"):
			sets[(data[setN]["code"].encode('utf-8'))] = setN;
	OTD = {} #Original Text Dictionnary
	OTD2 = {}
	#Dictionnary of originalText : Key = card name, value = originalText
	for key, value in sets.items():
		if value in data:
			OT = {}
			OT2 = {}
			for card in data[value]["cards"]:
				if "originalText" in card:
					[cleaned, newdesc] = splitd.clean_desc(card["originalText"].encode('utf-8'), keywords)
					if len(cleaned) > 0:
						OT[card["name"].encode('utf-8')] = cleaned
					else:
						OT[card["name"].encode('utf-8')] = []
					if len(newdesc) > 0:
						OT2[card["name"].encode('utf-8')] = newdesc
					else:
						OT2[card["name"].encode('utf-8')] = []
				else:
					OT[card["name"].encode('utf-8')] = []
					OT2[card["name"].encode('utf-8')] = []
			if len(OT) > 0:
				OTD[data[value]["code"]] = OT
			if len(OT2) > 0:
				OTD2[data[value]["code"]] = OT2
		else:
			print("Set not in dataset.");
	return OTD, OTD2


if __name__ == "__main__":
	main();
