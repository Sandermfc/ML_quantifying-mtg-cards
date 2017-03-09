import os
import json
import re
import operator

keywords = {}

def clean_desc(description, kw):
	keywords = kw
	#Remove stuff that isn't keyword abilities
	description = remove_parentheses(description)
	description = remove_brackets(description)
	description = remove_char(description)
	description = description.replace('and/or', '')
	description = cDiv(description)
	description = clean_array(description)
	kw = description[0]
	newDesc = description[1]
	return [kw, newDesc]

#This function will return an array containing only keyword abilities. TO DO: add something that accepts Flying and flying.
#Also add a way to make multiple word abilities just one element in the array.
def clean_array(arr):
	cleaned = []
	description = []
	for i in range(0, len(arr)):
		if i+1 > len(arr):
			break
		if arr[i].title() in keywords:
			cleaned.append(keywords[arr[i].title()])
			if len(keywords[arr[i].title()].split(' ')) > 1:
				arr.remove(arr[i+1])
		else:
			description = ' '.join([arr[k] for k in range(i, len(arr))])
			break
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
		if not s[i].isalpha():
			s = s.replace(s[i], ' ')
	return s
