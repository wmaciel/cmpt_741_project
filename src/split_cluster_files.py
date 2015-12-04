__author__ = 'walthermaciel'

import sys


def load_cluster_file(file_path):
    fp_in = open(file_path, 'r')
    # {doc_id: cluster_number}
    id_cluster_dict = {}
    for line in fp_in:
        str_doc_id, str_cluster_id = line.strip().split(',')
        doc_id = int(str_doc_id)
        cluster_id = int(str_cluster_id) - 1
        id_cluster_dict[doc_id] = cluster_id
    fp_in.close()
    return id_cluster_dict


def main(clustering_file, document_words_file, output):

    print 'Loading cluster file', clustering_file
    id_cluster_dict = load_cluster_file(clustering_file)

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
        print 'doc_id', doc_id,
        # find out which cluster this document belongs to
        cluster = id_cluster_dict[doc_id]
        print 'belongs to cluster', cluster
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
        print 'parameters: clustering file, document words file, output folder'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
