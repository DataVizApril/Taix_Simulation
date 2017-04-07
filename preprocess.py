#!/usr/bin/env python
# coding: utf-8
import sys 
import random
import math

real_taxi = 25000
sim_taxi = 100


outflow =  open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Uber\outflow.csv','r')

outflow_list = []

for i in outflow:
	temp = i.replace('\n','').split(',')
	for j in range(len(temp)):
		outflow_list.append(int(temp[j]))


sum_outflow = sum(outflow_list)

print "The totol outflow : " + str(sum_outflow)
print "The daily outflow : " + str(sum(outflow_list)/2/365)


real_trip = sum(outflow_list)/2/365/12

# sim_trip : real_trip = sim_taxi: real_taxi
sim_trip = (sim_taxi*real_trip)/real_taxi

#The working hour is 12/day
print "The hourly outflow: " + str(real_trip)

print "The simulated hourly trip with " + str(sim_taxi) + " taxi is " + str(sim_trip)

prob_outflow_list = []

for i in outflow_list:
	prob = float(i)/float(sum_outflow)
	# print i, prob, sum_outflow
	prob_outflow_list.append(prob)

# print max(prob_outflow_list)
 
# inflow

# in_dd =  open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Uber\inflow.csv','r')

# in_dd_list = []

# for i in in_dd:
# 	temp = i.replace('\n','').split(',')
# 	for j in range(len(temp)):
# 		in_dd_list.append(int(temp[j]))

# print "The totol inflow : " + str(sum(in_dd_list))
# print "The daily inflow : " + str(sum(in_dd_list)/2/365)
# print "The hourly inflow: " + str(sum(in_dd_list)/2/365/12)

#Demand density value
# dd =  open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Uber\demand_density.csv','r')

# dd_list = []
 
# for i in dd:
# 	temp = i.replace('\n','').split(',')
# 	for j in range(len(temp)):
# 		dd_list.append(int(temp[j]))

# print dd_list
# print len(dd_list)
# print max(dd_list), min(dd_list)

# c_dd = open('C:\Users\mqzhang\Desktop\Taxi_Simulation\Uber\dd_value.csv','w')

# for k in range(len(dd_list)):
# 	c_dd.write(str(dd_list[k]) + '\n')

# print dd_list
r = random.uniform(0,1)

print "The radom number is " + str(r)

distri_list = []

for i in range(len(prob_outflow_list)):
	k = prob_outflow_list[i]
	if i == 0:
		distri_list.append(k)
	else:
		temp = distri_list[(i-1)] + k
		distri_list.append(temp)

print len(distri_list)
# print distri_list

for j in range(len(distri_list)):
	if distri_list[j] < r and r <= distri_list[j+1]:
		position = j

		print distri_list[j],distri_list[j+1],j

		print (distri_list[j+1] - distri_list[j])
		print (prob_outflow_list[j])
		print (prob_outflow_list[j+1])

		break



