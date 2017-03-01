import tensorflow as tf
import random
import unicodecsv as csv

#import csv file
def separateInputs():
	random.seed()
	with open("splitData/input.csv", "r") as inputfile:
		with open("splitData/learningData.csv", "w") as learning:
			with open("splitData/validationData.csv", "w") as validation:
				with open("splitData/testData.csv", "w") as test:
					reader = csv.reader(inputfile,delimiter = ",")
					writerl = csv.writer(learning, quotechar = "'", quoting=csv.QUOTE_ALL)
					writerv = csv.writer(validation, quotechar = "'", quoting=csv.QUOTE_ALL)
					writert = csv.writer(test, quotechar = "'", quoting=csv.QUOTE_ALL)
					data = list(reader)
					for row in data:
						a = random.randint(0,9)
						if(a < 6):
							writerl.writerow(row)
						elif(a > 5 and a < 8):
							writerv.writerow(row)
						elif(a > 7 and a < 10):
							writert.writerow(row)


#change the description to value

#change keyword to value

#change rarity to value
def rarityChange():
	with open("splitData/input.csv", "r") as inputfile:
		with open("splitData/input2.csv", "w") as outputfile:
			reader = csv.reader(inputfile,delimiter = ",")
			writer = csv.writer(outputfile, quotechar = "'", quoting=csv.QUOTE_ALL)
			data = list(reader)
			for row in data:
				if(row[5] == "Common"):
					row[5] = 1
				if(row[5] == "Uncommon"):
					row[5] = 2
				if(row[5] == "Rare"):
					row[5] = 3
				if(row[5] == "Mythic Rare"):
					row[5] = 4
				if(row[5] == "Nothing"):
					row[5] = 1
				writer.writerow(row)
			
def main():
	rarityChange()
	#separateInputs()
	print("main")


if __name__ == "__main__":
	main();
