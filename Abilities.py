import os
import json
import re
import operator

def main():
	#open the big json file containing our dataset
	with open("AllSets-x.json") as file1:
		data = json.load(file1)
	keywords = {};
	#Create a dictionnary containing all the unique keyword abilities.
	with open('keywords2.txt', 'r') as file2:
		for line in file2:
			keywords[line.strip('\n')] = 0;

	#Get the dictionnary of keywords by card name.
	key_abilities = dict(get_keywords(data, keywords))
	keyword_array = make_keyword_arrays(key_abilities, keywords)


	print(keyword_array["Young Wolf"])
	#Write a JSON file that contains the prices of each ability.
	with open("keywords.json", 'w') as file3:
		json.dump(keyword_array, file3)


def get_keywords(data, keywords):
	sets = {};
	#Get the JSON file
	for setN in data:
		if (data[setN]["name"].encode('utf-8') != "Unhinged") and (data[setN]["name"].encode('utf-8') != "Unglued"):
			sets[(data[setN]["name"].encode('utf-8'))] = setN;

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
		if value[0] == "{":
			del key_abilities[key]
			continue
		if cDiv(remove_char(value))[0] not in keywords:
			del key_abilities[key];
		else:
			if cDiv(remove_char(value))[0] != "Enchant":
				del other_abilities[key];
			else:
				del key_abilities[key]

	#Remove stuff that isn't keyword abilities
	for key, value in key_abilities.items():
		key_abilities[key] = remove_parentheses(key_abilities[key])
		key_abilities[key] = remove_brackets(key_abilities[key])
		key_abilities[key] = remove_char(key_abilities[key])
		key_abilities[key] = key_abilities[key].replace('and/or', '')
		key_abilities[key] = cDiv(key_abilities[key])

	#Print stats
	print("Total", len(OT))
	print("Other", len(other_abilities))

	#Return a dictionnary of keyword abilities
	#key: name of card
	#value: keyword abilities
	return key_abilities

#This function will return a dictionnary of arrays that contain all the keyword abilities of a card
#Key: Name of card
#Value: array of its keyword abilities
def make_keyword_arrays(keywords, keyword_list):
	#Divide key_abilities in one word abilities and multiple word abilities.
	one_word = dict(keywords)
	more_words = dict(keywords)
	for key, value in keywords.items():
		if len(list(filter(None, value))) > 1:
			del one_word[key]
			more_words[key] = list(filter(None, more_words[key]))
		else:
			del more_words[key]
			one_word[key] = list(filter(None, one_word[key]))

	#This will remove non-keyword stuff.
	for key, value in more_words.items():
		more_words[key] = clean_array(value, keyword_list)

	#Put everything together.
	all_abilities = dict(one_word.items() + more_words.items())
	#Print stats
	print('One word', len(one_word))
	print('More words', len(more_words))
	print("Keywords", len(keywords))
	print("All", len(all_abilities))


	return all_abilities


#This function will return an array containing only keyword abilities. TO DO: add something that accepts Flying and flying.
#Also add a way to make multiple word abilities just one element in the array.
def clean_array(arr, keywords):
	cleaned = []
	for i in range(0, len(arr)):
		if arr[i].title() in keywords:
			cleaned.append(arr[i])
		else:
			break
	if len(cleaned) > 0:
		return cleaned
	else:
		return arr

#Devides a string at every capital letter.
def cDiv(s):
	n = re.findall('[A-Z][^A-Z]*', s)
	n2 = []
	for i in range(0,len(n)):
		n2 += n[i].split(' ')
	return filter(None, n2)

def remove_parentheses(s):
	s = re.sub('\(.*?\)',' ', s);
	return s

def remove_brackets(s):
	s = re.sub('\{.*?\}',' ', s);
	return s

def remove_numbers(s):
	s = re.sub('[0-9]','', s);
	return s

def remove_commas(s):
	s = re.sub(',','', s);
	return s

def remove_char(s):
	for i in range(0, len(s)):
		if not s[i].isalpha():
			s = s.replace(s[i], ' ')
	return s

if __name__ == "__main__":
	main();
