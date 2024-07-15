from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, XSD, ConjunctiveGraph
from urllib.parse import unquote

g = ConjunctiveGraph()
g.parse("out.nq",format='nquads')

# EMC by epsilon specificity
query9="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT  ?emc ?size ?sized ?sizeo ?player2 ?cosine
WHERE{
    ?emc a emc:EMC ;
         emc:epsilon ?e ;
         emc:delta ?d ;
         emc:omega ?o .
    ?player1 ?emc ?player2 .
    ?player2 emc:hasCosine ?cosine .
    ?e emc:size ?size .
    ?d emc:size ?sized .
    ?o emc:size ?sizeo .
}
ORDER BY DESC (?size)
"""
results = g.query(query9)
print()
for row in results:
    print(str(row.emc) + " " + str(row.size) + " " + str(row.sized) + " " + str(row.sizeo) +" " + str(unquote(row.player2)) + " " +str(row.cosine))

# e_15
query10="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?p
WHERE {
    emc:e_15 emc:includes ?p .
}
"""
results = g.query(query10)
print()
print("e_15")
e_15 = set()
for row in results:
    e_15.add(row.p)
    print(row.p)

# d_0
query10="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?p
WHERE {
    emc:d_0 emc:includes ?p .
}
"""
results = g.query(query10)
print()
print("d_0")
d_0 = set()
for row in results:
    d_0.add(row.p)
    print(row.p)


# e_4
query11="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?p
WHERE {
    emc:e_4 emc:includes ?p .
}
"""
results = g.query(query11)
print()
print("e_4")
e_4 = set()
for row in results:
    e_4.add(row.p)
    print(row.p)

print()
print("e_15 - e_4 and e_4 - e_15")
print(e_15 - e_4)
print(e_4 - e_15)


# d_4
query11="""
PREFIX emc: <https://lisn.upsaclay.fr/vocabulary/emc/>
SELECT ?p
WHERE {
    emc:d_4 emc:includes ?p .
}
"""
results = g.query(query11)
print()
print("d_4")
d_4 = set()
for row in results:
    d_4.add(row.p)
    print(row.p)

print()
print("d_0 - d_4 and d_4 - d_0")
print(d_0 - d_4)
print(d_4 - d_0)



