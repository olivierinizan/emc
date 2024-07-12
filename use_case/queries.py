from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, XSD, ConjunctiveGraph
from urllib.parse import unquote

g = ConjunctiveGraph()
g.parse("out.nq",format='nquads')

# How many context ?
query1= """
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT (COUNT(?context) as ?TOTAL)
WHERE {
    ?context a emc:Context
}
"""

results = g.query(query1)
print()
print("Nb Contexts")
for row in results:
    print(row.TOTAL)

# How many EMC ?
query2="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT (COUNT(?emc) as ?TOTAL)
WHERE {
    ?emc a emc:EMC
}
"""
results = g.query(query2)
print()
print("Nb EMCs")
for row in results:
    print(row.TOTAL)

# named graph min/max cosine
query4="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?g 
WHERE {
    ?g emc:hasCosineMin "0.75"^^<http://www.w3.org/2001/XMLSchema#double> .
}
"""
print()
print("Cosine")
results = g.query(query4)
for row in results:
    print(row.g)

# emc with team, goals, years, caps, clubs and diff in position
query5="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?emc
WHERE {
    ?emc a emc:EMC ;
        emc:epsilon ?e ;
        emc:delta ?d .
    ?e emc:includes <http://dbpedia.org/property/goals> ;
        emc:includes <http://dbpedia.org/ontology/team> ;
        emc:includes <http://dbpedia.org/property/years> ;
        emc:includes <http://dbpedia.org/property/caps> ;
        emc:includes <http://dbpedia.org/property/clubs> .
    ?d emc:includes <http://dbpedia.org/property/position> .
}
"""
print()
print("Query EMC by properties")
print("Epsilon: team, goals, years, caps, clubs")
print("Delta: position")
results = g.query(query5)
for row in results:
    print(row.emc)

"""
emc:emc_23_e_18_d_14_o_22
emc:emc_14_e_10_d_4_o_14
emc:emc_12_e_10_d_4_o_12
emc:emc_48_e_15_d_0_o_33
emc:emc_46_e_15_d_0_o_31
emc:emc_18_e_15_d_0_o_17
emc:emc_49_e_15_d_0_o_4
emc:emc_21_e_17_d_4_o_20
emc:emc_33_e_22_d_16_o_26
"""

# emc with team, goals, years, caps, clubs and position
query7="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?emc
WHERE {
    ?emc a emc:EMC ;
        emc:epsilon ?e .
    ?e emc:includes <http://dbpedia.org/property/goals> ;
        emc:includes <http://dbpedia.org/ontology/team> ;
        emc:includes <http://dbpedia.org/property/years> ;
        emc:includes <http://dbpedia.org/property/caps> ;
        emc:includes <http://dbpedia.org/property/clubs> ;
        emc:includes <http://dbpedia.org/property/position> . 
}
"""
print()
print("Query EMC by properties")
print("Epsilon: team, goals, years, caps, clubs, position")
results = g.query(query7)
for row in results:
    print(row.emc)
"""
emc:emc_1_e_1_d_1_o_1
emc:emc_43_e_27_d_3_o_14
emc:emc_37_e_25_d_20_o_13
emc:emc_15_e_12_d_11_o_12
emc:emc_34_e_23_d_17_o_27
emc:emc_35_e_22_d_18_o_28
emc:emc_33_e_22_d_16_o_26
"""
