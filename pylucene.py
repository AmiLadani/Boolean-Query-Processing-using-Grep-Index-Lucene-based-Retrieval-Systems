
import sys, lucene
from os import path, listdir
from java.io import File
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.util import Version
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from datetime import datetime

no_tokens = 100000
ABS_PATH = path.dirname(path.abspath(sys.argv[0]))
PATH_INPUT_DIR = ABS_PATH + "/alldocs/"

# lucene and JVM initialization
lucene.initVM()
# creating a new directory
dir = SimpleFSDirectory(File("index_pylucene/"))
# IndexWriter configuration
std_analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
l_analyzer = LimitTokenCountAnalyzer(std_analyzer, no_tokens)
index_config = IndexWriterConfig(Version.LUCENE_CURRENT, l_analyzer)
index_writer = IndexWriter(dir, index_config)

for file_name in listdir(PATH_INPUT_DIR): # iterating over all files in input directory
    print "Indexing file:", file_name
    file_path = PATH_INPUT_DIR + file_name
    f = open(file_path)
    index_doc = Document()
    index_doc.add(StringField("title", file_name, Field.Store.YES))
    index_doc.add(TextField("text", f.read(), Field.Store.YES))
    f.close() # closing file
    index_writer.addDocument(index_doc) # add the document to the IndexWriter

print "\nNo of indexed documents: %d" % index_writer.numDocs()
index_writer.close()
print "Indexing Completed!\n"
print "------------------------------------------------------"

# Creating an index_searcher for defined directory
index_searcher = IndexSearcher(DirectoryReader.open(dir))
# Create a new retrieving analyzer
ret_analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

query_doc = open('updated_query.txt','r')
retrieved_docs = open('pylucene_retrieved_docs.txt','w+')
query_time = open('pylucene_query_time.txt','w+')

for line in query_doc : # iterate over each query in query.txt
    query_id = line[:3]
    query_term = line[4:]
    print "Searching Query:",query_id, query_term
    # query parser
    query_parser = QueryParser(Version.LUCENE_CURRENT, "text", ret_analyzer)
    query_parser.setDefaultOperator(query_parser.Operator.AND)
    query = query_parser.parse(query_term)
    start_time = datetime.now()
    docs_scored = index_searcher.search(query, 50).scoreDocs
    query_time.write(str(query_id)+' '+str(datetime.now() - start_time)+' \n')
    #retrieved_docs.write(str(query_id)+": no_matching_docs: "+str(len(docs_scored))+'\n')

    for s_doc in docs_scored:   # printing retrieved docs
        retrieved_doc = index_searcher.doc(s_doc.doc)
        retrieved_docs.write(str(query_id)+' '+str(retrieved_doc.get("title"))+' \n')

retrieved_docs.close()  #closing files
query_time.close()
query_doc.close()