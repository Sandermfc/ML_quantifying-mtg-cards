import json

ngramin = {};

def getNGramNum(originalText, ngramin):
	#subfunction
	def getNGramNum2(sent):
		temp = "";
		valList = []
		numWords = numGram;
		for x in range(0, len(sent)):
			temp+=sent[x]+" ";
			#print temp.strip().encode('utf-8');
			print temp.strip().encode('utf-8');
			if(temp.strip().encode("utf-8") in ngramin):
				valList.append(ngramin[temp.strip().encode("utf-8")]);
			numWords-=1;
			if(numWords==0):
				break;
		return valList;
	#Example for numGram = 3
	#for each SENTENCE in the description, do 1 gram;2 gram;3gram on the first 1,2 and 3 words
	#then do 3 gram for the rest of the sentence (do not do 2gram and 1 gram on the last 2 and 1 words)
	numGram = 3;

	#seperate into sentences and words
	wordSeperators = [' ', '\n'];
	sentenceSeperators = ['.','(',')',','];
	removeTheseFromFront = [' ','\n','\t'];


	valList = [];
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
	#deal with case where no dot at the end
	if(word not in wordSeperators and word != ""):
		sentence.append(word);
		#print(sentence);
		sentences.append(sentence);
		sentence = [];

	word="";

	print sentences;
	
	ngramcount = 0.0
	for i in range(0,len(sentences)): #for each sentence
		valList = valList + getNGramNum2(sentences[i]);
		counter = min(3, len(sentences[i]));
		for j in range(1,len(sentences[i])-numGram+1): #for each word in the sentence starting at word number 2 (we already dealt with all instances of 1st word in upToNGram())
			temp="";
			for k in range(0,numGram): #get the next 3 words
				temp+=sentences[i][j+k]+" ";
			print temp.strip().encode('utf-8');
			if( temp.strip().encode("utf-8") in ngramin):
				valList.append(ngramin[temp.strip().encode("utf-8")]);
			counter = counter + 1

	valList.sort();
	print(valList);
	finalVal = 0;
	for i in range(0, len(valList)):
		finalVal += valList[i]*i;
	return finalVal/len(valList);


def main():
	with open("parsedData/ngramVal.json") as fp:
		ngramin = json.load(fp);
	print ("shitcock " + str(getNGramNum("draw a card, then lose 2 life.", ngramin)));
	#print ngramin["graveyard other than"];


if __name__ == "__main__":
	main();