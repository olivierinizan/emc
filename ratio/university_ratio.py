# table and bar chart generation
from Lib import *
import json
from Ratio import *

# we use the convertion of DB/YAGO label to id done previously 
# (files are on serv/reset4)
# the mapping of label to ids is in these 2 files:
DB_IDS = "./University/DB_University_ids"
YAGO_IDS = "./University/YAGO_University_ids"

# And the dicts of triple with ids are:
DB_TRIPLES = "./University/DB_University_triples" 
YAGO_TRIPLES = "./University/YAGO_University_triples"

# r_metric for actor
R_METRICS = "./University/edo_university_index2.r.m"


SAMEAS_PAIR_FILE = "./university/University.Goldstandard.txt"

# the preprocess convert pair lable file to id file
def preprocess():
    pairs = load_pair(SAMEAS_PAIR_FILE) 
    with open(DB_IDS) as input_file:
        d_DB_ids = json.load(input_file)
    with open(YAGO_IDS) as input_file:
        d_YAGO_ids = json.load(input_file)
    d_DB_ids_reversed = reverse_dict(d_DB_ids)
    d_YAGO_ids_reversed = reverse_dict(d_YAGO_ids)

    pairs_reversed = []
    for name1,name2 in pairs:
        id1 = d_DB_ids_reversed[name1]
        id2 = d_YAGO_ids_reversed[name2]
        pairs_reversed.append((id1,id2))
    return pairs_reversed

if __name__ == "__main__":
    # same as stuff
    with open(DB_TRIPLES) as input_file:
        DB_dict = json.load(input_file)
    with open(YAGO_TRIPLES) as input_file:
        YAGO_dict = json.load(input_file)
 
    sameas_pairs_ids = preprocess()
    sameas_r_metrics = compute_r_owlsameas2(sameas_pairs_ids,DB_dict,YAGO_dict)
    sameas_r_metrics_epsilon = compute_r_metrics_for_all_epsilon(sameas_r_metrics)
    sameas_rme_ranked = rank_r_metrics_epsilon(sameas_r_metrics_epsilon)
 
    # assert
    all_same_as = 0
    for item in sameas_rme_ranked:
        all_same_as += item[1]
    assert(all_same_as == 8885)
    
    # all pair stuff
    r_metrics = {}
    with open(R_METRICS) as input_file:
        r_metrics = json.load(input_file)
    r_metrics_epsilon = compute_r_metrics_for_all_epsilon(r_metrics)

    # assert
    all_pair = 0
    for key in r_metrics_epsilon:
        all_pair += r_metrics_epsilon[key]
    assert(all_pair == 241763256)
 
    sameas_rme_pareto = pareto(8885,sameas_rme_ranked)
    # print here data for table
    #compute_sameas_ratio_rank(sameas_rme_pareto,r_metrics_epsilon)

    # print here data for bar chart
    # to print bar chart detail go in Ratio.py and uncomment # print detail section
    print("epsilon\tinitial sameas ratio\tnb sameas > 0.8\tall sameas\tnb sameas > 0.8/all sameas"+"\t"+ "mean ratio" )
 
    initial_ratio =6.601770353113879e-06
    nb_sameas = 1546 
    e1 = []
    e1_r_metrics = compute_r_metrics_for_one_epsilon(r_metrics,e1)
    sameas_e1_r_metrics = compute_r_metrics_for_one_epsilon(sameas_r_metrics,e1)
    compute_sameas_ratio(sameas_e1_r_metrics,e1_r_metrics,initial_ratio,nb_sameas,e1)

    initial_ratio = 0.06575449569976544
    nb_sameas = 841 
    e2 = ['graduatedfrom-inv']
    e2_r_metrics = compute_r_metrics_for_one_epsilon(r_metrics,e2)
    sameas_e2_r_metrics = compute_r_metrics_for_one_epsilon(sameas_r_metrics,e2)
    compute_sameas_ratio(sameas_e2_r_metrics,e2_r_metrics,initial_ratio,nb_sameas,e2)

    initial_ratio = 7.629404743134004e-05
    nb_sameas = 570
    e3 = ['islocatedin']
    e3_r_metrics = compute_r_metrics_for_one_epsilon(r_metrics,e3)
    sameas_e3_r_metrics = compute_r_metrics_for_one_epsilon(sameas_r_metrics,e3)
    compute_sameas_ratio(sameas_e3_r_metrics,e3_r_metrics,initial_ratio,nb_sameas,e3)

    initial_ratio = 0.0297244094488189
    nb_sameas = 151
    e4 = ['graduatedfrom-inv', 'islocatedin']
    e4_r_metrics = compute_r_metrics_for_one_epsilon(r_metrics,e4)
    sameas_e4_r_metrics = compute_r_metrics_for_one_epsilon(sameas_r_metrics,e4)
    compute_sameas_ratio(sameas_e4_r_metrics,e4_r_metrics,initial_ratio,nb_sameas,e4)
