__author__ = 'walthermaciel'

import sys
from frequent_itemsets import compute_frequent_itemsets

def main(cluster_folder, output_file, min_sup, assoc_min_sup, assoc_min_conf ):
    print 'Opening output file:', output_file, '...'
    fp_out = open(output_file, 'w')

    for i in xrange(4):
        c_str = cluster_folder + '/c' + str(i) + '.txt'
        tmp_str = cluster_folder + '/out_c' + str(i) + '.txt'
        print 'Computing frequent itemsets on cluster', i, '...'
        compute_frequent_itemsets(c_str, tmp_str, int(min_sup), int(assoc_min_sup), float(assoc_min_conf))
        print 'Opening temp file...',
        fp_tmp = open(tmp_str, 'r')
        print 'Apending to output file...',
        fp_out.write(fp_tmp.read())
        print 'Done!'
        fp_tmp.close()

    print 'Closing output file...'
    fp_out.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'parameters: cluster_folder , output file, min_sup, assoc_min_sup, assoc_min_conf'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
