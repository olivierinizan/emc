from Lib import *
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, XSD, ConjunctiveGraph
from urllib.parse import quote


COSINE_FILE = './Adam_May__footballer__xaa'
VEC1_CSV = './triples/Adam_May__footballer_.csv'
VEC1_URI = "http://dbpedia.org/resource/Adam_May_(footballer)"
SLICE_PARAM = 100

PREFIX = "http://example.org/emc/"
NAMED_GAPH_PREFIX = "http://emc.org/"

def index_named_graphs_and_hasCosine_min_max_predicate(cosine_interval,g):
    index = {}
    ng = 0
    for item in cosine_interval:
        if len(item[2]) == 0:
            continue
        key = str(item[0]) + "-" + str(item[1])
        name = "g" + str(ng)
        ng +=1
        index[key] = name
       
        # has cosineMin/Max predicate
        ng_s = URIRef(PREFIX+name)
        ng_p_min = URIRef(PREFIX+"hasCosineMin")
        ng_o_min = Literal(item[0])
        g.add((ng_s,ng_p_min,ng_o_min))
        ng_p_max = URIRef(PREFIX+"hasCosineMax")
        ng_o_max = Literal(item[1])
    return index

def neighborRdf2Vec_predicates(index_named_graph,cosine_interval,VEC1_URI,g):
    for item in cosine_interval:
        if len(item[2]) == 0:
            continue
        key = str(item[0]) + "-" + str(item[1])
        name = index_named_graph[key]
        for uri in item[2]:
            #print(VEC1_URI + " " + PREFIX+"neighbor" + " " + uri + " " + name)
            s = URIRef(quote(VEC1_URI,safe=":/")) 
            p = URIRef(PREFIX+"neighbor")
            o = URIRef(quote(uri,safe=":/"))
            
            ng = URIRef(quote(NAMED_GAPH_PREFIX+name,safe=":/"))
            g.add((s,p,o,ng))

def load_cosines_and_uris():
    k = 51
    cosines_and_uris = []
    # load cosine file
    with open(COSINE_FILE) as input_file:
        lines = input_file.readlines()
        for line in lines:
            # we reach nb edos required
            if len(cosines_and_uris) == k:
                break
            line_corrected = cosine_line_correction(line)
            tuple_ = eval(line_corrected)
            uri, cosine = tuple_[0],tuple_[1]
            cosines_and_uris.append((uri,cosine))
    return cosines_and_uris

def generate_cosine_interval(step):
    index = []
    binf = 0
    while True:
        if binf > 1:
            break
        binf = round(binf,2)
        bsup = round((binf + step),2)
        index.append([binf,bsup,[]])
        binf = bsup 
    return index

def affect_cosine_to_interval(keys,cosines_and_uris):
    for item in cosines_and_uris:
        uri = item[0]
        cosine = item[1]
        for key in keys:
            binf = key[0]
            bsup = key[1]
            if not binf <= cosine <= bsup:
                continue
            key[2].append(uri)


def includes_predicate(context,context_label,d_context,graphe):
    d_context[str(context)] = context_label
    # add includes predicate for epsilon
    s_ttl = URIRef(PREFIX+d_context[str(context)])
    g.add( (s_ttl,URIRef(PREFIX+"size"),Literal(len(context),datatype=XSD.integer)) )
    g.add( (s_ttl,URIRef(RDF.type),URIRef(PREFIX+"Context")) )
    for prop in context:
        prop_ttl = URIRef(PREFIX+prop) if ":" not in prop else URIRef(prop)
        g.add((s_ttl,URIRef(PREFIX+"includes"),prop_ttl))


def emc_subPropertyOf_predicate(emcs,d_epsilon,d_delta,d_omega,g):
    dr_epsilon = revert_dict(d_epsilon)
    dr_delta = revert_dict(d_delta)
    dr_omega = revert_dict(d_omega)
    for emc1 in emcs:
        for emc2 in emcs:
            if emc1 == emc2:
                continue
            e1_str,d1_str,o1_str = split_emc_str(emc1)
            e2_str,d2_str,o2_str = split_emc_str(emc2)
            se_1 = set(eval(dr_epsilon[e1_str]))
            se_2 = set(eval(dr_epsilon[e2_str]))
            sd_1 = set(eval(dr_delta[d1_str]))
            sd_2 = set(eval(dr_delta[d2_str]))
            # check subPropertyOf
            if (se_2.issubset(se_1) and sd_1.issubset(sd_2)):
                # emc1 subPropertyOf emc2
                emc1_ttl = URIRef(PREFIX+emc1)
                emc2_ttl = URIRef(PREFIX+emc2)
                g.add((emc1_ttl,RDFS.subPropertyOf,emc2_ttl))
def split_emc_str(emc):
    emc_split = emc.split("_")
    e = "e_" + emc_split[3]
    d = "d_" + emc_split[5]
    o = "o_" + emc_split[7]
    return e,d,o

def revert_dict(d):
    d_reverted = {}
    for key in d:
        if d[key] in d_reverted:
            raise Exception()
        d_reverted[d[key]] = key
    return d_reverted

if __name__ == "__main__":
   
    k = 51
    # compute edos for adam and its 50
    shaun_triples = load_csv(VEC1_URI,VEC1_CSV)
    edos,triples = from_cosine_to_edo(COSINE_FILE,shaun_triples,k)
    # adam and its 50 in the graph
    #g = Graph()
    g = ConjunctiveGraph()
    '''
    for entity_triples in triples:
        for s,p,o in entity_triples:
            s_ttl = URIRef(quote(s,safe=":/")) 
            p_ttl = URIRef(quote(p,safe=":/"))
            o_ttl = Literal(quote(o)) if "http" not in o else URIRef(quote(o,safe=":/"))
            g.add((s_ttl,p_ttl,o_ttl))
    ''' 
    # edo
    e_index = 0
    d_index = 0
    o_index = 0
    # we need to index emc:e, emc:d, emc:o
    d_epsilon = {}
    d_delta = {}
    d_omega = {}
    emcs = []
    for edo in edos[1:]:
        # index all iswc:e, iswc:d, iswc:o 
        edo_py = edo[:-1]

        # 3.2.1 include predicate
        # include predicate for e  
        e = edo_py[0]    
        if str(e) not in d_epsilon:
            includes_predicate(e,"e_" + str(e_index),d_epsilon,g)
            e_index += 1
        e_label = d_epsilon[str(e)]
        
        # include predicate for d  
        d = edo_py[1]    
        if str(d) not in d_delta:
            includes_predicate(d,"d_" + str(d_index),d_delta,g)
            d_index += 1
        d_label = d_delta[str(d)]
   
        # include predicate for o  
        o = edo_py[2]    
        if str(o) not in d_omega:
            includes_predicate(o,"o_" + str(o_index),d_omega,g)
            o_index += 1
        o_label = d_omega[str(o)]
        
        # 3.2.2 emc as a subject
        edo_s_ttl = URIRef(PREFIX+"emc_" + "id" + "_" + e_label + "_" + d_label + "_" + o_label)
        edo_p_ttl = RDF.type
        #edo_o_ttl= URIRef(PREFIX+"EntityMatchingContext")
        edo_o_ttl= URIRef(PREFIX+"EMC")
        
        # add rdf type predicate
        g.add((edo_s_ttl,edo_p_ttl,edo_o_ttl)) 

        
        # 3.2.3 add epsilon, delta, omega predicate
        e_s_ttl = URIRef(PREFIX+e_label)
        g.add((edo_s_ttl,URIRef(PREFIX+"epsilon"),e_s_ttl))
        
        d_s_ttl = URIRef(PREFIX+d_label)
        g.add((edo_s_ttl,URIRef(PREFIX+"delta"),d_s_ttl))
   
        o_s_ttl = URIRef(PREFIX+o_label)
        g.add((edo_s_ttl,URIRef(PREFIX+"omega"),o_s_ttl))
        # 3.2.4 emc as predicate singleton property pattern
        s1 = URIRef(quote(VEC1_URI,safe=":/")) 
        s2 = URIRef(quote(edo[-1],safe=":/"))
        pair_p_ttl = edo_s_ttl
        g.add((s1,pair_p_ttl,s2)) 
        #g.add((s2,pair_p_ttl,s1)) 
        
        # store emc
        emcs.append("emc_" + "id" + "_" + e_label + "_" + d_label + "_" + o_label)
        
    # .. emc subPropertyOf predicate
    emc_subPropertyOf_predicate(emcs,d_epsilon,d_delta,d_omega,g)


    # 4 hasCosine min max pedicate 
    cosine_interval = generate_cosine_interval(0.05)
    cosines_and_uris = load_cosines_and_uris()
    affect_cosine_to_interval(cosine_interval,cosines_and_uris)
    index_named_graph = index_named_graphs_and_hasCosine_min_max_predicate(cosine_interval,g)
    # 5 neighborRedf2vec predicate
    neighborRdf2Vec_predicates(index_named_graph,cosine_interval,VEC1_URI,g) 
    # 6 add cosine to named graph
    for t in cosines_and_uris:
        s = URIRef(quote(t[0],safe=":/"))
        p = URIRef(PREFIX + "hasCosine")
        o = Literal(t[1])
        # choose the graph
        for key in index_named_graph:
            key_split = key.split("-")
            binf = float(key_split[0])
            bsup = float(key_split[1])
            if binf <= t[1] <= bsup:
                ng = URIRef(quote(NAMED_GAPH_PREFIX+index_named_graph[key],safe=":/"))
        g.add((s,p,o,ng))
    out = g.serialize(format="nquads")
    print(out)    
