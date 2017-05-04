import unicodecsv as csv
import numpy as np
import json
import matplotlib.pyplot as plt
import sys
from matplotlib import pylab
import plotly.plotly as py
import plotly.graph_objs as go

def normalize(train_X):

	global mean, std
	mean = np.mean(train_X, axis=0)
	std = np.std(train_X, axis=0)
	return (train_X - mean) / std

def main():
	with open("splitData/input3.csv", 'r') as inputfile:
		reader = csv.reader(inputfile,delimiter = ",")
		data = list(reader)
		x_cmc = []
		x_description = []
		x_numOfColors = []
		x_numOfReprints = []
		x_power = []
		x_rarity = []
		x_toughness = []
		x_releaseDate = []
		y_price = []
		n = len(data)
		for row in data:
			x_cmc.append(float(row[0].encode("utf-8")))
			x_description.append(float(row[1].encode("utf-8")))
			x_numOfColors.append(float(row[2].encode("utf-8")))
			x_numOfReprints.append(float(row[3].encode("utf-8")))
			x_power.append(float(row[4].encode("utf-8")))
			x_rarity.append(float(row[5].encode("utf-8")))
			x_toughness.append(float(row[6].encode("utf-8")))
			x_releaseDate.append(float(row[7].encode("utf-8")))
			y_price.append(float(row[8].encode("utf-8")))


	x_cmc = normalize(x_cmc)
	x_description = normalize(x_description)
	x_numOfColors = normalize(x_numOfColors)
	x_numOfReprints = normalize(x_numOfReprints)
	x_power = normalize(x_power)
	x_rarity = normalize(x_rarity)
	x_toughness = normalize(x_toughness)
	x_releaseDate = normalize(x_releaseDate)
	y_price = normalize(y_price)

#-----------------------------------------------------------------

	#listc = zip(x_cmc, y_price)
	#listc = sorted(listc)
	#[x_cmc, y_price] = zip(*listc)

	#plt.plot(x_cmc, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_cmc, y_price, 2)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_cmc[0], x_cmc[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_cmc,y_price,'ro')
	#plt.plot(x_new, y_new, '-')
	#         2
	#0.03566 x - 0.07401 x - 0.03566

#-----------------------------------------------------------------

	#listc = zip(x_description, y_price)
	#listc = sorted(listc)
	#[x_description, y_price] = zip(*listc)

	#plt.plot(x_description, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_description, y_price, 5)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_description[0], x_description[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_description,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

	#          5            4           3          2
	#9.72e-05 x - 0.004812 x + 0.07381 x - 0.3591 x + 0.5503 x + 0.01723

#------------------------------------------------------------------

	#listc = zip(x_numOfColors, y_price)
	#listc = sorted(listc)
	#[x_numOfColors, y_price] = zip(*listc)

	#plt.plot(x_numOfColors, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_numOfColors, y_price, 1)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_numOfColors[0], x_numOfColors[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_numOfColors,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

	#-0.01296 x + 6.301e-17

#------------------------------------------------------------------

	#listc = zip(x_numOfReprints, y_price)
	#listc = sorted(listc)
	#[x_numOfReprints, y_price] = zip(*listc)

	#plt.plot(x_numOfReprints, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_numOfReprints, y_price, 5)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_numOfReprints[0], x_numOfReprints[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_numOfReprints,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

    #	        5            4           3          2
	#3.123e-05 x - 0.001432 x + 0.02162 x - 0.1175 x + 0.1829 x + 0.05195

#------------------------------------------------------------------
	
	#listc = zip(x_power, y_price)
	#listc = sorted(listc)
	#[x_power, y_price] = zip(*listc)

	#plt.plot(x_power, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_power, y_price, 2)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_power[0], x_power[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_power,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

	#         2
	#0.01329 x - 0.05062 x - 0.01329

#-------------------------------------------------------------------

	#listc = zip(x_rarity, y_price)
	#listc = sorted(listc)
	#[x_rarity, y_price] = zip(*listc)

	#plt.plot(x_rarity, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_rarity, y_price, 2)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_rarity[0], x_rarity[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_rarity,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

    #  	       2
	#0.004992 x + 0.05619 x - 0.004992

#--------------------------------------------------------------------

	#listc = zip(x_toughness, y_price)
	#listc = sorted(listc)
	#[x_toughness, y_price] = zip(*listc)

	#plt.plot(x_toughness, y_price, 'ro', label='Original data')
	#p = np.polyfit(x_toughness, y_price, 7)
	#f = np.poly1d(p)
	#print f

	#x_new = np.linspace(x_toughness[0], x_toughness[-1], 100)
	#y_new = f(x_new)

	#plt.plot(x_toughness,y_price,'ro')
	#plt.plot(x_new, y_new, '-')

	#            7             6            5           4           3			2
	#-3.626e-05 x + 0.0008285 x - 0.007141 x + 0.02922 x - 0.05931 x + 0.05915 x - 0.02199 x - 0.04356

#-------------------------------------------------------------------
	listc = zip(x_releaseDate, y_price)
	listc = sorted(listc)
	[x_releaseDate, y_price] = zip(*listc)

	plt.plot(x_releaseDate, y_price, 'ro', label='Original data')
	p = np.polyfit(x_releaseDate, y_price, 6)
	f = np.poly1d(p)
	print f

	x_new = np.linspace(x_releaseDate[0], x_releaseDate[-1], 100)
	y_new = f(x_new)

	plt.plot(x_releaseDate,y_price,'ro')
	plt.plot(x_new, y_new, '-')

	#        6            5          4           3          2
	#0.2261 x - 0.007512 x - 0.7398 x + 0.07484 x + 0.5864 x - 0.06682 x - 0.107


	plt.legend()
	plt.show()
if __name__ == "__main__":
	main();