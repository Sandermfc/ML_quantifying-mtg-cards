import os
import json
import re
import operator

keywords = {}

def main():
	#open the big json file containing our dataset
	with open("AllSets-x.json") as file1:
		data = json.load(file1)
	#Create a dictionnary containing all the unique keyword abilities.
	with open('keywords2.txt', 'r') as file2:
		for line in file2:
			keywords[line.strip('\n')] = 0;

	#Extract keywords returns a tuple. [0]: keyword abilities [1]: Descritpions
	card_keywords = {}
	card_descritpions = {}
	kd = []
	kd = extract_keywords(data)
	card_keywords = kd[0]
	card_descritpions = kd[1]


def extract_keywords(data):
	#Get the dictionnary of keywords by card name.
	both = make_keyword_arrays(only_keywords(dict(get_data(data, 0))))
	key_abilities = both[0]
	descriptions = both[1]
	paragraph2 = make_keyword_arrays(only_keywords(dict(get_data(data, 1))))[0]
	paragraph3 = make_keyword_arrays(only_keywords(dict(get_data(data, 2))))[0]

	all_keywords = key_abilities
	print("Key_abilities",len(key_abilities))


	#Merge dictionnaries
	for key, value in key_abilities.items():
		if key in paragraph2:
			all_keywords[key] =  key_abilities[key] + paragraph2[key]
		if key in paragraph3:
			all_keywords[key] =  key_abilities[key] + paragraph3[key]
	for key, value in paragraph2.items():
		if key in paragraph3:
			paragraph2[key] = paragraph2[key] + paragraph3[key]
			del paragraph3[key]
	for key, value in paragraph2.items():
		all_keywords[key] = paragraph2[key]
	for key, value in paragraph3.items():
		all_keywords[key] = paragraph3[key]

	print("Paragraph 1",len(key_abilities))
	print("Paragraph 2",len(paragraph2))
	print("Paragraph 3",len(paragraph3))
	print("All", len(all_keywords))
	#Write in a file for debugging
	f = open("other.txt", 'w')
	sorted_other = sorted(paragraph3.items(), key=operator.itemgetter(1))
	for key, value in sorted_other:
		f.write("[" + key + "]" + ': ')
		for i in range(0, len(value)):
			f.write(value[i] + ' ')
		f.write('\n')

	#Write a JSON file that contains the prices of each ability.
	with open("keywords.json", 'w') as file3:
		json.dump(all_keywords, file3)

	with open("descriptions.json", 'w') as file4:
		json.dump(descriptions, file4)

	return [all_keywords, descriptions]

def get_data(data, paragraph):
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
					if len(card["originalText"].encode('utf-8').splitlines()) > paragraph:
						OT[card["name"].encode('utf-8')] = card["originalText"].encode('utf-8').splitlines()[paragraph]
		else:
			print("Set not in dataset.");
	return OT

def only_keywords(OT):
	#Create dictionnaries for key abilities and other abilities
	#key = card name, value = ability
	key_abilities = dict(OT);
	other_abilities = dict(OT);

	#Now we divid OT in two dictionnaries : keyword abilities and other abilities.
	for key, value in OT.items():
		if value[0] == "{":
			del key_abilities[key]
			continue
		if len(cDiv(remove_char(value))) < 1:
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
	# print("Total", len(OT))
	# print("Other", len(other_abilities))

	#Return a dictionnary of keyword abilities
	#key: name of card
	#value: keyword abilities
	return key_abilities

#This function will return a dictionnary of arrays that contain all the keyword abilities of a card
#Key: Name of card
#Value: array of its keyword abilities
def make_keyword_arrays(keyword_list):
	#Divide key_abilities in one word abilities and multiple word abilities.
	one_word = dict(keyword_list)
	more_words = dict(keyword_list)
	for key, value in keyword_list.items():
		if len(list(filter(None, value))) > 1:
			del one_word[key]
			more_words[key] = list(filter(None, more_words[key]))
		else:
			del more_words[key]
			one_word[key] = list(filter(None, one_word[key]))

	descriptions = {}
	#This will remove non-keyword stuff.
	for key, value in more_words.items():
		more_words[key] = clean_array(value)[0]
		descriptions[key] = clean_array(value)[1]

	#Put everything together.
	all_abilities = dict(one_word.items() + more_words.items())
	#Print stats
	# print('One word', len(one_word))
	# print('More words', len(more_words))
	# print("Keywords", len(keyword_list))
	# print("All", len(all_abilities))
	return [all_abilities, descriptions]


#This function will return an array containing only keyword abilities. TO DO: add something that accepts Flying and flying.
#Also add a way to make multiple word abilities just one element in the array.
def clean_array(arr):
	cleaned = []
	description = []
	for i in range(0, len(arr)):
		if arr[i].title() in keywords:
			cleaned.append(arr[i])
		else:
			description = ' '.join([arr[k] for k in range(i, len(arr))])
			break
	if len(cleaned) > 0:
		return [cleaned, description]
	else:
		return [arr, description]

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
