import networkx as nx
import matplotlib.pyplot as plt

G=nx.read_shp('C:/DATA/zh_roadsLV95.shp') #Read shapefile as graph
pos = {xy: xy for xy in G.nodes()}
nx.draw_networkx_nodes(G,pos,node_size=100,node_color='r')
nx.draw_networkx_edges(G,pos,edge_color='k')
plt.xlim(450000, 470000)
plt.ylim(430000, 450000)