import pandas as pd

def prec_recall(retvd_output_file,filename):
   
    file_query = open("query.txt",'r')
    file_output = open("output.txt",'r')    
    file_est_output = open(retvd_output_file)
   
    file_prec_recall = open(filename,'w+')
    file_prec_recall.write("qID" + '\t' + "precision" + '\t' + "recall" + '\n')

    q_ID = []
    for query in file_query:
        q_ID.append(query.split()[0])

    est_output = pd.DataFrame(columns=['query_ID','Doc_ID'])
    act_out = pd.DataFrame(columns=['query_ID','Doc_ID'])

    # processing estimated output
    est_q_list = []  
    est_doc_list = []

    for l in file_est_output:
        q,d,newline = l.split(' ')
        est_q_list.append(q)
        est_doc_list.append(d)

    est_output['query_ID'] = est_q_list
    est_output['Doc_ID'] = est_doc_list

    # processing ground truth
    qrnd_thrth_query = []
    qrnd_thrth_docs = []

    for l in file_output:    
        qrnd_thrth_query.append(l.split()[0])
        qrnd_thrth_docs.append(l.split()[1])

    act_out['query_ID'] = qrnd_thrth_query
    act_out['Doc_ID'] = qrnd_thrth_docs
        
    for q_id in q_ID:

        est_list = list(est_output[est_output['query_ID'] == q_id]['Doc_ID'])        
        true_list = list(act_out[act_out['query_ID'] == q_id]['Doc_ID'])

        tp = len(list(set(est_list).intersection(set(true_list))))
        fp = len(est_list) - tp
        fn = len(true_list) - tp

        if(tp==0 and fp==0 and fn==0):
            prec = 1.0
            recall = 1.0
        elif(tp==0 and (fp>0 or fn>0)):
            prec = 0.0
            recall = 0.0
        else:
            prec = tp/float(len(est_list))
            recall = tp/float(len(true_list))

        file_prec_recall.write(str(q_id)+'\t')
        file_prec_recall.write('%.8f' %prec)
        file_prec_recall.write('\t' + str(recall) + '\n')

    file_prec_recall.close()
    file_output.close()
    file_est_output.close()

prec_recall("grep_retrieved_docs.txt", "grep_precision_and_recall.txt")
prec_recall("inverted_retrieved_docs.txt","inverted_precision_and_recall.txt")
prec_recall("pylucene_retrieved_docs.txt", "pylucene_precision_and_recall.txt")