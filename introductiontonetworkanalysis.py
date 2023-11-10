#importing the libraries
import networkx as nx
import numpy as np
import itertools
import matplotlib.pyplot as plt

#initializing an empty (here undirected) graph
G = nx.Graph()
#adding nodes
G.add_node("Rome")
G.add_node("Bern")
G.add_node("Zurich")
G.add_node("Vienna")
G.add_node("Berlin")
G.add_node("Paris")

#adding edges between the nodes (undirected)
G.add_edge("Bern","Zurich", weight=120)
G.add_edge("Rome","Zurich", weight=946)
G.add_edge("Rome","Vienna", weight=1033)
G.add_edge("Rome","Paris", weight=1351)
G.add_edge("Rome","Berlin", weight=1469)
G.add_edge("Paris","Berlin", weight=991)
G.add_edge("Paris","Bern", weight=509)
G.add_edge("Vienna","Zurich", weight=672)
#show the graph
nx.draw(G, with_labels=True)
nx.draw_circular(G, with_labels=True)

#or plot the graph with matplotlib
plt.figure(figsize=(10,7))
pos=nx.random_layout(G)
nx.draw(G, node_size=90, node_color="cyan", with_labels=True)
plt.show()

#show graph information
print(nx.info(G))

#create an adjacency matrix
adjmatrix=nx.adj_matrix(G)
print(adjmatrix.todense())

#create a numpy array
G_array=nx.to_numpy_array(G)
#save the matrix to a file
np.savetxt( "C:/DATA/G_array.txt", G_array, fmt="%d",delimiter=";")

#create an edges list from the graph
edge_list= nx.to_edgelist(G)
print(edge_list)

#create a node list from the graph
node_list=G.nodes()
print(node_list)


#calculate shortest path with Dijkstra algorithm
print("path length from Bern to Rome is "+str(nx.dijkstra_path_length(G,"Bern","Rome"))+" km")
print("when travelling from Bern to Rome we travel along: "+str(nx.dijkstra_path(G,"Bern","Rome")))

#iterate trhough all paths in the graph G (limit the path length to 3)
print(list(itertools.combinations(G.nodes(),3)))

#get the node degrees
print(G.degree())

#calculate betweenness centrality
print(nx.betweenness_centrality(G))

#graph density
print("graph density: ", nx.density(G))




