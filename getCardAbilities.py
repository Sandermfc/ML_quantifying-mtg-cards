import os
import json
import re
import operator
import splitdesc as splitd

def main():
	with open("Keywords-Dict.json") as file1:
		keywords = json.load(file1)
	with open("AllSets-x.json") as file2:
		data = json.load(file2)
	OTD = get_data(data, keywords)
	with open("Set-Card-Abilities.json", 'w') as file4:
		json.dump(OTD, file4)

def get_data(data, keywords):
	sets = {};
	#Get the JSON file
	originalText = ""
	for setN in data:
		if (data[setN]["name"].encode('utf-8') != "Unhinged") and (data[setN]["name"].encode('utf-8') != "Unglued"):
			sets[(data[setN]["code"].encode('utf-8'))] = setN;
	OTD = {} #Original Text Dictionnary
	#Dictionnary of originalText : Key = card name, value = originalText
	for key, value in sets.items():
		if value in data:
			OT = {}
			for card in data[value]["cards"]:
				if "originalText" in card:
					cleaned = splitd.clean_desc(card["originalText"].encode('utf-8'), keywords)[0]
					if len(cleaned) > 0:
						OT[card["name"].encode('utf-8')] = cleaned
			if len(OT) > 0:
				OTD[key] = OT
		else:
			print("Set not in dataset.");
	return OTD


if __name__ == "__main__":
	main();
