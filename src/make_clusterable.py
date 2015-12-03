__author__ = 'walthermaciel'

import sys
import copy


def make_empty_row(vocabulary_path):
    fp_vocabulary = open(vocabulary_path, 'r')
    row_dict = {}

    for line in fp_vocabulary:
        word = line.strip()
        row_dict[word] = 0

    fp_vocabulary.close()
    return row_dict


def print_titles_csv(row):
    out_str = 'doc_id'
    row_keys = sorted(row.keys())

    for k in row_keys:
        out_str += ',' + str(k)

    return out_str


def print_row_csv(row, doc_id):
    out_str = str(doc_id)
    row_keys = sorted(row.keys())

    for k in row_keys:
        out_str += ',' + str(row[k])

    return out_str


def output_to_csv(d, output_path):
    fpout = open(output_path, 'w')

    # write column titles
    fpout.write(print_titles_csv(d.items()[0][1]) + '\n')

    # write rows
    for doc_id, row in d.items():
        fpout.write(print_row_csv(row, doc_id) + '\n')


def main(document_word_path, vocabulary_path, output_path, minimum_occurrence):

    # create a row template with an entry for each word
    row_template = make_empty_row(vocabulary_path)

    # Write attribute names
    # fp_out = open(output_path, 'w')
    # fp_out.write(print_titles_csv(row_template) + '\n')

    # Save everything in a dict of dicts
    file_dict = {}
    fp_doc = open(document_word_path, 'r')
    for line in fp_doc:
        tokens = line.strip().split(',')
        doc_id = tokens[0]
        words = tokens[2:]
        row = copy.deepcopy(row_template)
        for w in words:
            row[w] = 1
        file_dict[doc_id] = row
    fp_doc.close()

    # sum the occurrences of each word
    for doc_id, row in file_dict.items():
        for k, v in row.items():
            row_template[k] += v

    # Find which words are relevant
    for k, v in row_template.items():
        if v < minimum_occurrence:
            del row_template[k]

    # Remove the irrelevant words from the main table
    for doc_id, row in file_dict.items():
        for k,v in row.items():
            if not row_template.has_key(k):
                del row[k]

    output_to_csv(file_dict, output_path)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'USAGE ERROR!'
        print 'CORRECT USAGE:\n> make_clusterable.py document_word_path vocabulary_path output_path minimum_occurrence'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
