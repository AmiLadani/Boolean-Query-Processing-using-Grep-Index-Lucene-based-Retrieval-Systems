#17CS60R85
import subprocess
import time as t

query_doc = open('query.txt','r')
retrieved_docs = open('grep_retrieved_docs.txt','w+')
query_time = open('grep_query_time.txt','w+')

for query in query_doc :
    print query
    start_time = t.time()
    query_id = query[0:3]
    query_value = query[4:]

    docs_retrieved = set()
    query_terms = query_value.split(' ') 
    term_count = 0
    
    for term in query_terms:
        proc = subprocess.Popen(['grep','-lr',term,'alldocs'], stdout=subprocess.PIPE)
        output = str(proc.stdout.read())
        doc_id = output.split('\n')

        if term_count == 0:
            docs_retrieved = set(doc_id)
            term_count += 1
        else:
            docs_retrieved = set(doc_id) & docs_retrieved

    docs_retrieved = list(docs_retrieved)

    print str(query_id)+': no_matching_docs: '+str(len(docs_retrieved)-1)+"\n"
    for answers in docs_retrieved :
        if answers == "":
            continue
        retrieved_docs.write(str(query_id)+' '+str(answers.split("/")[-1])+' \n')
    #retrieved_docs.write('\n')
      
    query_time.write(str(query_id)+" "+str(t.time()-start_time)+" \n")

retrieved_docs.close()
query_time.close()
query_doc.close()