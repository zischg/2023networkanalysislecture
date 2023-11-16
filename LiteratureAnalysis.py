#script for showing exemplarily the use of networkx for the analysis of co-authors networks

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cm


#general workspace settings
myworkspace="C:/DATA/develops/LiteratureAnalysis"

#input data: the txt file with all the papers of the GIUB with GIUB-professors as co-authors. Exported from BORIS.unibe.ch
papersfile=open(myworkspace+"/papersGIUB.txt", "r", encoding='iso-8859-1')

#list of GIUB professors, surnames used only --> further improvement needed if used for in-depth analysis.
proflist=["Bottazzi", "Broennimann", "Gerber", "Grosjean", "Ruiz-Villanueva", "Martius", "Mayer", "Messerli", "Schaefli", "Schurr", "Speranza", "Thieme", "Wunderle", "Zischg", "Stocker"]

#create a list of unique papers
paperslist=[]
for line in papersfile:
    if line not in paperslist:
        paperslist.append(line)
papersfile.close()
print(str(len(paperslist))+" papers found")

#create graph
G = nx.Graph()
G.add_nodes_from(proflist)
G.nodes
for paper in paperslist:
    for prof in proflist:
        coauthorslist=proflist.copy()
        coauthorslist.remove(prof)
        if prof in paper:
            for coauthor in coauthorslist:
                if coauthor in paper:
                    G.add_edge(prof,coauthor)

#analysis of the number of connections
coauthorships = {}
for x in G.nodes:
    coauthorships[x] = len(G[x])
#print the number of coauthorships
print(coauthorships)

#create a graph
plt.figure(figsize=(15, 15))
nx.draw_shell(G, with_labels=True,)


#calculate centrality
print(nx.degree_centrality(G))
#Compute the degree centrality for nodes
#The degree centrality for a node v is the fraction of nodes it is connected to.
nx.subgraph_centrality(G)
nx.degree_centrality(G)

#voterank Select a list of influential nodes in a graph using VoteRank algorithm
nx.voterank(G,15)

#closeness centrality
#Closeness centrality [1] of a node u is the reciprocal of the average shortest path distance to u over all n-1 reachable nodes.
print(nx.closeness_centrality(G, u=None, distance=None, wf_improved=True))



#write the Graphml for Gephi
nx.write_graphml(G, myworkspace+"/papersGIUB_graphml.graphml")

#graph with degree centrality
cent = np.fromiter(nx.degree_centrality(G).values(), float)
sizes = cent / np.max(cent) * 200
normalize = mcolors.Normalize(vmin=cent.min(), vmax=cent.max())
colormap = cm.viridis
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(cent)
plt.colorbar(scalarmappaple)
pos = nx.spring_layout(G)#pos = nx.draw_circular(G)
nx.draw(G, pos, node_size=sizes, node_color=sizes, cmap=colormap,with_labels=True,)
plt.show()

nx.draw(G, pos, with_labels=True,)
plt.show()


nx.draw(G, with_labels=True,)
nx.draw_circular(G, with_labels=True,)
nx.draw_spectral(G, with_labels=True,)
nx.draw_spring(G, with_labels=True,)
nx.draw(nx.degree_centrality(G), with_labels=True,)
