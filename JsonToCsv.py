import unicodecsv as csv
import os
import json
import io

def main():
	with open("splitData/input.csv", "w") as myfile:
		writer = csv.writer(myfile, quotechar = '"', quoting=csv.QUOTE_ALL)
		writer.writerow(["cmc","description","numOfColors","numOfReprints","power","rarity","toughness","keywords","releaseDate","price"])
		with open('parsedData/cmc.json', 'r') as file1:
			cmc = json.load(file1)
		with open('parsedData/descriptions.json', 'r') as file2:
			description = json.load(file2)
		with open('parsedData/numOfColors.json', 'r') as file3:
			numOfColors = json.load(file3)
		with open('parsedData/numOfReprints.json', 'r') as file4:
			numOfReprints = json.load(file4)
		with open('parsedData/power.json', 'r') as file5:
			power = json.load(file5)
		with open('parsedData/rarity.json', 'r') as file6:
			rarity = json.load(file6)
		with open('parsedData/toughness.json', 'r') as file7:
			toughness = json.load(file7)
		with open('parsedData/keywords.json', 'r') as file8:
			keywords = json.load(file8)
		with open('parsedData/releaseDate.json', 'r') as file9:
			releaseDate = json.load(file9)
		with open('parsedData/price.json', 'r') as file10:
			price = json.load(file10)
		for sets in cmc:
			for card in cmc[sets]:
				value1 = cmc[sets][card]
				value2 = description[sets][card]
				value3 = numOfColors[sets][card]
				value4 = numOfReprints[sets][card]
				value5 = power[sets][card]
				value6 = rarity[sets][card]
				value7 = toughness[sets][card]
				value8 = keywords[sets][card]
				value9 = releaseDate[sets][card]
				value10 = price[sets][card]
				value2 = value2.replace('\n', '')
				writer.writerow([value1,value2,value3,value4,value5,value6,value7,value8,value9,value10])
if __name__ == "__main__":
	main();
