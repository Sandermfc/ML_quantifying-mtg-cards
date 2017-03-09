import tensorflow as tf
import random
import unicodecsv as csv
import numpy as np
import json

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_float('learning_rate', 0.1, 'Initial learning rate.')
flags.DEFINE_integer('max_steps', 2000, 'Number of steps to run trainer.')
flags.DEFINE_integer('display_step', 100, 'Display logs per step.')

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
						if(a < 6):
							writerl.writerow(row)
						elif(a > 5 and a < 8):
							writerv.writerow(row)
						elif(a > 7 and a < 10):
							writert.writerow(row)

def poop(originalText):
	#subfunction
	def poop2(sent):
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
	#Example for numGram = 3
	#for each SENTENCE in the description, do 1 gram;2 gram;3gram on the first 1,2 and 3 words
	#then do 3 gram for the rest of the sentence (do not do 2gram and 1 gram on the last 2 and 1 words)
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
				#print(sentence);
				sentences.append(sentence);
				sentence = [];
			word="";
		else:
			word+=originalText[i];
	ngramcount = 0.0
	for i in range(0,len(sentences)): #for each sentence
		temp1 = poop2(sentences[i]);
		counter = 3
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
		temp1=0.0
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
			

def run_training(train_X, train_Y):
    X = tf.placeholder(tf.float32, [m, n])
    Y = tf.placeholder(tf.float32, [m, 1])

    # weights
    W = tf.Variable(tf.zeros([n, 1], dtype=np.float32), name="weight")
    b = tf.Variable(tf.zeros([1], dtype=np.float32), name="bias")

    # linear model
    activation = tf.add(tf.matmul(X, W), b)
    cost = tf.reduce_sum(tf.square(activation - Y)) / (2*m)
    optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate).minimize(cost)

    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)

        for step in range(FLAGS.max_steps):

            sess.run(optimizer, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})

            if step % FLAGS.display_step == 0:
                print "Step:", "%04d" % (step+1), "Cost=", "{:.2f}".format(sess.run(cost, \
                    feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})), "W=", sess.run(W), "b=", sess.run(b)

        print "Optimization Finished!"
        training_cost = sess.run(cost, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})
        print "Training Cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n'

        #print "Predict.... (Predict a house with 1650 square feet and 3 bedrooms.)"
        					#cmc,desc,numcol,numreprint,power,rarity,tough,release
        temp = "When Protean Hulk is put into a graveyard from play, search your library for any number of creatures cards with total converted mana cost 6 or less and put them into play. Then shuffle your library."
        orginalText = poop(temp)
        predict_X = np.array([7, orginalText,1,1,6,3,6,732345], dtype=np.float32).reshape((1, 8))
        # Do not forget to normalize your features when you make this prediction
        predict_X = (predict_X - mean) / std

        predict_Y = tf.add(tf.matmul(predict_X, W),b)
        print "House price(Y) =", sess.run(predict_Y)


def read_data(filename, read_from_file = True):
    global m, n

    if read_from_file:
        with open(filename) as fd:
            data_list = fd.read().splitlines()

            m = len(data_list) # number of examples
            n = 8 # number of features

            train_X = np.zeros([m, n], dtype=np.float32)
            train_Y = np.zeros([m, 1], dtype=np.float32)

            for i in range(m):
                datas = data_list[i].split(',')
                for j in range(n):
                    train_X[i][j] = float(datas[j][1:len(datas[j])-1]);
                train_Y[i][0] = float(datas[-1][1:len(datas[j])-3])

    return train_X, train_Y


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
	[X, Y] = read_data("splitData/learningData.csv")
	X = normalize(X)
	run_training(X, Y)

	print("main")


if __name__ == "__main__":
	main();