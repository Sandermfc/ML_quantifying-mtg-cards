import os
import json
import re
import operator
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def clean_desc(description, keywords):
	#Get 3 first paragraphes
	para1 = description.splitlines()[0]
	newDesc = ""
	#Remove stuff that isn't keyword abilities
	para1 = remove_parentheses(para1)
	para1 = remove_brackets(para1)
	para1 = remove_char(para1)
	para1 = remove_commas(para1)
	para1 = para1.replace('and/or', '')
	para1 = cDiv(para1)
	para1 = clean_array(para1, keywords)
	kw = list(para1[0])
	if len(para1[1]) > 0:
		newDesc = str(para1[1])
	if len(description.splitlines()) > 1:
		para2 = description.splitlines()[1]
		para2 = remove_parentheses(para2)
		para2 = remove_brackets(para2)
		para2 = remove_char(para2)
		para2 = remove_commas(para2)
		para2 = para2.replace('and/or', '')
		para2 = cDiv(para2)
		para2 = clean_array(para2, keywords)
		kw = kw + list(para2[0])
		if len(para2[1]) > 0:
			newDesc = newDesc + " " + para2[1]

	if len(description.splitlines()) > 2:
		para3 = description.splitlines()[2]
		para3 = remove_parentheses(para3)
		para3 = remove_brackets(para3)
		para3 = remove_char(para3)
		para3 = remove_commas(para3)
		para3 = para3.replace('and/or', '')
		para3 = cDiv(para3)
		para3 = clean_array(para3, keywords)
		kw = kw + list(para3[0])
		if len(para3[1]) > 0:
			newDesc = newDesc + " " + para3[1]


	return [list(set(kw)), newDesc]

#This function will return an array containing only keyword abilities.
def clean_array(arr, keywords):
	cleaned = []
	description = []
	for i in range(0, len(arr)):
		if i+1 > len(arr):
			break
		if arr[i].title() in keywords:
			cleaned.append(keywords[arr[i].title()])
			if len(keywords[arr[i].title()].split(' ')) > 1 and (i+2 < len(arr)):
				arr.remove(arr[i+1])
		else:
			description = ' '.join([arr[k] for k in range(i, len(arr))])
			break
	if description != []:
		for word in keywords:
			if (description.find(keywords[word.title()]) != -1 or description.find(keywords[word.title()].lower()) != -1) and (word != "Battle"):
				cleaned.append(keywords[word.title()])
				description = description.replace(word, '')
		description = description.lower()
	return [cleaned, description]

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
		if not str(s[i]).isalpha() and not '.':
			s = s.replace(s[i], ' ')
	return s
