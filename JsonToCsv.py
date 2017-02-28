import csv
import os
import json

def main():
	with open("input.csv", "w", newline='', encoding='utf8') as myfile:
		writer = csv.writer(myfile, quotechar = "'", quoting=csv.QUOTE_ALL)
		with open('cmc.json', 'r') as file1:
			cmc = json.load(file1)
		with open('descriptions.json', 'r') as file2:
			description = json.load(file2)
		with open('numOfColors.json', 'r') as file3:
			numOfColors = json.load(file3)
		with open('numOfReprints.json', 'r') as file4:
			numOfReprints = json.load(file4)
		with open('power.json', 'r') as file5:
			power = json.load(file5)
		with open('rarity.json', 'r') as file6:
			rarity = json.load(file6)
		with open('toughness.json', 'r') as file7:
			toughness = json.load(file7)
		#with open('keywords.json', 'r') as file8:
		#	keywords = load(file8)
		with open('setCodes.json', 'r') as file9:
			setTrans = json.load(file9)
			
		for sets in cmc:
			for card in cmc[sets]:
				value1 = cmc[sets][card]
				value2 = description[sets].get(card)
				value3 = numOfColors[sets][card]
				value4 = numOfReprints[sets][card]
				value5 = power[sets][card]
				value6 = rarity[sets][card]
				value7 = toughness[sets][card]
				#value8 = keywords[sets][card]
				#value9 = yearPrinted[sets][card]
				#writer.writerow([value1])
				value2 = value2.replace('\n', '')
				writer.writerow([value1, value2,value3,value4,value5,value6,value7])
				
if __name__ == "__main__":
	main();
