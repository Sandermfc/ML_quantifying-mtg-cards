import tensorflow as tf
import random
import unicodecsv as csv
import numpy as np
import json
import matplotlib.pyplot as plt

settings = tf.app.flags
SETTINGS = settings.FLAGS
settings.DEFINE_float('alpha', 3, 'Initial learning rate.')
settings.DEFINE_integer('max_steps', 10000, 'Number of steps to run trainer.')
settings.DEFINE_integer('display_step', 100, 'Display logs per step.')

ngramin = {}

#import csv file
def separateInputs():
	random.seed()
	with open("splitData/input3.csv", "r") as inputfile:
		with open("splitData/learningData.csv", "w") as learning:
			with open("splitData/validationData.csv", "w") as validation:
				with open("splitData/testData.csv", "w") as test:
					reader = csv.reader(inputfile,delimiter = ",")
					writerl = csv.writer(learning, quotechar = '"', quoting=csv.QUOTE_ALL)
					writerv = csv.writer(validation, quotechar = '"', quoting=csv.QUOTE_ALL)
					writert = csv.writer(test, quotechar = "'", quoting=csv.QUOTE_ALL)
					data = list(reader)
					for row in data:
						a = random.randint(0,9)
						if(a < 8):
							writerl.writerow(row)
						#elif(a > 5 and a < 8):
							writerv.writerow(row)
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

#change keyword to value

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


def polyn(X):
	for i in range(len(X)):
		X[i][0] = 0.03566*pow(X[i][0],2) - 0.07401*X[i][0] - 0.03566
		X[i][1] = 0.0000972*pow(X[i][1], 5) - 0.004812*pow(X[i][1], 4) + 0.07381*pow(X[i][1],3) - 0.3591*pow(X[i][1],2) + 0.5503*X[i][1] + 0.01723
		X[i][2] = -0.01296*X[i][2]
		X[i][3] = 0.00003123*pow(X[i][3],5) - 0.001432*pow(X[i][3],4) + 0.02162*pow(X[i][3],3) - 0.1175*pow(X[i][3],2) + 0.1829*X[i][3] + 0.05195
		X[i][4] = 0.01329*pow(X[i][4],2) - 0.05062*X[i][4] - 0.01329
		X[i][5] = 0.004992*pow(X[i][5],2) + 0.05619*X[i][5] - 0.004992
		X[i][6] = -0.00003626*pow(X[i][6],7) + 0.0008285*pow(X[i][6],6) - 0.007141*pow(X[i][6],5) + 0.02922*pow(X[i][6],4) - 0.05931*pow(X[i][6],3) + 0.05915*pow(X[i][6],2) - 0.02199*X[i][6] - 0.04356
		X[i][7] = 0.2261*pow(X[i][7],6) - 0.007512*pow(X[i][7],5) - 0.7398*pow(X[i][7],4) + 0.07484*pow(X[i][7],3) + 0.5864*pow(X[i][7],2) - 0.06682*X[i][7] - 0.107

def run_training(train_X, train_Y, test_X, test_Y):
	#X = tf.placeholder(tf.float32, [m, n])
	#Y = tf.placeholder(tf.float32, [m, 1])

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

		#test_X = read_dataTest("splitData/testData.csv")
		#test_X = normalize(test_X)

		#print "Predict.... (Predict a house with 1650 square feet and 3 bedrooms.)"
		        					#cmc,desc,numcol,numreprint,power,rarity,tough,release
		#temp = "When Protean Hulk is put into a graveyard from play, search your library for any number of creatures cards with total converted mana cost 6 or less and put them into play. Then shuffle your library."
		#temp = ""
		"""
		temp = "if this attacks and is blocked, you may choose to have it deal its damage to the defending player instead of to the creatures blocking it."
		originalText = getNGramNum(temp)

		#predict_X = np.array([7, originalText,1,1,6,3,6,732345], dtype=np.float32).reshape((1, 8))
		#predict_X = np.array([0, originalText,0,1,1,2,1,733951], dtype=np.float32).reshape((1, 8))
		predict_X = np.array([8, originalText,1,2,7,3,6,729451], dtype=np.float32).reshape((1, 8))
		# Do not forget to normalize your features when you make this prediction
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"3","when this comes into play from your hand, choose and discard a creature card from your hand or destroy this.","1","5","4.0","Rare","4.0","729451","1.67"
		temp = "when this comes into play from your hand, choose and discard a creature card from your hand or destroy this."
		originalText = getNGramNum(temp)
		predict_X = np.array([3,originalText,1,5,4,3,4,729451], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"2","before untapping lands at the start of a turn, each player takes 1 damage for each land he or she controls but did not tap during the previous turn.","1","7","0","Rare","0","727690","110.00"
		temp  = "before untapping lands at the start of a turn, each player takes 1 damage for each land he or she controls but did not tap during the previous turn."
		originalText = getNGramNum(temp)
		predict_X = np.array([2,originalText,1,7,0,3,0,727690], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"2","this can't be blocked except by creatures with flying.this can't be the target of spells or abilities your opponents control.","1","2","1.0","Common","1.0","732253","0.58"
		temp  = "this can't be blocked except by creatures with flying.this can't be the target of spells or abilities your opponents control."
		originalText = getNGramNum(temp)
		predict_X = np.array([2,originalText,1,2,1,1,1,732253], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"4","your black spells cost an additional {b} to play.","1","4","4.0","Rare","4.0","728999","0.33"
		temp  = "your black spells cost an additional {b} to play.","1","4","4.0","Rare","4.0"
		originalText = getNGramNum(temp)
		predict_X = np.array([4,originalText,1,4,4,3,4,728999], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"3","all elves get +1/+1 and have forestwalk. (they're unblockable as long as defending player controls a forest.)","1","7","2.0","Rare","2.0","730302","7.39"
		temp  = "all elves get +1/+1 and have forestwalk. (they're unblockable as long as defending player controls a forest.)"
		originalText = getNGramNum(temp)
		predict_X = np.array([3,originalText,1,7,2,3,2,730302], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"5","return two target cards from your graveyard to your hand. remove this from the game.","1","2","0","Rare","0","730302","0.63"
		temp  = "return two target cards from your graveyard to your hand. remove this from the game."
		originalText = getNGramNum(temp)
		predict_X = np.array([5,originalText,1,2,0,3,0,730302], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"9","flyingat the beginning of your upkeep, you may return target creature card from your graveyard to play.","1","6","4.0","Rare","6.0","730302","1.86"
		temp  = "flyingat the beginning of your upkeep, you may return target creature card from your graveyard to play."
		originalText = getNGramNum(temp)
		predict_X = np.array([9,originalText,1,6,4,3,6,730302], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)

		#"6","vigilancewhenever this enters the battlefield or attacks, you may return target permanent card with converted mana cost 3 or less from your graveyard to the battlefield.","1","6","6.0","Mythic Rare","6.0","734230","2.80"
		temp  = "vigilancewhenever this enters the battlefield or attacks, you may return target permanent card with converted mana cost 3 or less from your graveyard to the battlefield."
		originalText = getNGramNum(temp)
		predict_X = np.array([6,originalText,1,6,6,4,6,734230], dtype=np.float32).reshape((1, 8))
		predict_X = (predict_X - mean) / std
		polyn(predict_X)
		predict_Y = tf.add(tf.matmul(predict_X, W),b)
		print "card price =", sess.run(predict_Y)
		"""
		#plt.plot(train_X, train_Y, 'ro', label='Original data')
		#plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
		#plt.legend()
		#plt.show()


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
					print 1
					test_X[i][j] = float(datas[j][1:len(datas[j])-1]);
				test_Y[i][0] = float(datas[-1][1:len(datas[j])-3])


	return test_X, test_Y

def keywordsCount():
	with open("kvals.json") as p:
		prices = json.load(p)

	r = csv.reader(open("splitData/input3.csv"))
	input3 = [l for l in r]

	for k in range(0, len(input3)):
		if input3[k][7] != "[]":
			input3[k][7] = input3[k][7].translate(None, " []'")
			temp = input3[k][7].split(",")
			som = 0
			for t in range(0, len(temp)):
				if temp[t][1:] in prices:
					som += prices[temp[t][1:]]
			input3[k][7] = som
		else:
			input3[k][7] = 0
	writer = csv.writer(open('splitData/output3.csv', 'wb'))
	writer.writerows(input3)
	return None

def normalize(train_X):

	global mean, std
	mean = np.mean(train_X, axis=0)
	std = np.std(train_X, axis=0)

	return (train_X - mean) / std

import sys

def main():
	#rarityChange()
	#getNGramCount()
	#separateInputs()
	[X, Y] = read_data("splitData/learningData.csv")
	[test_X, test_Y] = read_dataTest("splitData/testData.csv")
	#X = normalize(X)
	#polyn(X)
	#X = normalize(X)
	#print X
	run_training(X, Y, test_X, test_Y)

	print("main")


if __name__ == "__main__":
	main();
