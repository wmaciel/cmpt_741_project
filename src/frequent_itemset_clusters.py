__author__ = 'walthermaciel'

import sys
from frequent_itemset import compute_frequent_itemsets

def main(cluster_folder, output_file):
    fp_tmp = []
    for i in xrange(4):
        c_str = cluster_folder + '/c' + str(i) + '.txt'
        tmp_str = cluster_folder + '/out_c' + str(i) + '.txt'
        compute_frequent_itemsets(c_str, tmp_str)
        fp_tmp.append(open(tmp_str, 'r'))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'parameters: cluster_folder , output file
    else:
        main(sys.argv[1], sys.argv[2])
