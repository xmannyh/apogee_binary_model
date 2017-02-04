import numpy as np

class BFData:
	def __init__(self, locationID='', apogeeID='',ranger=''):
		folder = '/Volumes/CoveyData-1/APOGEE_Spectra/APOGEE2_DR13/Bisector/BinaryFinder/'
		
		self.apogeeID = apogeeID
		self.locationID = locationID
		self.ranger = ranger
		self.filename = folder + str(ranger) + '/' + str(locationID) + '/' + str(apogeeID) + '.tbl'
		self.max1 = []
		self.max2 = []
		self.r = []

		data = np.loadtxt(self.filename, delimiter='\t', dtype=str,skiprows=1)
		for visit in data:
			self.max1.append(visit[2])
			self.max2.append(visit[4])
			self.r.append(visit[5:].astype(float))