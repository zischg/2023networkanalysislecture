#script for analysing betweenness centrality in the road network of the Canton of ZH
import numpy as np
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt


#general workspace settings
myworkspace="C:/DATA/develops/zh"

#input data: the csv file for nodes and edges
nodesfile=myworkspace+"/zh_nodes.shp"
edgesfile=myworkspace+"/zh_roads.shp"
#input data: the roads file
nodesgdf = gpd.read_file(nodesfile)
edgesgdf = gpd.read_file(edgesfile)

#output data: the nodes distances file
nodesbetweennesscentralityfile=open(myworkspace+"/betweennesscentrality_normalsituation.csv","w")
nodesbetweennesscentralityfile.write("nodeid"+";"+"betweennesscentrality"+"\n")

#create graph
G = nx.Graph()
#loop through the road shapefile
for index, row in edgesgdf.iterrows():
    length = row.SHAPE_Leng
    nodeid1=row.nodeid1
    nodeid2 = row.nodeid2
    xcoord1=nodesgdf[nodesgdf["nodeid"]==row.nodeid1].x
    ycoord1 = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].y
    G.add_node(row.nodeid1, pos=(xcoord1, ycoord1))
    xcoord2=nodesgdf[nodesgdf["nodeid"]==row.nodeid2].x
    ycoord2 = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].y
    G.add_node(row.nodeid2, pos=(xcoord2, ycoord2))
    G.add_edge(row.nodeid1, row.nodeid2, weight=length)
print("network graph created ...")

#calculate betweenness centrality for all nodes and write it to the output file
#Betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v.
#parameter k is the number of the sample to safe time, k=1000 --> ca. 1% of the total network is taken as a sample
#if k=None, the full network will be considered. This needs some hours of computation
betweennesscentrality=nx.betweenness_centrality(G, k=1000, normalized=True, endpoints=True)
#betweennesscentrality=nx.betweenness_centrality(G, k=None, normalized=True, endpoints=True)
for n in betweennesscentrality:
    nodesbetweennesscentralityfile.write(str(n)+";"+str(betweennesscentrality[n])+"\n")
nodesbetweennesscentralityfile.close()
print("betweenness centrality for nodes in ZH traffic network computed and exported to file ...")




