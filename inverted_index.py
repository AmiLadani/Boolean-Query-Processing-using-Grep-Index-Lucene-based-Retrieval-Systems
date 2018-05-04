import os
import pickle as pkl 
import numpy as np
import pandas as pands
import sys
import operator
import re
import nltk
import time

def preprocessDocs(sentence):                                       # stemm words                                
    tokens = totokenize(sentence)

    stemmer = nltk.stem.porter.PorterStemmer()

    stopwords = nltk.corpus.stopwords.words('english')              # remove the stopwords 
    new_sent = ""

    for token in tokens:

        token = token.lower()

        if token not in stopwords:
            new_sent += stemmer.stem(token)
            new_sent += " "

    return new_sent

def totokenize(sentence):                                           # tokenize 

    sentence = re.sub("[^a-zA-Z]+", " ", sentence)          

    tokens = nltk.tokenize.word_tokenize(sentence)

    return tokens        



if __name__ == "__main__":

    with open("docsIndexed.p","wb") as handle:

        dict_inverted = {}                                        
        indexedDoc = 0

        docList = os.listdir("./alldocs")                               
        size = len(docList)                                             

        lim = size / 100                                                
        c = size / 100

        for file in docList:  
                                                                            # iterate for every file
            fileLocation = "./alldocs/" + str(file)                      # create the absolute path

            file_doc = open(fileLocation, "r")                          
            file_doc = preprocessDocs(file_doc.read())                  # pre-process docs

            tokens = totokenize(file_doc)                                # store tokenized words
            for term in tokens:                                          

                if not dict_inverted.__contains__(term):          
                    c = 1                                               
                    doc_dictionary = {}
                    doc_dictionary[file] = 1                       
                    dict_inverted[term] = doc_dictionary     

                else:
                    if file in dict_inverted[term]:               
                        doc_dictionary = dict_inverted[term] 
                        doc_dictionary[file] += 1                  
                        dict_inverted[term] = doc_dictionary 
                    else:
                        c = 1
                        doc_dictionary = dict_inverted[term]     # retrieve stored value
                        doc_dictionary[file] = c                           # assign index
                        dict_inverted[term] = doc_dictionary      # storeit back t
                        
            indexedDoc += 1                                             
            i = indexedDoc

            if(i % (lim) == 0):                                  # progress bar       
                sys.stdout.write("\r[" + "." * (i / c) + "_" +  " " * ((size - i)/ count) + "]" +  str(100*i / float(len(docList))) + "%")
                sys.stdout.flush()                                

        indexed_docs=dict_inverted 

        pkl.dump(indexed_docs, handle)                                  