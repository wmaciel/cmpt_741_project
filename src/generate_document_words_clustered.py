__author__ = 'walthermaciel'

import sys
import arff
from pprint import pprint


def main(clustering_file, document_words_file, output):
    print 'Splitting DocumentWords into separate folders for it cluster...'

    print 'Loading', clustering_file
    fp_in = open(clustering_file, 'r')
    arff_dict = arff.load(fp_in)
    fp_in.close()

    print 'Extracting clusters...'
    # {doc_id: cluster_number}
    id_cluster_dict = {}
    for doc_list in arff_dict[u'data']:
        id_cluster_dict[int(doc_list[1])] = int(doc_list[-1][-1])

    print 'Saving clustering for the undergrad answer...'
    fp_undergrad = open(output + '/undergrad_clustering.txt', 'w')
    for k, v in id_cluster_dict.items():
        fp_undergrad.write(str(k) + ',' + str(v) + '\n')
    fp_undergrad.close()

    print 'Preparing output files...'
    # [fp to 'output/c1..4']
    fp_out = []
    for i in xrange(4):
        fp_out.append(open(output + '/c' + str(i) + '.txt', 'w'))

    print 'Distributing docs among cluster files...'
    # fp to DocumentWords.txt
    fp_words = open(document_words_file, 'r')
    for line in fp_words:
        # isolate the document id and the list of words
        tokens = line.strip().split(',')
        doc_id = int(tokens[0])
        words = tokens[2:]

        # find out which cluster this document belongs to
        cluster = id_cluster_dict[doc_id]
        fpc = fp_out[cluster]

        # write document information
        fpc.write(str(doc_id) + ',' + str(len(words)))
        for w in words:
            fpc.write(',' + str(w))
        fpc.write('\n')

    print 'Closing file pointers...'
    # close file pointers
    fp_words.close()
    for fp in fp_out:
        fp.close()

    print 'SUCCESS!'

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'parameters: clustering arff file, document words file, output folder'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
