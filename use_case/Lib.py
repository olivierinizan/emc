import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

FILTERED_PROPERTIES = []

def get_properties(instance):
    properties = set()
    for s,p,o in instance:
        if p not in properties:
            properties.add(p)
    return properties

def get_property_values(prop,instance):
    values = []
    for s,p,o in instance:
        if p == prop:
            values.append(o)
    return values

def compute_shared_unshared_properties(pair):
    i1_properties = get_properties(pair[0])
    i2_properties = get_properties(pair[1])
    
    shared_properties = i1_properties & i2_properties
    unshared_properties = i1_properties ^ i2_properties

    return shared_properties, unshared_properties

def compute_edo_for_a_pair(i1,i2):
        # epsilon: the set of properties with the same values
        # delta: the set of properties with different values
        # omega: the set of unshared properties
        epsilon, delta, omega = [],[],[]
        shared,unshared = compute_shared_unshared_properties((i1,i2))
        
        i1_properties = get_properties(i1)
        i2_properties = get_properties(i2)

        # shared and unsahred properties must cover all properties
        assert(set(list(i1_properties) + list(i2_properties)) == set(list(shared) + list(unshared))) 

        # for each property in shared
        for p in shared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue
            # we not dot want the type here
            if "type" in p:
                continue
            # list of values for instances x and y     
            i1_list_of_values = get_property_values(p,i1)
            i2_list_of_values = get_property_values(p,i2)
            
            # we consider all properties as data properties
            i1_set_of_values = set(i1_list_of_values)
            i2_set_of_values = set(i2_list_of_values)

            i1_and_i2 = i1_set_of_values & i2_set_of_values
            i1_xor_i2 = i1_set_of_values ^ i2_set_of_values
 
            if len(i1_and_i2) != 0:
                epsilon.append(p)
            if len(i1_xor_i2) != 0:
                delta.append(p)
            # we can not have both sets empty 
            if len(i1_and_i2) == 0 and len(i1_xor_i2) ==0:
                raise exception("values/properties exception")

        for p in unshared:
            # filter properties
            if p in FILTERED_PROPERTIES:
                continue
            omega.append(p)

        # sort epsilon, delta omega in oder to use them as dict keys
        epsilon.sort()
        delta.sort()
        omega.sort()

        return epsilon,delta,omega

def clean_uri(uri):
    uri_split = uri.split("/")
    return uri_split[-1]

def clean_uri_on_context(context):
    context_cleaned = []
    for uri in context:
        context_cleaned.append(clean_uri(uri))
    return context_cleaned

def from_cosine_to_triples(uri1,k,file_cosine):
    triples = []
    cosines = []
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        lines_2_loop = get_slice_from_cosine(uri1,0,100,file_cosine)
        for line in lines_2_loop:
            if len(triples) == k:
                break
            tuple_ = eval(cosine_line_correction(line))
            uri = tuple_[0]
            tmp = uri_2_prefix(uri)
            rdf_file = tmp + ".csv"
            try:
                rdf_triples = load_csv(uri,"./triples/" + rdf_file)
                triples.append(rdf_triples)
                cosine = tuple_[1]
                cosines.append(cosine)
            except FileNotFoundError:
                print("File " + "./triples/"+ rdf_file + " not found")
    return triples, cosines 

# TODO change the name
def from_cosine_to_triples2(uri1,uri_start,k,file_cosine):
    triples = []
    cosines = []
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        lines_2_loop = get_top100_start_uri_from_cosine(uri_start,file_cosine)
        for line in lines_2_loop:
            print(line)
            if len(triples) == k:
                break
            tuple_ = eval(cosine_line_correction(line))
            uri = tuple_[0]
            tmp = uri_2_prefix(uri)
            rdf_file = tmp + ".csv"
            try:
                rdf_triples = load_csv(uri,"./triples/" + rdf_file)
                triples.append(rdf_triples)
                cosine = tuple_[1]
                cosines.append(cosine)
            except FileNotFoundError:
                print("File " + "./triples/"+ rdf_file + " not found")
    return triples, cosines 

def get_topK_from_cosine(uri1,k,file_cosine):
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        lines_2_loop = []
        # first line of the file is uri1 ?
        line0 = cosine_line_correction(lines[0])
        tuple0 = eval(line0)
        uri0 = tuple0[0]
        if uri0 == uri1:
            lines_2_loop = lines[1:(k+1)]
        else:
            lines_2_loop = lines[0:k]
    return lines_2_loop

def get_slice_from_cosine(uri1,start,end,file_cosine):
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        lines_2_loop = []
        # first line of the file is uri1 ?
        line0 = cosine_line_correction(lines[0])
        tuple0 = eval(line0)
        uri0 = tuple0[0]
        if uri0 == uri1:
            lines_2_loop = lines[(start+1):(end+1)]
        else:
            lines_2_loop = lines[start:end]
    return lines_2_loop

def get_top100_start_uri_from_cosine(uri2,file_cosine):
    uri_found = False
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        lines_2_loop = []
        for line in lines:
            line_corrected = cosine_line_correction(line)
            tuple_ = eval(line_corrected)
            if tuple_[0] == uri2:
                uri_found = True
            if uri_found and len(lines_2_loop) < 101 :
                lines_2_loop.append(line)
    return lines_2_loop

def cosine_line_correction(line):
    line_corrected = line.replace("(http",'("http')
    line_corrected = line_corrected.replace(",0.",'",0.')
    line_corrected = line_corrected.replace(",1.",'",1.')
    return line_corrected

def uri_2_prefix(uri):
    uri_split = uri.split('/')
    tmp = uri_split[-1]
    tmp = tmp.replace('.','_')
    tmp = tmp.replace('(','_')
    tmp = tmp.replace(')','_')
    tmp = tmp.replace(',','_')
    tmp = tmp.replace("'",'_')
    tmp = tmp.replace('&','_')
    return tmp

def from_triples_to_edo(vec1_triples,top_k_triples):
    edo_s = []
    for triples in top_k_triples:
        edo = compute_edo_for_a_pair(vec1_triples,triples)
        t =(edo[0],edo[1],edo[2],triples[0][0])
        edo_s.append(t)
    return edo_s

def load_csv(uri,file_path):
    triples = []
    with open(file_path,"r") as input_file:
        lines = input_file.readlines()
        for line in lines:
            if not line.startswith("http"):
                continue
            line_split = line.strip().split(",")
            t = (uri,line_split[0],line_split[1])
            triples.append(t)
    return triples

def remove_random_items(lst,x):
    # compute x% len of the list
    len_ = int(len(lst) * x/100)
    for i in range(0,len_):
        lst.remove(random.choice(lst))
    return lst

def load_csv_remove_random(uri,file_path,x):
    triples = []
    with open(file_path,"r") as input_file:
        lines = input_file.readlines()
        lines_remove = remove_random_items(lines[1:],x)
        for line in lines_remove:
            if not line.startswith("http"):
                continue
            line_split = line.strip().split(",")
            t = (uri,line_split[0],line_split[1])
            triples.append(t)
    return triples
           
def load_glove_ressources(file_path):
    glove_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            word = parts[0]
            # keep ressource
            if word.startswith("http://dbpedia.org/resource/"):
                vector = np.array(parts[1:], dtype=np.float32)
                glove_dict[word] = vector
        return glove_dict

def cosine2(vec_reshaped,key2,glove):
    vec2 = glove[key2].reshape(1,-1)
    sim = cosine_similarity(vec_reshaped,vec2) 
    return sim

# glove is glove_dict
def get_others_file(glove,vec1_shaped,prefix,suffix):
    others = []
    keys = list(glove.keys())
    for key2 in keys:
        sim = cosine2(vec1_shaped,key2,glove)
        others.append((key2,sim[0][0]))
    others_sorted = sorted(others, key=lambda item:item[1], reverse=True)
    out_file = prefix + "_" + suffix
    with open(out_file,"w") as output_file:
        for other in others_sorted:
            output_file.write("(" + other[0]+","+str(other[1])+")\n")

def get_others(vectors,vec1_shaped):
    others = []
    glove = load_glove_ressources(vectors)
    keys = list(glove.keys())
    for key2 in keys:
        sim = cosine2(vec1_shaped,key2,glove)
        others.append((key2,sim[0][0]))
    others_sorted = sorted(others, key=lambda item:item[1], reverse=True)
    return others_sorted

def set_dummy(triples):
    dummy = []
    for s,p,o in triples:
        dummy.append((":dummy",p,o))
    return dummy

def compute_j1(triples1,triples2):
    s1 = set(set_dummy(triples1))
    s2 = set(set_dummy(triples2))
    intersection_len = len(s1.intersection(s2))
    union_len = len(s1.union(s2))
    return intersection_len/union_len

def compute_j1_for_topKtriples(shaun_triples,top_10_triples):
    j1s = []
    for triple in top_10_triples:
        j1 = compute_j1(shaun_triples,triple)
        j1s.append(j1)
    return sum(j1s)/len(j1s)

def from_cosine_to_edo(file_cosine,query_triple,k):
    edos = []
    triples = []
    with open(file_cosine) as input_file:
        lines = input_file.readlines()
        for line in lines:
            # we reach nb edos required
            if len(edos) == k:
                break
            line_corrected = cosine_line_correction(line)
            tuple_ = eval(line_corrected)
            uri, cosine = tuple_[0],tuple_[1]
            rdf_file = uri_2_prefix(uri) + ".csv"
            try:
                rdf_triple = load_csv(uri,"./triples/" + rdf_file)
                edo = compute_edo_for_a_pair(query_triple,rdf_triple)
                t = (edo[0],edo[1],edo[2],uri)
                edos.append(t)
                triples.append(rdf_triple)

            except FileNotFoundError:
                print("File " + "./triples/"+ rdf_file + " not found")
    return edos, triples 

def index_contexts(edos,i):
    index = {}
    for edo in edos:
        context = edo[i]
        key = str(context)
        if key not in index:
            index[key] = [0,[]]
        index[key][0] += 1
        index[key][1].append(edo[-1])
    return index

def match_profile(edo,profile):
    if len(profile) == 0:
        return True
    
    param_e,param_d = 4,5

    len_e = len(edo[0])
    len_d = len(edo[1])
    
    ep = profile[0] 
    dp = profile[1]   
    
    #is_e_match = (ep-param_e) <= len_e <= (ep+param_e)
    is_e_match = (ep-param_e) <= len_e
    is_d_match = (dp-param_d) <= len_d <= (dp+param_d)
    return is_e_match and is_d_match

def match_profile2(edo,profile):
    if len(profile) == 0:
        return True
    
    param_e,param_d = 4,5

    len_e = edo[0]
    len_d = edo[1]
    
    ep = profile[0] 
    dp = profile[1]   
    
    #is_e_match = (ep-param_e) <= len_e <= (ep+param_e)
    is_e_match = (ep-param_e) <= len_e
    is_d_match = (dp-param_d) <= len_d <= (dp+param_d)
    return is_e_match and is_d_match

def filter_triples_according_profile(triples,edos,cosines,profile):
    out_triples = []
    out_cosines = []
    assert(len(triples) == len(edos))
    for i in range(len(triples)):
        triple = triples[i]
        edo = edos[i]
        cosine = cosines[i]
        if match_profile(edo,profile):
            out_triples.append(triple)
            out_cosines.append(cosine)
    return out_triples, out_cosines

def profile_detection(edos,param_e,param_d):
    clusters = []
    cluster_found = False
    for edo in edos:
        e_len = len(edo[0])
        d_len = len(edo[1])
        i= find_cluster(e_len,d_len,clusters,param_e,param_d)
        if i != -1:
            # update
            new_e = (clusters[i][0] + e_len)/2
            new_d = (clusters[i][1] + d_len)/2
            clusters[i] = [new_e,new_d]
        # new cluster
        else:
            clusters.append([e_len,d_len])
    return clusters

def find_cluster(e_len,d_len,clusters,param_e,param_d):
    i=0
    for cluster in clusters:
        e_diff = abs(e_len - cluster[0])
        d_diff = abs(d_len - cluster[1])
        if e_diff <= param_e and d_diff <= param_d:
            return i
        i += 1
    return -1

def select_cluster(clusters):
    max_e = 0
    selected_cluster = None
    for cluster in clusters:
        current_e = cluster[0]
        if current_e > max_e:
            max_e = current_e
            selected_cluster = cluster
    return selected_cluster

def save_triples(triples,file_path):
    with open(file_path,"w") as output_file:
        for t in triples:
            output_file.write(t[0] + "," + t[1] + "," + t[2] +"\n")

