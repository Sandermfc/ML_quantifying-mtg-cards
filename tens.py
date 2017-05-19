import tensorflow as tf
import random
import unicodecsv as csv
import numpy as np
import json
import matplotlib.pyplot as plt
import re
import operator
import os


settings = tf.app.flags
SETTINGS = settings.FLAGS
settings.DEFINE_float('alpha', 5, 'Initial learning rate.')
settings.DEFINE_integer('max_steps', 100000, 'Number of steps to run trainer.')
settings.DEFINE_integer('display_step', 100, 'Display logs per step.')

ngramin = {}

#import csv file
def separateInputs():
	random.seed()
	with open("splitData/input4.csv", "r") as inputfile:
		inputfile.readline()
		with open("splitData/learningData.csv", "w") as learning:
			with open("splitData/testData.csv", "w") as test:
				reader = csv.reader(inputfile,delimiter = ",")
				writerl = csv.writer(learning, quotechar = '"', quoting=csv.QUOTE_ALL)
				writert = csv.writer(test, quotechar = "'", quoting=csv.QUOTE_ALL)
				data = list(reader)
				for row in data:
					a = random.randint(0,9)
					if(a < 8):
						writerl.writerow(row)
					elif(a > 7 and a < 10):
						writert.writerow(row)

def getNGramNum(originalText):
	#subfunction
	def getNGramNum2(sent):
		temp = "";
		temp1 = 0.0
		numWords = numGram;
		for x in range(0, len(sent)):
			temp+=sent[x]+" ";
			if( temp.strip().encode("utf-8") in ngramin):
				temp1 = temp1 + ngramin[temp.strip().encode("utf-8")]
			numWords-=1;
			if(numWords==0):
				break;
		return temp1
	with open("parsedData/ngramVal.json", "r") as file1:
		ngramin = json.load(file1)

		numGram = 3;

		#seperate into sentences and words
		wordSeperators = [' ', '\n'];	
		sentenceSeperators = ['.','(',')',','];
		removeTheseFromFront = [' ','\n','\t'];

		word="";
		sentence = [];
		sentences = [];
		for i in range(0,len(originalText)):
			if(originalText[i] in wordSeperators and word != ""):
				sentence.append(word);
				word="";
			elif(originalText[i] in sentenceSeperators):
				if(word not in wordSeperators and word != ""):
					sentence.append(word);
					sentences.append(sentence);
					sentence = [];
				word="";
			else:
				word+=originalText[i];
		ngramcount = 0.0
		for i in range(0,len(sentences)): #for each sentence
			temp1 = getNGramNum2(sentences[i])
			counter = min(3, len(sentences[i]))
			for j in range(1,len(sentences[i])-numGram+1): #for each word in the sentence starting at word number 2 (we already dealt with all instances of 1st word in upToNGram())
				temp="";
				for k in range(0,numGram): #get the next 3 words
					temp+=sentences[i][j+k]+" ";
				if( temp.strip().encode("utf-8") in ngramin):
					temp1 = temp1 + ngramin[temp.strip().encode("utf-8")]
				counter = counter + 1
			ngramcount += temp1 / counter
		return ngramcount


#change the description to value
def getNGramCount():
	#subfunction
	def upToNGram(sent):

		temp = "";
		numWords = numGram;
		temp1 = 0.0
		for x in range(0, len(sent)):
			temp+=sent[x]+" ";
			if( temp.strip().encode("utf-8") in ngramin):
				temp1 = temp1 + ngramin[temp.strip().encode("utf-8")]
			numWords-=1;
			if(numWords==0):
				break;
		return temp1
	with open("splitData/input2.csv", 'r') as inputfile:
		next(inputfile)
		with open("parsedData/ngramVal.json", "r") as file1:
			with open("splitData/input3.csv", "w") as outputfile:
				ngramin = json.load(file1)
				reader = csv.reader(inputfile,delimiter = ",")
				writer = csv.writer(outputfile, quotechar = '"', quoting=csv.QUOTE_ALL)
				writer.writerow(["cmc","description","numOfColors","numOfReprints","power","rarity","toughness","keywords","releaseDate","price"])
				#Example for numGram = 3
				#for each SENTENCE in the description, do 1 gram;2 gram;3gram on the first 1,2 and 3 words
				#then do 3 gram for the rest of the sentence (do not do 2gram and 1 gram on the last 2 and 1 words)
				numGram = 3;

				#seperate into sentences and words
				wordSeperators = [' ', '\n'];	
				sentenceSeperators = ['.','(',')',','];
				removeTheseFromFront = [' ','\n','\t'];
				data = list(reader)
				for row in data:
					word="";
					sentence = [];
					sentences = [];
					for i in range(0,len(row[1])):
						if(row[1][i] in wordSeperators and word != ""):
							sentence.append(word);
							word="";
						elif(row[1][i] in sentenceSeperators):
							if(word not in wordSeperators and word != ""):
								sentence.append(word);
								#print(sentence);
								sentences.append(sentence);
								sentence = [];
							word="";
						else:
							word+=row[1][i];
					if(word not in wordSeperators and word != ""):
						sentence.append(word);
						#print(sentence);
						sentences.append(sentence);
						sentence = [];
					ngramcount = 0.0
					for i in range(0,len(sentences)): #for each sentence
						temp1 = upToNGram(sentences[i]);
						counter = 3
						for j in range(1,len(sentences[i])-numGram+1): #for each word in the sentence starting at word number 2 (we already dealt with all instances of 1st word in upToNGram())
							temp="";
							for k in range(0,numGram): #get the next 3 words
								temp+=sentences[i][j+k]+" ";
							if( temp.strip().encode("utf-8") in ngramin):
								temp1 = temp1 + ngramin[temp.strip().encode("utf-8")]
							counter = counter + 1
						ngramcount += temp1 / counter
					row[1] = ngramcount

					writer.writerow(row)

#change rarity to value
def rarityChange():
	with open("splitData/input.csv", "r") as inputfile:
		with open("splitData/input2.csv", "w") as outputfile:
			reader = csv.reader(inputfile,delimiter = ',')
			writer = csv.writer(outputfile, quotechar = '"', quoting=csv.QUOTE_ALL)
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
					row[5] = 2.5
				writer.writerow(row)

def run_training(train_X, train_Y, test_X, test_Y):

	X = tf.placeholder(tf.float32)
	Y = tf.placeholder(tf.float32)

	# weights
	W = tf.Variable(tf.zeros([n, 1], dtype=np.float32), name="weight")
	b = tf.Variable(tf.zeros([1], dtype=np.float32), name="bias")

	activation = tf.add(tf.matmul(X, W), b)
	cost = tf.reduce_mean(tf.square(activation - Y)) / (2*m)
	optimizer = tf.train.GradientDescentOptimizer(SETTINGS.alpha).minimize(cost)

	with tf.Session() as sess:
		init = tf.global_variables_initializer()
		sess.run(init)

		for step in range(SETTINGS.max_steps):
			sess.run(optimizer, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})
			if step % SETTINGS.display_step == 0:
				print "Step:", "%04d" % (step+1), "Cost=", "{:.2f}".format(sess.run(cost, \
					feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})), "W=", sess.run(W), "b=", sess.run(b)

		print "Optimization Finished!"
		training_cost = sess.run(cost, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})
		print "Training Cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n'

		testing_cost = sess.run(tf.reduce_mean(tf.square(activation - Y)) / (2*k),feed_dict={X: test_X, Y: test_Y})
		print("Testing cost=", testing_cost)
		print("Absolute mean square loss difference:", abs(training_cost - testing_cost))
		

		#test_X = normalize(test_X)
		predict_Y = tf.add(tf.matmul(test_X, W),b)
		pricePredict = sess.run(predict_Y)
		
		difference = 0
		diffmoyen  = 0
		moyTest = 0
		moyPredict = 0
		for i in range(len(test_Y)):
			difference = test_Y[i] - pricePredict[i]
			diffmoyen += difference
			moyTest = test_Y[i]
			moyPredict = pricePredict[i]
		diffmoyen = diffmoyen / len(test_Y)
		moyPredict = moyPredict[0]
		moyPredict = moyPredict / len(test_Y)
		moyTest = moyTest / len(test_Y)
		print("diffmoyen" + str(diffmoyen))
		print("test moy" + str(moyTest))
		print("test predict" + str(moyPredict))


def read_data(filename, read_from_file = True):
	global m, n

	if read_from_file:
		with open(filename) as fd:
			fd.readline()
			data_list = fd.read().splitlines()

			m = len(data_list) # number of examples
			n = 9 # number of features

			train_X = np.zeros([m, n], dtype=np.float32)
			train_Y = np.zeros([m, 1], dtype=np.float32)

			for i in range(m):
				datas = data_list[i].split(',')
				for j in range(n):
					train_X[i][j] = float(datas[j][1:len(datas[j])-1])
				train_Y[i][0] = float(datas[-1][1:len(datas[j])-3])

	return train_X, train_Y

def read_dataTest(filename, read_from_file = True):
	global k

	if read_from_file:
		with open(filename) as fd:
			fd.readline()
			data_list = fd.read().splitlines()

			k = len(data_list) # number of examples
			l = 9 # number of features

			test_X = np.zeros([k, l], dtype=np.float32)
			test_Y = np.zeros([k, 1], dtype=np.float32)

			for i in range(k):
				datas = data_list[i].split(',')
				for j in range(l):
					test_X[i][j] = float(datas[j][1:len(datas[j])-1]);
				test_Y[i][0] = float(datas[-1][1:len(datas[j])-3])


	return test_X, test_Y

def keywordsCount():
	with open("parsedData/kvals.json") as p:
		prices = json.load(p)

	r = csv.reader(open("splitData/input3.csv"))
	input3 = [l for l in r]

	for k in range(1, len(input3)):
		if input3[k][7] != "[]":
			input3[k][7] = input3[k][7].replace(' ','').replace('[','').replace(']','').replace('\'','')
			temp = input3[k][7].split(",")
			som = 0
			for t in range(0, len(temp)):
				if temp[t][1:] in prices:
					som += prices[temp[t][1:]]
			input3[k][7] = som
		else:
			input3[k][7] = 0
	writer = csv.writer(open('splitData/input4.csv', 'wb'))
	writer.writerows(input3)
	return None


def normalize(train_X):

	global mean, std
	mean = np.mean(train_X, axis=0)
	std = np.std(train_X, axis=0)

	return (train_X - mean) / std

import sys

def main():
	rarityChange()
	getNGramCount()
	separateInputs()
	keywordsCount()
	[X, Y] = read_data("splitData/learningData.csv")
	[test_X, test_Y] = read_dataTest("splitData/testData.csv")
	X = normalize(X)
	test_X = normalize(test_X)
	run_training(X, Y, test_X, test_Y)

	print("main")


if __name__ == "__main__":
	main();