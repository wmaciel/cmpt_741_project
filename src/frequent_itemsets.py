import sys
from pprint import pprint
from pymining import itemmining, assocrules


def find_frequent_itemsets(transactions, support):
    relim_input = itemmining.get_relim_input(transactions)
    item_sets = itemmining.relim(relim_input, min_support=support)
    return item_sets


def generate_association_rules(item_sets, support, confidence):
    rules = assocrules.mine_assoc_rules(item_sets, min_support=support, min_confidence=confidence)
    return rules


def extract_transactions(file_pointer):
    list_of_transactions = []
    list_of_ids = []
    for line in file_pointer:
        tokens = line.strip().split(',')
        words = tokens[2:]
        transaction = tuple(words)
        list_of_transactions.append(transaction)
        list_of_ids.append(tokens[0])
    return tuple(list_of_ids), tuple(list_of_transactions)


def match_rules(transaction, rules):
    recommendations = []
    st = frozenset(transaction)

    for r in rules:
        if st.issuperset(r[0]) and st.isdisjoint(r[1]):
            recommendations.append(r)

    return recommendations


def sort_recommendations(recommendations):
    # Sort recommendations by confidence, which is in the 3rd position of the tuple
    for tid in recommendations:
        recommendations[tid].sort(key=lambda x: x[3], reverse=True)


def generate_recommendation_list(recommendation):
    pick = []
    for r in recommendation:
        if_items, then_items, support, confidence = r
        for item in then_items:
            pick.append((item, confidence))
    return pick


def pick_top_5(r_list):
    picked_set = set()
    top5 = []
    for r in r_list:
        item = r[0]
        if item not in picked_set:
            picked_set.add(item)
            top5.append(item)

    if len(top5) < 5:
        return top5
    else:
        return top5[0:5]


def compute_frequent_itemsets(input, output, min_sup, assoc_min_sup, assoc_min_conf):
    print 'opening file...'
    fp_in = open(input, 'r')

    print 'extracting transactions...',
    ids, transactions = extract_transactions(fp_in)
    fp_in.close()
    print len(transactions)
    pprint(transactions)

    print 'finding frequent itemsets...',
    # 30
    item_sets = find_frequent_itemsets(transactions, int(min_sup))
    print len(item_sets)

    print 'generating association rules...',
    # 20, 0.5
    rules = generate_association_rules(item_sets, int(assoc_min_sup), float(assoc_min_conf))
    print len(rules)

    print 'matching transactions and rules...'
    recommendations = {}
    for i, t in enumerate(transactions):
        tid = ids[i]
        recommends = match_rules(t, rules)
        recommendations[tid] = recommends

    print 'sorting recommendations...'
    sort_recommendations(recommendations)

    print 'organizing in dict form...'
    rec_per_tid = {}
    for tid in recommendations:
        r = recommendations[tid]
        rec_per_tid[tid] = generate_recommendation_list(r)

    print 'picking top5...'
    top5_per_tid = {}
    for tid in rec_per_tid:
        r_list = rec_per_tid[tid]
        top5_per_tid[tid] = pick_top_5(r_list)

    #pprint.pprint(top5_per_tid)
    print 'saving file:', output, '...'
    fp_out = open(output, 'w')
    for doc_id, words in top5_per_tid.items():
        fp_out.write(str(doc_id))
        for w in words:
            fp_out.write(',' + str(w))
        fp_out.write('\n')

if __name__ == "__main__":
    compute_frequent_itemsets(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
