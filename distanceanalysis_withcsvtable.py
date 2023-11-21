#script for analysing shortes paths from all nodes in road network of Canton Zurich to Zurich main central station
import pandas as pd
import networkx as nx

#general workspace settings
myworkspace="C:/DATA/develops/zh"
roadstable=myworkspace+"/zhroads.csv"

#create a csv file for nodes and edges
nodesfile=open(myworkspace+"/nodes.csv","w")
edgesfile=open(myworkspace+"/edges.csv","w")
nodesfile.write("nodeid"+";"+"x"+";"+"y"+"\n")
edgesfile.write("edgeid"+";"+"nodeid1"+";"+"nodeid2"+";"+"length"+"\n")
nodesdistancesfile=open(myworkspace+"/nodesdistances.csv","w")
nodesdistancesfile.write("nodeid"+";"+"x"+";"+"y"+";"+"distancetoZHsbb"+"\n")

#read the roads table
roadsdf=pd.read_csv(roadstable, delimiter=";")

#loop through roads dataframe and create a list of nodes and a list of edges
nodescoordinateslist=[]
nodesidlist=[]
edgeslist=[]
nodescounter=0

#create graph
G = nx.Graph()

for index, row in roadsdf.iterrows():
    if row.ID_Road not in edgeslist:
        edgeslist.append(row.ID_Road)
        xstart = row.BeginX
        ystart = row.BeginY
        xend = row.EndX
        yend = row.EndY
        length = row.SHAPE_Leng
        nodeidstart=0
        nodeidend=0
        #check if node coordinates are not counted twice
        if [xstart, ystart] not in nodescoordinateslist:
            nodescoordinateslist.append([xstart, ystart])
            nodescounter+=1
            nodesidlist.append(nodescounter)
            nodeidstart=nodescounter
            nodesfile.write(str(nodeidstart) + ";" + str(xstart) + ";" + str(ystart) + "\n")
            G.add_node(nodeidstart, pos=(xstart, ystart))
        else:
            nodeidstart=nodesidlist[nodescoordinateslist.index([xstart, ystart])]
            G.add_node(nodeidstart, pos=(xstart, ystart))
        if [xend, yend] not in nodescoordinateslist:
            nodescoordinateslist.append([xend, yend])
            nodescounter += 1
            nodesidlist.append(nodescounter)
            nodeidend = nodescounter
            nodesfile.write(str(nodeidend) + ";" + str(xend) + ";" + str(yend) + "\n")
            G.add_node(nodeidend, pos=(xend, yend))
        else:
            nodeidend=nodesidlist[nodescoordinateslist.index([xend, yend])]
            G.add_node(nodeidend, pos=(xend, yend))
        #add the road segment to the graph
        edgesfile.write(str(row.ID_Road)+";"+str(nodeidstart)+";"+str(nodeidend)+";"+str(length)+"\n")
        edgeslist.append([row.ID_Road,nodeidstart,nodeidend,length])
        G.add_edge(nodeidstart, nodeidend, weight=length)
nodesfile.close()
edgesfile.close()
print("network graph created ...")

#G.clear()

#target is main railway station in Zurich = node_id 76266
targetnode=72356

#calculate shortest path for each node
i=0
while i<len(nodesidlist):
    print(i)
    sourcenode =nodesidlist[i]
    x=nodescoordinateslist[i][0]
    y=nodescoordinateslist[i][1]
    if nx.has_path(G,sourcenode,targetnode):
        distancetoZHsbb=nx.shortest_path_length(G,source=sourcenode, target=targetnode, weight="weight")
        nodesdistancesfile.write(str(sourcenode)+";"+str(x)+";"+str(y)+";"+str(distancetoZHsbb)+"\n")
    i+=1
nodesdistancesfile.close()
print("shortest paths to ZH main station computed ...")
