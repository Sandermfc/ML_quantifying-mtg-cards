""" Linear Regression Example """

import tflearn
import tensorflow as tf
import random
import unicodecsv as csv
import numpy as np
import json
import matplotlib.pyplot as plt

#settings = tf.app.flags
#SETTINGS = settings.FLAGS
#settings.DEFINE_float('alpha', 3, 'Initial learning rate.')
#settings.DEFINE_integer('max_steps', 10000, 'Number of steps to run trainer.')
#settings.DEFINE_integer('display_step', 100, 'Display logs per step.')

ngramin = {}

#import csv file
def separateInputs():
	random.seed()
	with open("splitData/input4.csv", "r") as inputfile:
		with open("splitData/learningData.csv", "w") as learning:
			with open("splitData/testData.csv", "w") as test:
				reader = csv.reader(inputfile,delimiter = ",")
				writerl = csv.writer(learning, quotechar = '"', quoting=csv.QUOTE_ALL)
				writert = csv.writer(test, quotechar = "'", quoting=csv.QUOTE_ALL)
				data = list(reader)
				for row in data:
					a = random.uniform(0,1)
					if(a < 0.85):
						writerl.writerow(row)
					else:
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

	finalValue = 0.0
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
		with open("parsedData/ngramVal.json", "r") as file1:
			with open("splitData/input3.csv", "w") as outputfile:
				ngramin = json.load(file1)

				reader = csv.reader(inputfile,delimiter = ",")
				writer = csv.writer(outputfile, quotechar = '"', quoting=csv.QUOTE_ALL)
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

					for i in range(0,len(sentences)): #for each sentence
						
						temp1 = upToNGram(sentences[i]);
						finalValue += temp1
						counter = 3
						for j in range(1,len(sentences[i])-numGram+1): #for each word in the sentence starting at word number 2 (we already dealt with all instances of 1st word in upToNGram())
							temp="";
							for k in range(0,numGram): #get the next 3 words
								temp+=sentences[i][j+k]+" ";
							if( temp.strip().encode("utf-8") in ngramin):
								finalValue += ngramin[temp.strip().encode("utf-8")]
							counter = counter + 1
					if not len(sentences) == 0:
						row[1] = finalValue/len(sentences)
					else:
						row[1] = 0
					writer.writerow(row)
					finalValue=0.0

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
					row[5] = 5
				if(row[5] == "Rare"):
					row[5] = 14
				if(row[5] == "Mythic Rare"):
					row[5] = 18
				if(row[5] == "Nothing"):
					row[5] = 12
				writer.writerow(row)

def learn(train_X, train_Y, test_X, test_Y):

	# Linear Regression graph
	net = tflearn.input_data(shape=[None,9])
	net = tflearn.fully_connected(net, 9, activation="relu", name="fully_connected_1")
	net = tflearn.dropout(net, 0.7, name="dropout_1")
	net = tflearn.fully_connected(net, 81, activation="relu", name="fully_connected_2")
	net = tflearn.dropout(net, 0.5, name="dropout_2")
	net = tflearn.fully_connected(net, 1, activation="softplus", name="single_output")
	regression = tflearn.regression(net, optimizer='sgd', loss='mean_square', metric='R2', learning_rate=0.1, name="regression")
	m = tflearn.DNN(regression, tensorboard_verbose=3)
	m.fit(train_X, train_Y, validation_set=0.2, n_epoch=100, show_metric=True, snapshot_epoch=False, run_id="FinalFinal")

	print("\nRegression result:")
	print("Y = " + str(m.get_weights(net.W)) +
	    "*X + " + str(m.get_weights(net.b)))

	pricePredict = m.predict(test_X)
	for i,j in zip(pricePredict, test_Y):
		print(str(i)+" "+str(j))
	print("evaluate: " + str(m.evaluate(test_X, test_Y)))

	m.save("dnn_mtg_price_predictor.tfl")

def test(input_, realValues = None):
	input_ = normalize(input_)
	# Linear Regression graph
	net = tflearn.input_data(shape=[None,9])
	#net = tflearn.layers.normalization.batch_normalization (net, beta=0.0, gamma=1.0, epsilon=1e-05, decay=0.9, stddev=0.002, trainable=True, restore=True, reuse=False, scope=None, name='BatchNormalization')
	net = tflearn.fully_connected(net, 9, activation="relu", name="fully_connected_1")
	net = tflearn.dropout(net, 0.7, name="dropout_1")
	net = tflearn.fully_connected(net, 81, activation="relu", name="fully_connected_2")
	net = tflearn.dropout(net, 0.7, name="dropout_2")
	net = tflearn.fully_connected(net, 1, activation="softplus", name="single_output")
	regression = tflearn.regression(net, optimizer='sgd', loss='mean_square', metric='R2', learning_rate=0.1, name="regression")
	m = tflearn.DNN(regression, tensorboard_verbose=3)

	m.load("dnn_mtg_price_predictor.tfl")
	
	prediction = m.predict(input_)
	if(not realValues is None):
		tot = 0.0
		for i,j in zip(prediction, realValues):
			print(str(i)+" "+str(j))
			tot += i-j
		tot/=len(prediction)
		print("On average, we are off by "+str(tot)+"$")
	else:
		print(prediction)


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


def normalize(train_X):

	global mean, std
	mean = np.mean(train_X, axis=0)
	std = np.std(train_X, axis=0)

	return (train_X - mean) / std

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

import sys
import os

def main():
	
	[test_X, test_Y] = read_dataTest("splitData/testData.csv")
	if len(sys.argv) > 1 and sys.argv[1] == "test":
		test(test_X, test_Y)
	else:
		rarityChange()
		getNGramCount()
		separateInputs()
		keywordsCount()

		[X, Y] = read_data("splitData/learningData.csv")

		X = normalize(X)
		test_X = normalize(test_X)

		learn(X, Y, test_X, test_Y)

if __name__ == "__main__":
	main();