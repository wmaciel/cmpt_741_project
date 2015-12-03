__author__ = 'walthermaciel'

from pyspark import SparkConf, SparkContext, SQLContext
import sys
import pprint
from pyspark.mllib.recommendation import *


def split_votes(row):
    tokens = row.strip().split(',')
    doc_id = int(tokens[0])
    words = tokens[2:]
    map(lambda x: int(x), words)
    out = []
    for w in words:
        out.append((doc_id, w, 1))
    return tuple(out)


def generate_rankings(sc, input_directory):
    # read input
    text_rdd = sc.textFile(input_directory)
    rankings_rdd = text_rdd.flatMap(split_votes)
    return rankings_rdd


def main(input, output):
    # spark specific setup
    conf = SparkConf().setAppName('Word Recommender')
    sc = SparkContext(conf=conf)

    rankings_rdd = generate_rankings(sc, input).cache()

    # trains the model
    model = ALS.trainImplicit(rankings_rdd, 10)

    doc_id_rdd = rankings_rdd.map(lambda (doc_id, w, one): doc_id)
    doc_ids = doc_id_rdd.collect()
    doc_ids = set(doc_ids)

    recommendations = []
    for i in doc_ids:
        products = model.recommendProducts(i, 5)
        rec_row = [i] + products
        recommendations.append(rec_row)

    answer = []
    for r in recommendations:
        a = [r[0]]
        for i in r[1:]:
            a.append(i.product)
        answer.append(a)

    fp_out = open(output, 'w')
    for a in answer:
        fp_out.write(str(a[0]))
        for i in a[1:]:
            fp_out.write(',' + str(i))
        fp_out.write('\n')
    fp_out.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

