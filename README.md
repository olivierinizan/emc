This is the code for Entity Matching Contexts
 
# EMCs 
- EMCs have been detected on the VICKEY dataset
- Classes studied are: Album, Actor, University, Book, Film and Mountain

# EMCs detection: 
- EMCs detection for cartesian product of pairs DBpedia YAGO
- Scripts experiment/CLASSNAME\_edo\_index2r.py compute this detection
- Results are in files experiment/CLASSNAME/edo\_CLASSNAME\_index2.r.m
- Results are indexed with ids, mapping ids-individuals are in DBorYAGO\_CLASSNAME\_ids

# Experiments (table 1, table 2, figure 3, figure 4)
- raw data for the left side of table 1 are generated by the script: experiment/table1\_left.py
- raw data for the right side of table 1 (RIC,WIC,NIC contexts) are in files: experiment/CLASSNAME\_ratio\_table.csv
- raw data for figure 3 are in: experiment/album\_ratio\_table.csv  
- raw data for table 2 are in: experiment/album\_ratio\_barchart\_detail.csv
- raw data for figure 4 are in: experiment/CLASSNAME\_ratio\_barchart.csv
- details on raw data generation are in experiment/README

# Use case (table 3)
- nquad graph for Adam May: use\_case/out.nq
- sparql query result (table 3): use\_case/adam\_query.res
- queries example: use\_case/queries.py
