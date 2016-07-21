# This is for VS code only.
import vsEnvironSetup
vsEnvironSetup.setVariables()

import mspecGen as mg
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from apogee.modelspec import ferre
import apogee.tools.read as apread

# Current constants
teff1 = 5000.
teff2 = 5250.
logg = 4.7
metals = am = nm = cm = 0.

# Star stuff
visit = 1

# Create parameter arrays
params = [	[teff1, teff2],
			[logg, logg],
			[metals, metals],
			[am, am],
			[nm, nm],
			[cm, cm] ]

# Temperature values for our grid
maxTeff = 5500. # was 7500. need to check for which library to pull from. possibly just check in ferre.interpolate
minTeff = 3500.
rangeTeff = np.linspace(minTeff, maxTeff, num=3)

def printParams(params):
	print('Teff A: ' + str(params[0][0]) + '\tTeff B: ' + str(params[0][1]))
	print('logg A: ' + str(params[1][0]) + '\tlogg B: ' + str(params[1][1]))
	print('metals A: ' + str(params[2][0]) + '\tmetals B: ' + str(params[2][1]))
	print('am A: ' + str(params[3][0]) + '\tam B: ' + str(params[3][1]))
	print('nm A: ' + str(params[4][0]) + '\tnm B: ' + str(params[4][1]))
	print('cm A: ' + str(params[5][0]) + '\tcm B: ' + str(params[5][1]))

def binaryGridFit(locationID, apogeeID, params, visit, rangeTeff):
	'''
	Fits binary via grid by using the magnitude of the maximum from the cross correlation of the binary model
	and continuum-normalized.

	:param locationID: The location ID of the binary.
	:param apogeeID: The apogee ID of the binary.
	:param params: The paramters to test against the observed data.
		format: [ [Teff1, ...], [logg1, ...], [metals1, ...], [am1, ...], [nm1, ...], [cm1, ...]]
	:param visit: The visit to test against.
	:param rangeTeff: The range of teff
	:return: The best fit params
	'''
	peak = np.full((len(rangeTeff), len(rangeTeff)), -1.)

	# Navigate grid
	for i in range(len(rangeTeff)):
		for j in range(len(rangeTeff)):
			# Assign the range values to test in params
			params[0][0], params[0][1] = rangeTeff[i], rangeTeff[j]
			binModel, peak[i][j] = mg.binaryModelGen(locationID, apogeeID, params, visit)
	
	print(np.max(np.max(peak, axis=1), axis=0))
	# Get the max peak value
	peakMax = np.argmax(peak)

	# In case there are multiple equivelant maximums
	fitParams = np.full((6, 2), 0.)
	max1 = int(peakMax / len(rangeTeff))
	max2 = int(peakMax % len(rangeTeff))
	print('Peak max index:' + str(peakMax))
	print(max1)
	print(max2)
	fitParams = [[rangeTeff[max1], rangeTeff[max2]],
					[logg, logg],
					[metals, metals],
					[am, am],
					[nm, nm],
					[cm, cm] ]

	return fitParams

locationID, apogeeID = np.loadtxt('binaries.dat', unpack=True, delimiter=',', dtype=str)
# for i in range(len(locationIDs)):
	# print(locationIDs[i], apogeeIDs[i])
print('Fitting: ' + locationID + ', ' + apogeeID)
badheader, header = apread.apStar(int(locationID), apogeeID, ext=0, header=True)

for visit in range(header['NVISITS']):
	print('---------------VISIT ' + str(visit + 1) + '---------------')
	printParams(binaryGridFit(int(locationID), apogeeID, params, visit + 1, rangeTeff))