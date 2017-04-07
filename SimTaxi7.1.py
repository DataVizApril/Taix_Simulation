#!/usr/bin/env python
# coding: utf-8
import sys 
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

### Different Method to simulation
### Radius stands for the size of nearby area
method = int(sys.argv[1])
radius = int(sys.argv[2])
no_map = int(sys.argv[3])

#To set the value for parameter
parameter = 0.05

def SimTaxi(method,radius):

	#Get the inflow, outflwo, demand density maps
	class DDMap:
		"""docstring for DDMap"""
		def __init__(self):

			#Read the method and radius from argv
			self.method = method
			self.radius = radius

			self.no_map = no_map


			#The parameter for waiting time

			self.parameter = parameter

			# print parameter
			#Define the size of martix
			#IMPORTANT!!! 
			#"column" stands for "X" value
			#"row" stands for "Y" value
			self.row = 56
			self.column = 99

			#Demand density =  outflow - inflow
			self.DemandDensity = [[0 for j in range(self.column)] for i in range(self.row)]

			if (self.no_map == 1):
				dd_map = open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Data\dd1.csv','r')

			elif (self.no_map == 2):
				dd_map = open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Data\dd2.csv','r')

			elif (self.no_map == 3):
				dd_map = open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Data\dd3.csv','r')

			elif (self.no_map == 4):
				dd_map = open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Data\dd4.csv','r')


			temp_flow =[]

			for i in dd_map:
				temp = i.replace('\n','').split(',')
				for j in temp:
					temp_flow.append(int(j))

			# print test_temp_flow

			for k in range(len(temp_flow)):
				x = k/99
				y = k%99
				#print (x,y)
				self.DemandDensity[x][y] = temp_flow[k]


	#Run simulations for taxi driver
	class SimDrive:
		"""docstring for SimDrive"""
		def __init__(self,method,radius,parameter):

			#Read the method and radius from argv
			self.method = method
			self.radius = radius

			self.parameter = parameter

			#print "The parameter is" + str(self.parameter)

			self.row = 55
			self.column = 98

			#Taxi starts from a random zone
			#IMPORTANT!!! 
			#"column" stands for "X" value
			#"row" stands for "Y" value
			self.nowX = random.randint(0,self.row)
			self.nowY = random.randint(0,self.column)

			self.state = 0

			self.travelTime = 0
			self.waitTime = 0

			self.travelTimeWithPass = 0
			self.travelTimeWithoutPass = 0
			self.totalWaitingTime = 0

			self.totalDriveTime = 0

			self.leftWorkingTime = 0

			# The trip number starts with 1
			self.numTrip = 1

			# Notes the results
			# self.StartZone = []
			# self.EndZone = []

			# self.travel = []
			# self.wait = []
			# self.trasit = []

			# self.test = 0

		# Randomly generate a destination for a passenger's trip
		def gen_passenger_drive(self):

			destX = random.randint(0,self.row)
			destY = random.randint(0,self.column)

			#print "The destination for passenger is : (" + str(destX) + ',' + str(destY) + ')' + '\n'

			return destX,destY

		#Method = 1, "random" : Drive randomly to get a new passenger. 
		def random_drive(self):
			#Generate the destination with some requirments
			destX = random.randint(0,self.row)
			destY = random.randint(0,self.column)

			#print "The expect pick-up zone is : " + '(' +str(destX) + ',' + str(destY) + ')' + '\n'

			return destX,destY

		#Method = 2, "Near Search" : Drive randomly within a area to get a new passenger
		def nearsearch_drive(self):

			x =  self.nowX
			y =  self.nowY

			# r : stands for the the haf 
			r = self.radius

			# print "The raduis is " + str(r)
			setij = []

			for i in range(1,r+1):
			    for j in range(1,r+1):
			        setij.append((x+i,y))
			        setij.append((x-i,y))

			        setij.append((x,y+j))
			        setij.append((x,y-j))

			        setij.append((x+i,y+j))
			        setij.append((x-i,y-j))

			        setij.append((x+i,y-j))
			        setij.append((x-i,y+j))

			setij.append((x,y))
			f_setij = set(setij)

			# print setij

			# print f_setij
			# print len(f_setij)

			final_setij = []

			for i,j in f_setij:
				# if (i < 0) or (j < 0) or (i > self.row - 1) or (j > self.column - 1):
				# 	continue
				# else:
				# 	final_setij.append((i,j))

				if i < 0 and j < 0:
					final_setij.append((i+(r+1),j+(r+1)))

				elif i < 0  and  0 <= j <= 98:
					final_setij.append((i+(r+1),j))

				elif  0 <= i <= 55 and j < 0:
					final_setij.append((i,j+(r+1)))

				elif i < 0 and j > 98:
					final_setij.append((i+(r+1),j-(r+1)))

				elif 0 <= i <= 55 and j > 98:
					final_setij.append((i,j-(r+1)))

				elif i > 55 and j > 98:
					final_setij.append((i-(r+1),j-(r+1)))

				elif i > 55 and  0 <= j <= 98:

					final_setij.append((i-(r+1),j))

				elif i > 55 and j < 0:
					final_setij.append((i-(r+1),j+(r+1)))

				else:
					final_setij.append((i,j))

			# print final_setij

			f_point = random.choice(final_setij)

			# print "The nearby search area includes : " + str(final_setij) + '\n'
			# print "The expect pick-up zone is : " + str(f_point) + '\n'

			destX = f_point[0]
			destY = f_point[1]

			return destX,destY

		def getProbability(self,x,y):

			dd = ddMap.DemandDensity[x][y]

			para = self.parameter

			# if dd > 0:
			probability = 1- math.exp(-para*dd)

			# print probability
			return probability


		def genBestRoute(self,destX,destY):

			bestRouteList = []

			R = abs(destX - self.nowX)+1# R stands for row
			C = abs(destY - self.nowY)+1# C stands for column

			totalProb = [[0 for i in range(C)] for j in range(R)]

			#Get the probability value for starting point
			totalProb[0][0] = self.getProbability(self.nowX,self.nowY)


			# From starting point to expected point can only: Go right and down

			if (self.nowX < destX) and (self.nowY < destY):# Checked !!! 6/12/2016
				#Checked!
				for j in range(1,R):
					totalProb[j][0] = totalProb[j-1][0]*self.getProbability(self.nowX+j,self.nowY)

				for i in range(1,C):
					totalProb[0][i] = totalProb[0][i-1]*self.getProbability(self.nowX,self.nowY+i)

				for j in range(1,R):
					for i in range(1,C):
						totalProb[j][i] = max(totalProb[j-1][i],totalProb[j][i-1])*self.getProbability(self.nowX+j,self.nowY+i)

				bestRouteList.append((destX,destY))

				#Traceback : To get the best route list
				i = C - 1
				j = R - 1

				while i> 0 or j >0:
					if i > 0 and j > 0:
						if totalProb[j][i-1] > totalProb[j-1][i]:
							bestRouteList.append((self.nowX+j, self.nowY+i-1))
							i = i - 1
						else:
							bestRouteList.append((self.nowX+j-1, self.nowY+i))
							j = j - 1

					elif i == 0 and j > 0:
						bestRouteList.append((self.nowX+j-1, self.nowY+i))
						j = j -1

					elif i > 0 and j == 0:
						bestRouteList.append((self.nowX+j, self.nowY+i-1))
						i = i - 1

				# Checked! Starting point is already in the list!!!
				# ###bestRouteList.append((self.nowX,self.nowY))

				# print "The route list is : " + str(bestRouteList)
				# print "The starting point is :" + str(self.nowX) + ' , ' + str(self.nowY)
				# print "The expect ending point is :" + str(destX) + ' , ' + str(destY)

				destination = random.choice(bestRouteList)

				#print 'Destination : '+str(destination)

				f_destX = int(destination[0])
				f_destY = int(destination[1])
				#print f_destX,f_destY
			
			# From starting point to expected point can only: Go left and down
			elif (self.nowX < destX) and (self.nowY > destY):

				for j in range(1,R):
					totalProb[j][0] = totalProb[j-1][0]*self.getProbability(self.nowX+j,self.nowY)

				for i in range(1,C):
					totalProb[0][i] = totalProb[0][i-1]*self.getProbability(self.nowX,self.nowY-i)


				for j in range(1,R):
					for i in range(1,C):
						totalProb[j][i] = max(totalProb[j-1][i],totalProb[j][i-1])*self.getProbability(self.nowX+j,self.nowY-i)

				bestRouteList.append((destX,destY))

				#Traceback : To get the best route list
				i = C - 1
				j = R - 1

				# print "The starting point is " + str(self.nowX) + ',' + str(self.nowY)
				# print "The expect ending point is " + str(destX) + ',' + str(destY)
				# print "The C is " + str(C)
				# print "The R is " + str(R)

				while i> 0 or j >0:
					# print j, i-1
					# print j-1,i
					if i > 0 and j > 0:
						if totalProb[j][i-1] > totalProb[j-1][i]:
							bestRouteList.append((self.nowX+j, self.nowY-i+1))
							# print "Adding point " + str(self.nowX+j) +',' +  str(self.nowY-i+1)
							# print "i,j is" + str(i)+',' +str(j)
							i = i-1	
							# print "i-1,j is" + str(i)+',' +str(j)
						else:
							bestRouteList.append((self.nowX+j-1, self.nowY-i))
							# print "Adding point " + str(self.nowX+j-1)+',' +str(self.nowY-i)
							# print "i,j is" + str(i)+',' +str(j)
							j = j-1
							# print "i,j-1 is" + str(i)+',' +str(j)

					elif i == 0 and j> 0:
						bestRouteList.append(((self.nowX+j-1, self.nowY-i)))
						j = j-1

					elif i > 0 and j == 0:
						bestRouteList.append(((self.nowX+j, self.nowY-i+1)))
						i = i-1

				# print "The route list is : " + str(bestRouteList)
				# print "The starting point is :" + str(self.nowX) + ' , ' + str(self.nowY)
				# print "The expect ending point is :" + str(destX) + ' , ' + str(destY)

				destination = random.choice(bestRouteList)

				#print 'Destination : '+str(destination)

				f_destX = int(destination[0])
				f_destY = int(destination[1])

				# From starting point to expected point can only: Go right and up
			elif (self.nowX > destX) and (self.nowY < destY):# Checked !!! 6/12/2016

				for j in range(1,R):
					totalProb[j][0] = totalProb[j-1][0]*self.getProbability(self.nowX-j,self.nowY)

				for i in range(1,C):
					totalProb[0][i] = totalProb[0][i-1]*self.getProbability(self.nowX,self.nowY+i)

				for j in range(1,R):
					for i in range(1,C):
						totalProb[j][i] = max(totalProb[j-1][i],totalProb[j][i-1])*self.getProbability(self.nowX-j,self.nowY+i)


				bestRouteList.append((destX,destY))

				#Traceback : To get the best route list
				i = C - 1
				j = R - 1

				# print self.nowX,self.nowY
				# print destX,destY
				# print C,R

				while i> 0 or j >0:
					if i > 0 and j > 0:
						if totalProb[j][i-1] > totalProb[j-1][i]:
							bestRouteList.append((self.nowX-j, self.nowY+i-1))
							# print "i,j is" + str(i)+',' +str(j)
							i = i - 1
						else:
							bestRouteList.append((self.nowX-j+1, self.nowY+i))
							# print "i,j is" + str(i)+',' +str(j)
							j = j -1
					elif i == 0 and j > 0:
						bestRouteList.append((self.nowX-j+1, self.nowY+i))
						j = j -1
					elif i > 0  and j == 0:
						bestRouteList.append((self.nowX-j, self.nowY+i-1))
						i = i - 1

				# print "The route list is : " + str(bestRouteList)
				# print "The starting point is :" + str(self.nowX) + ' , ' + str(self.nowY)
				# print "The expect ending point is :" + str(destX) + ' , ' + str(destY)

				destination = random.choice(bestRouteList)
				#print 'Destination : '+str(destination)

				f_destX = int(destination[0])
				f_destY = int(destination[1])

			# From starting point to expected point can only: Go left and up
			elif (self.nowX > destX) and (self.nowY > destY):

				for j in range(1,R):
					totalProb[j][0] = totalProb[j-1][0]*self.getProbability(self.nowX-j,self.nowY)

				for i in range(1,C):
					totalProb[0][i] = totalProb[0][i-1]*self.getProbability(self.nowX,self.nowY-i)

				for j in range(1,R):
					for i in range(1,C):
						totalProb[j][i] = max(totalProb[j-1][i],totalProb[j][i-1])*self.getProbability(self.nowX-j,self.nowY-i)

				bestRouteList.append((destX,destY))

				#Traceback : To get the best route list
				i = C - 1
				j = R - 1

				while i> 0 or j >0:
					if i > 0 and j > 0:
						if totalProb[j][i-1] > totalProb[j-1][i]:
							bestRouteList.append((self.nowX-j, self.nowY-i+1))
							i = i - 1
						else:
							bestRouteList.append((self.nowX-j+1, self.nowY-i))
							j = j - 1
					elif i == 0 and j > 0:

						bestRouteList.append((self.nowX-j+1, self.nowY-i))
						j = j - 1


					elif i > 0  and j == 0:

						bestRouteList.append((self.nowX-j, self.nowY-i+1))
						i = i - 1

				# print "The route list is : " + str(bestRouteList)
				# print "The starting point is :" + str(self.nowX) + ' , ' + str(self.nowY)
				# print "The expect ending point is :" + str(destX) + ' , ' + str(destY)

				destination = random.choice(bestRouteList)
				# print 'Destination : '+str(destination)

				f_destX = int(destination[0])
				f_destY = int(destination[1])

			#From starting point to expected point can only: Go left or right
			elif (self.nowX == destX) and (self.nowY != destY):

				if self.nowY > destY:
					f_destY = random.randint(destY,self.nowY)
				else:
					f_destY = random.randint(self.nowY,destY)

				#print destY,self.nowY
				# print "The Route List is (Y): From" + str(self.nowY) + ' to ' + str(destY)

				f_destX = destX
				# print (self.nowX,self.nowY)
				# print bestRouteList
				# print f_destX,f_destY

			#From starting point to expected point can only: Go up or down
			elif (self.nowX != destX) and (self.nowY == destY):

				if self.nowX > destX:
					f_destX = random.randint(destX,self.nowX)
				else:
					f_destX = random.randint(self.nowX,destX)
				# print destX,self.nowX
				# print "The Route List is (X): From" + str(self.nowX) + ' to ' + str(destX)

				f_destY = destY
				# print (self.nowX,self.nowY)
				# print bestRouteList
				# print f_destX,f_destY

			#Starting point and expected point are same
			elif (self.nowX == destX) and (self.nowY == destY):
				f_destX = destX
				f_destY = destY
				# bestRouteList.append((destX,destY))

				# print f_destX,f_destY
				# print self.nowX,self.nowY

			# print self.nowX,self.nowY
			# print destX,destY
			# print bestRouteList
			# print f_destX,f_destY
			return f_destX,f_destY

		#Method = 3, "learning model": Driver knows the demand density
		def learning_drive(self):

			x =  self.nowX
			y =  self.nowY

			# r : stands for the the haf 
			r = self.radius

			# print "The raduis is " + str(i)
			setij = []

			for i in range(1,r):
			    for j in range(1,r):
			        setij.append((x+i,y))
			        setij.append((x-i,y))

			        setij.append((x,y+j))
			        setij.append((x,y-j))

			        setij.append((x+i,y+j))
			        setij.append((x-i,y-j))

			        setij.append((x+i,y-j))
			        setij.append((x-i,y+j))

			setij.append((x,y))

			f_setij = set(setij)

			final_setij = []

			#Exclude the one outside the boundery 
			for i,j in f_setij:
				# if (i < 0) or (j < 0) or (i > self.row - 1) or (j > self.column - 1):

				if i < 0 and j < 0:
					final_setij.append((i+(r+1),j+(r+1)))

				elif i < 0  and  0 <= j <= 98:
					final_setij.append((i+(r+1),j))

				elif  0 <= i <= 55 and j < 0:
					final_setij.append((i,j+(r+1)))

				elif i < 0 and j > 98:
					final_setij.append((i+(r+1),j-(r+1)))

				elif 0 <= i <= 55 and j > 98:
					final_setij.append((i,j-(r+1)))

				elif i > 55 and j > 98:
					final_setij.append((i-(r+1),j-(r+1)))

				elif i > 55 and  0 <= j <= 98:

					final_setij.append((i-(r+1),j))

				elif i > 55 and j < 0:
					final_setij.append((i-(r+1),j+(r+1)))

				else:
					final_setij.append((i,j))

			# print 'Nearby zones for leanring model is : ' + str(final_setij)
			# print 'Original set is : ' + str(len(setij))
			# print 'Unique set model is : ' + str(len(f_setij))
			# print 'Nearby zones for leanring model is : ' + str(len(final_setij))

			fff_set = set(final_setij)

			# print 'The real set is : ' + str(len(fff_set))

			nearby_h_DD = 0
			destX = x
			destY = y

			k = 0


			for i,j in fff_set:
				# print i,j
				# print ddMap.DemandDensity[i][j]
				if i == self.nowX and j == self.nowY:
					nearby_h_DD = ddMap.DemandDensity[i][j]
					destX = i
					destY = j

				if ddMap.DemandDensity[i][j] > nearby_h_DD:
					nearby_h_DD = ddMap.DemandDensity[i][j]
					destX = i
					destY = j
					# print "The highest zone nearby is : " + str(nearby_h_DD)
			# 	k = k +1

			# print "k = " + str(k)


			# print "The highest zone nearby is : " + '(' +str(destX) + ',' + str(destY) + ')' 
			# print "The highest demand density is : " + str(nearby_h_DD)+ '\n'

			f_destX,f_destY = self.genBestRoute(destX,destY)

			# print "The expect pick-up zone is : " + '(' +str(f_destX) + ',' + str(f_destY) + ')' + '\n'

			return f_destX,f_destY


		#Get the wait time before the a new passenger in a Zone
		#Waiting time =-1/( Parameter*demand-density)*ln(rand(0,1)

		def getWaitTime(self,destX,destY):

			density = ddMap.DemandDensity[destX][destY]

			para = self.parameter

			r_value = random.uniform(0,1)

			waitTime = -1/(para*density)*np.log(r_value)

			# print density,waitTime

			return waitTime

		#Get the travel time between StartZone A to StartZone B based on euclidean distance
		# Travel with a passenger
		def getTravelTime_with_P(self,destX,destY):

			# distance = math.sqrt( math.pow(self.nowX - destX, 2) + math.pow(self.nowY - destY, 2) )

			#print "The travel distance is " + str(distance) +'\n'

			height = abs(destX - self.nowX)# R stands for row
			width = abs(destY - self.nowY)# C stands for column

			distance = (height +  width)*0.5

			travelTime = 4.5137*math.pow(distance,0.5396)

			# print travelTime

			return travelTime

		#Travel without a passenger
		def getTravelTime(self,destX,destY):

			height = abs(destX - self.nowX)# R stands for row
			width = abs(destY - self.nowY)# C stands for column

#			distance = (height + width)

#			travelTime = distance*5

			distance = (height +  width)*0.5

			travelTime = 4.5137*math.pow(distance,0.5396)

			# print travelTime

			return travelTime

		###Taxi has four different states when it drives
		#State = 0: The driver starts to find a new passenger
		#State = 1: The driver waits in a Zone for waitTime
		#State = 2: The driver drives without a passenger
		#State = 3: The driver drives with a passenger
		def Simulation(self):
 
			#State = 0: The driver starts to find a new passenger
			if self.state == 0:
				#Method = 1, "random" : Drive randomly to get a new passenger.
				if self.method == 1:
					destX,destY = self.random_drive()
					#Check whether the starting point equals to ending point
					if (destX == self.nowX) and (destY == self.nowY) : 
						self.waitTime = self.getWaitTime(destX,destY)
						self.state = 1
						# print "Trip "+ str(self.numTrip) + " wait time : " + str(self.waitTime)
						self.totalWaitingTime = self.totalWaitingTime + self.waitTime

					else:
						self.travelTime = self.getTravelTime(destX,destY)
						self.nowX = destX
						self.nowY = destY
						#Change to state: Driving without passengers
						self.state = 2
						# print "Trip "+ str(self.numTrip) + " travel time (without passengers) : " + str(self.travelTime)
						# print "Trip "+ str(self.numTrip) + " elapsed time : " + str(self.travelTime)
						self.travelTimeWithoutPass = self.travelTimeWithoutPass + self.travelTime

				#Method = 2, "Near Search" : Drive randomly within a area to get a new passenger
				elif self.method == 2:
					destX,destY = self.nearsearch_drive()
					#Check whether the starting point equals to ending point
					if (destX == self.nowX) and (destY == self.nowY) : 
						self.waitTime = self.getWaitTime(destX,destY)
						self.state = 1
						# print "Trip "+ str(self.numTrip) + " wait time : " + str(self.waitTime)
						self.totalWaitingTime = self.totalWaitingTime + self.waitTime

					else:
						self.travelTime = self.getTravelTime(destX,destY)
						self.nowX = destX
						self.nowY = destY
						#Change to state: Driving without passengers
						self.state = 2
						self.travelTimeWithoutPass = self.travelTimeWithoutPass + self.travelTime
						# print "Trip "+ str(self.numTrip) + " travel time (without passengers) : " + str(self.travelTime)
						# print "Trip "+ str(self.numTrip) + " elapsed time : " + str(self.travelTime)
				#Method = 3, "learning model": Driver knows the demand density
				elif self.method == 3:
					destX,destY = self.learning_drive()
					#Check whether the starting point equals to ending point
					if (destX == self.nowX) and (destY == self.nowY) : 
						self.waitTime = self.getWaitTime(destX,destY)
						self.state = 1
						self.totalWaitingTime = self.totalWaitingTime + self.waitTime
						# print "Trip "+ str(self.numTrip) + " wait time : " + str(self.waitTime)
					else:
						self.travelTime = self.getTravelTime(destX,destY)
						self.nowX = destX
						self.nowY = destY
						#Change to state: Driving without passengers
						self.state = 2
						self.travelTimeWithoutPass = self.travelTimeWithoutPass + self.travelTime
						# print "Trip "+ str(self.numTrip) + " travel time (without passengers) : " + str(self.travelTime)
						# print "Trip "+ str(self.numTrip) + " elapsed time : " + str(self.travelTime)


			#State = 1: The driver waits in a Zone for waitTime 
			elif self.state == 1:
				if self.waitTime > 0:
					self.waitTime = self.waitTime -1
					self.totalDriveTime = self.totalDriveTime + 1
				else:
					#Method = 1, "random" : Drive randomly to get a new passenger.
					if self.method == 1:

						# print "Trip "+ str(self.numTrip) +" the start zone :"+ '(' + str(self.nowX) + ',' + str(self.nowY) + ')'
						#Generate the destination for passenger randomly
						destX,destY = self.gen_passenger_drive()

						self.travelTime = self.getTravelTime_with_P(destX,destY)

						self.nowX = destX
						self.nowY = destY

						self.state = 3

						self.travelTimeWithPass = self.travelTimeWithPass + self.travelTime

						# print "Trip "+ str(self.numTrip) +" the end zone :" + '(' + str(self.nowX) + ',' + str(self.nowY) + ')'

						# print "Trip "+ str(self.numTrip) + " travel time (with passengers) : " + str(self.travelTime) + '\n' + '\n'


					#Method = 2, "Near Search" : Drive randomly within a area to get a new passenger
					elif self.method == 2:
						# #Generate the destination for passenger randomly
						# print "Trip "+ str(self.numTrip) +" the start zone :"+ '(' + str(self.nowX) + ',' + str(self.nowY) + ')'
						destX,destY = self.gen_passenger_drive()

						self.travelTime = self.getTravelTime_with_P(destX,destY)

						self.nowX = destX
						self.nowY = destY

						self.state = 3

						self.travelTimeWithPass = self.travelTimeWithPass + self.travelTime

						# print "Trip "+ str(self.numTrip) +" the end zone :" + '(' + str(self.nowX) + ',' + str(self.nowY) + ')'

						# print "Trip "+ str(self.numTrip) + " travel time (with passengers) : " + str(self.travelTime) + '\n' + '\n'

					#Method = 3, "learning model": Driver knows the demand density
					elif self.method == 3:
						#Generate the destination for passenger randomly
						# print "Trip "+ str(self.numTrip) +" the start zone :"+ '(' + str(self.nowX) + ',' + str(self.nowY) + ')'
						destX,destY = self.gen_passenger_drive()

						self.travelTime = self.getTravelTime_with_P(destX,destY)

						self.nowX = destX
						self.nowY = destY

						self.state = 3

						self.travelTimeWithPass = self.travelTimeWithPass + self.travelTime

						# print "Trip "+ str(self.numTrip) +" the end zone :" + '(' + str(self.nowX) + ',' + str(self.nowY) + ')'

						# print "Trip "+ str(self.numTrip) + " travel time (with passengers) : " + str(self.travelTime) + '\n' + '\n'

			#State = 2: The driver drives without a passenger
			elif self.state == 2:
				if self.travelTime > 0:
					self.travelTime = self.travelTime - 1
					self.totalDriveTime = self.totalDriveTime + 1
				else:
					self.waitTime = self.getWaitTime(self.nowX,self.nowY)
					self.state = 1
					# print "Trip "+ str(self.numTrip) + " wait time : " + str(self.waitTime)
					self.totalWaitingTime = self.totalWaitingTime + self.waitTime
 
			#State = 3: The driver drives with a passenger
			elif self.state == 3:
				if self.travelTime > 0:
					self.travelTime = self.travelTime - 1
					self.totalDriveTime = self.totalDriveTime + 1
				else:
					#Check for the last trip
					#If the left time is less than 5 min then just go home
					if (600 - self.totalDriveTime) > 5: 
						self.numTrip = self.numTrip + 1
						self.state = 0
					else:
						self.totalDriveTime = 600

	#New a demand density map
	ddMap = DDMap()

	###Check value for demand density map
	#print len(ddMap.DemandDensity)
	#print ddMap.DemandDensity[10]
	#print ddMap.DemandDensity[45]

	TotalAverageTripsNumber = 0.0

	TotalAverageTravelingTime_P = 0
	TotalAverageTravelingTime_No_P = 0
	TotalAverageWaiting = 0

	simulationTime = 1000

	for i in range(simulationTime):

	#Define a maximum working time for a user
	#Working hour : 12 hour
		# workingTime = 720
	#Working hour : 10 hour
		workingTime = 600

		new_driver = SimDrive(method,radius,parameter)

		TripTotalNumber = 0
		AvarageDrivingTime = 0
		TripTotalWrokingHour = 0

		TravelTimeWithPassenger = 0
		TravelTimeWithoutPassenger = 0

		WaitingTime = 0

		#Situation 1: Working hour is 10h, check the number of trips

		# For last trip: when left working hour is less than 5 min then stop working.

		while new_driver.totalDriveTime < workingTime:
			new_driver.Simulation()

			TripTotalNumber = new_driver.numTrip
			TripTotalWrokingHour = new_driver.totalDriveTime

			TravelTimeWithPassenger = new_driver.travelTimeWithPass
			TravelTimeWithoutPassenger = new_driver.travelTimeWithoutPass
			WaitingTime = new_driver.totalWaitingTime

		# print "The total number of Trips within 10h is " + str(TripTotalNumber)
		# print "ttp is " +str(TravelTimeWithPassenger)
		# print "ttnp is " + str(TravelTimeWithoutPassenger)
		# print "waiting is " + str(WaitingTime)

		TotalAverageTripsNumber = TotalAverageTripsNumber + TripTotalNumber

		TotalAverageTravelingTime_P = TotalAverageTravelingTime_P + TravelTimeWithPassenger

		TotalAverageTravelingTime_No_P = TotalAverageTravelingTime_No_P + TravelTimeWithoutPassenger

		TotalAverageWaiting = TotalAverageWaiting + WaitingTime

	#Situation 2: 40 trips check the total working hour
	# while new_driver.numTrip <= 40:
	# 	new_driver.Simulation()
	# 	TripTotalNumber = new_driver.numTrip
	# 	TripTotalWrokingHour = new_driver.totalDriveTime

	#Method = 1, "random" : Drive randomly to get a new passenger. 
	#Method = 2, "Near Search" : Drive randomly within a area to get a new passenger
	#Method = 3, "learning model": Driver knows the demand density

	# if method == 1:
	# 	print "Method = Random" + '\n'
	# elif method == 2:
	# 	print "Method = Near Search" + '\n'
	# 	print "Radius = " + str((radius-1)*0.5) + ' km ' + '\n'
	# elif method == 3:
	# 	print "Method = Learning model" + '\n'
	# 	print "Radius = " + str((radius-1)*0.5) + ' km ' + '\n'

	# print "The totalTrips number is " + str(TotalAverageTripsNumber)


	# print "The average trips number is " + str(TotalAverageTripsNumber/simulationTime)

	# print "The average traveling time with Passengers is " + str(float(TotalAverageTravelingTime_P/simulationTime))
	# print "The average traveling time without Passengers is " + str(float(TotalAverageTravelingTime_No_P/simulationTime))
	# print "The average waiting time is  " + str(float(TotalAverageWaiting/simulationTime))

	# radius + average trips + average traveling time with passengers + average traveling time without + average waiting time

	print str((radius-1)*0.5) + ','+ str(TotalAverageTripsNumber/simulationTime) + ',' + str(float(TotalAverageTravelingTime_P/simulationTime)) + ',' + str(float(TotalAverageTravelingTime_No_P/simulationTime)) + ',' + str(float(TotalAverageWaiting/simulationTime))


#Read the method and radius from command line

sys.stdout = open( str(parameter) +'_'+str(no_map) + '_' + str(method) +'_'+ 'result.csv','w')
print "radius" + ',' + "avg_trips"+ ','+"avg_travelTime_P"+','+"avg_travelTime_no_P"+','+"avg_waitTime"
for i in range(1,radius+1):
	runSim = SimTaxi(method,i)


