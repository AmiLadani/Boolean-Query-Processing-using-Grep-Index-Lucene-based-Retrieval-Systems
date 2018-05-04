import os
import sys
import pickle as pkl
import nltk
import pandas as pands
import time
from inverted_IndexSearch import *

with open("docsIndexed.p","r") as dict_file:                              # loading data from .p file

    dictionaryFile = pkl.load(dict_file)

if __name__ == "__main__":

    f = open("query.txt",'r')

    queryIdentifierList = []
    queryAnswer = []
    TimeStamp = []

    qResult = pands.DataFrame(columns = ["qID","Time"])

    for extra,queryy in enumerate(f):

        ans = []
        qIdentifier = queryy.split(' ')[0]

        queryIdentifierList.append(qIdentifier)
        q_s= preprocessDocs(queryy)

        queryy = q_s.split()
        startTime = time.time()

        for i,word in enumerate(queryy):
            
            if i == 0:
                for i in dictionaryFile[word].items():
                    ans.append(i[0])
            else:
                temporary = []
                for i in dictionaryFile[word].items():
                    temporary.append(i[0])
                ans = list(set(ans).intersection(set(temporary)))

        endTime = time.time()
        fileDescriptor = open("inverted_retrieved_docs.txt",'a')

        for result in ans:                                                       # storing the query identifier and the name of the document the query was found it 
            fileDescriptor.write(str(qIdentifier) + " " + str(result) + " \n")
            print (str(qIdentifier) + " " + str(result) + " \n")

        fileDescriptor.close() 
        TimeStamp.append(float(endTime - startTime))
        queryAnswer.append(ans)

    qResult["qID"] = queryIdentifierList
    ans = pands.DataFrame(columns = ["query_ID","rel_docs"])
    
    ans["query_ID"] = queryIdentifierList
    ans["rel_docs"] = queryAnswer

    outputTime = open("inverted_query_time.txt",'w+')

    for i in range(0,len(TimeStamp)):
        outputTime.write(queryIdentifierList[i]+' '+str(TimeStamp[i])+' \n')

    outputTime.close()
    query_fp = ans