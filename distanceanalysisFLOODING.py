#script for analysing shortes paths from all nodes in road network of Canton Zurich to Zurich main central station
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes

#general workspace settings
myworkspace="C:/DATA/develops/zh"

#input data: the csv file for nodes and edges
nodesfile=myworkspace+"/zh_nodes.shp"
edgesfile=myworkspace+"/zh_roads.shp"
floodednodesfile=myworkspace+"/zh_nodes_flooded.shp"
floodededgesfile=myworkspace+"/zh_roads_flooded.shp"
floodmap=myworkspace+"/WB_HW_IK100_F_LV03dissolve.shp"
#input data: the roads file
nodesgdf = gpd.read_file(nodesfile)
nodesgdf.columns
edgesgdf = gpd.read_file(edgesfile)
edgesgdf.columns
floodmapgdf=gpd.read_file(floodmap)
floodmapgdf.columns
#input data: the flooded nodes and roads files
floodednodesgdf = gpd.read_file(floodednodesfile)
floodededgesgdf = gpd.read_file(floodededgesfile)

#output data: the nodes distances file
nodesdistancesfile=open(myworkspace+"/nodesdistancesflooding.csv","w")
nodesdistancesfile.write("nodeid"+";"+"distancetoZHsbbFLOOD"+"\n")

#plot the geodata
nodesgdf.plot()
edgesgdf.plot()
floodmapgdf.plot()

#create lists of flooded nodes and flooded edges (will not be part of the created graph
listoffloodednodes=floodednodesgdf["nodeid"].unique().tolist()
listoffloodededges=floodededgesgdf["ID_Road"].unique().tolist()
print(str(len(listoffloodednodes))+" nodes are flooded")
print(str(len(listoffloodededges))+" road segments are flooded")


#create graph
G = nx.Graph()
nodesidlist=[]
edgesidlist=[]
#loop through the road shapefile
counter=0
for index, row in edgesgdf.iterrows():
    if row.ID_Road not in listoffloodededges:
        #print(counter)
        length = row.SHAPE_Leng
        nodeid1=row.nodeid1
        nodeid2 = row.nodeid2
        if row.nodeid1 not in listoffloodednodes:
            xcoord=nodesgdf[nodesgdf["nodeid"]==row.nodeid1].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid1].y
            if row.nodeid1 not in G:
                G.add_node(row.nodeid1, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid1)
        if row.nodeid2 not in listoffloodednodes:
            xcoord=nodesgdf[nodesgdf["nodeid"]==row.nodeid2].x
            ycoord = nodesgdf[nodesgdf["nodeid"] == row.nodeid2].y
            if row.nodeid2 not in G:
                G.add_node(row.nodeid2, pos=(xcoord, ycoord))
                nodesidlist.append(row.nodeid2)
        edgesidlist.append(row.ID_Road)
        if row.nodeid1 not in listoffloodednodes and row.nodeid2 not in listoffloodednodes:
            G.add_edge(row.nodeid1, row.nodeid2, weight=length)
        counter+=1
print("network graph created ...")

#calculate shortest distance to Zurich main railway station during flooding
#target is main railway station in Zurich = node_id 72356
targetnode=72356
#calculate shortest path for each node
i=0
for n in list(G.nodes):
    print(i)
    sourcenode =n
    if nx.has_path(G,sourcenode,targetnode):
        distancetoZHsbbFLOOD=nx.shortest_path_length(G,source=sourcenode, target=targetnode, weight="weight")
        nodesdistancesfile.write(str(sourcenode)+";"+str(distancetoZHsbbFLOOD)+"\n")
    i+=1
nodesdistancesfile.close()
print("shortest paths to ZH main station during flooding computed ...")


