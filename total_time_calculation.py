import time as tym

def calc_time_pylucene(filename):								
	file = open(filename,'r')
	time = []

	for index in file:
		q,time = index.split('.')
		r = time.split(' ')[0]
		time.append(r)

	totalTime=0.0	
	for t in time:
		totalTime = totalTime + float(t)
	return totalTime

def calc_time_grep(filename):									
	file = open(filename,'r')								
	time = []	

	for index in file:										
		q,time,n_line = index.split(' ')						
		time.append(time)									
	totalTime = 0.0	

	for t in time:										
		totalTime = totalTime + float(t)
	return totalTime											

def calc_time_invertedIndex(filename):							
	file = open(filename,'r')								
	time = []	

	for index in file:										
		q,time,n_line = index.split(' ')						
		time.append(time)									
	totalTime = 0.0	

	for t in time:										
		totalTime=totalTime + float(t)
	return totalTime											




time_grep=calc_time_grep("grep_query_time.txt")
print "Time taken by grep= " + str(time_grep)

time_inverted=calc_time_invertedIndex("inverted_query_time.txt")
print "Time taken by inverted index= " + str(time_inverted)

time_pylucene=calc_time_pylucene("pylucene_query_time.txt")
time_pylucene=s_pylucene*1e-6
print "Time taken by pylucene= " + str(time_pylucene)
