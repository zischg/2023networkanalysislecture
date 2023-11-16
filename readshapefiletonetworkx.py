import momepy
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import pandas as pd
from shapely.geometry import LineString

#function to test
def convert_shp2graph(p, make_G_bidi=True, name='unamed'):
    """
    Converts shapefile to routable networkx graph.

    Parameters
    ----------
    p : str, File path - allowed formats geojson and ESRI Shapefile and other formats Fiona can read and write
    make_G_bidi : bool, if True, assumes linestrings are bidirectional
    name : str, Optional name of graph

    Returns
    -------
    G : graph
    """

    # Load shapefile into GeoDataFrame
    gdf = gpd.read_file(p)

    # shapefile needs to include minimal: geometry linestring and the length computed (e.g. in QGIS)
    if 'length' not in gdf.columns:
        raise Exception('Shapefile is invalid: length not in attributes:\n{}'.format(gdf.columns))

    if not gdf.geometry.map(lambda x: type(x) == LineString).all():
        s_invalid_geo = gdf.geometry[gdf.geometry.map(lambda x: type(x) == LineString)]
        raise Exception('Shapefile is invalid: geometry not all linestring \n{}'.format(s_invalid_geo))

    # Compute the start- and end-position based on linestring
    gdf['Start_pos'] = gdf.geometry.apply(lambda x: x.coords[0])
    gdf['End_pos'] = gdf.geometry.apply(lambda x: x.coords[-1])

    # Create Series of unique nodes and their associated position
    s_points = gdf.Start_pos.append(gdf.End_pos).reset_index(drop=True)
    s_points = s_points.drop_duplicates()
    #     log('GeoDataFrame has {} elements (linestrings) and {} unique nodes'.format(len(gdf),len(s_points)))

    # Add index of start and end node of linestring to geopandas DataFrame
    df_points = pd.DataFrame(s_points, columns=['Start_pos'])
    df_points['FNODE_'] = df_points.index
    gdf = pd.merge(gdf, df_points, on='Start_pos', how='inner')

    df_points = pd.DataFrame(s_points, columns=['End_pos'])
    df_points['TNODE_'] = df_points.index
    gdf = pd.merge(gdf, df_points, on='End_pos', how='inner')

    # Bring nodes and their position in form needed for osmnx (give arbitrary osmid (index) despite not osm file)
    df_points.columns = ['pos', 'osmid']
    df_points[['x', 'y']] = df_points['pos'].apply(pd.Series)
    df_node_xy = df_points.drop('pos', 1)

    # Create Graph Object
    G = nx.MultiDiGraph(name=name, crs=gdf.crs)

    # Add nodes to graph
    for node, data in df_node_xy.T.to_dict().items():
        G.add_node(node, **data)

    # Add edges to graph
    for i, row in gdf.iterrows():
        dict_row = row.to_dict()
        if 'geometry' in dict_row: del dict_row['geometry']
        G.add_edge(u=dict_row['FNODE_'], v=dict_row['TNODE_'], **dict_row)

    if make_G_bidi:
        gdf.rename(columns={'Start_pos': 'End_pos',
                            'End_pos': 'Start_pos',
                            'FNODE_': 'TNODE_',
                            'TNODE_': 'FNODE_', }, inplace=True)

        # Add edges to graph
        for i, row in gdf.iterrows():
            dict_row = row.to_dict()
            if 'geometry' in dict_row: del dict_row['geometry']
            G.add_edge(u=dict_row['FNODE_'], v=dict_row['TNODE_'], **dict_row)

    #         G = G.to_undirected() # Some function in osmnx do not work anymore

    # Log information
    #     log('Graph has been successfully generated /n {}'.format(nx.info(G)))
    #     log('Show graph data structure EDGE'.format(G.get_edge_data(*list(G.edges())[0])))
    #     log('Show graph data structure NODE'.format(list(G.nodes())[0]))
    return G

graph= convert_shp2graph("C:/DATA/BEroads2021sp_extract.shp", make_G_bidi=True, name ="graphname")


#import the street dataset
#streets = gpd.read_file("C:/DATA/BEroads1940sp.shp", layer='BEroads1940sp')
#streets = gpd.read_file("C:/DATA/BEroads2021sp_extract.shp", layer='BEroads2021sp_extract')
streets = gpd.read_file("C:/DATA/BEroads2021sp.shp", layer='BEroads2021sp')
len(streets)

#plot
f, ax = plt.subplots(figsize=(10, 10))
#streets2021.plot(ax=ax)
streets.plot(ax=ax)
ax.set_axis_off()
plt.show()

#convert line data to networkx graph
graph = momepy.gdf_to_nx(streets, approach='primal',length='mm_len')
f, ax = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
streets.plot(color='#e32e00', ax=ax[0])
for i, facet in enumerate(ax):
    facet.set_title(("Streets", "Primal graph", "Overlay")[i])
    facet.axis("off")
nx.draw(graph, {n:[n[0], n[1]] for n in list(graph.nodes)}, ax=ax[1], node_size=15)
streets.plot(color='#e32e00', ax=ax[2], zorder=-1)
nx.draw(graph, {n:[n[0], n[1]] for n in list(graph.nodes)}, ax=ax[2], node_size=15)

#compare
dual = momepy.gdf_to_nx(streets, approach='dual', length='mm_len')
f, ax = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
streets.plot(color='#e32e00', ax=ax[0])
for i, facet in enumerate(ax):
    facet.set_title(("Streets", "Dual graph", "Overlay")[i])
    facet.axis("off")
nx.draw(dual, {n:[n[0], n[1]] for n in list(dual.nodes)}, ax=ax[1], node_size=15)
streets.plot(color='#e32e00', ax=ax[2], zorder=-1)
nx.draw(dual, {n:[n[0], n[1]] for n in list(dual.nodes)}, ax=ax[2], node_size=15)

#calculate degree
degree = dict(nx.degree(graph))
nx.set_node_attributes(graph, degree, 'degree')
#or directly
graph = momepy.node_degree(graph, name='degree')
#graph = momepy.clustering(graph, name='clustering')

#plot node degrees
nodes, edges, sw = momepy.nx_to_gdf(graph, points=True, lines=True,spatial_weights=True)
f, ax = plt.subplots(figsize=(10, 10))
nodes.plot(ax=ax, column='degree', cmap='tab20b', markersize=(nodes['degree'] * 100), zorder=2)
edges.plot(ax=ax, color='lightgrey', zorder=1)
ax.set_axis_off()
plt.show()

#edge based analysis - edge betweenness
f, ax = plt.subplots(figsize=(10, 10))
edges.plot(ax=ax, linewidth=0.2)
ax.set_axis_off()
plt.show()
primal = momepy.gdf_to_nx(edges, approach='primal') #primal = edges are streets and nodes are intersections

#closeness centrality (average distance to every other node from each node)
primal = momepy.closeness_centrality(primal, radius=400, name='closeness400', distance='mm_len', weight='mm_len')
nodes = momepy.nx_to_gdf(primal, lines=False)
f, ax = plt.subplots(figsize=(15, 15))
nodes.plot(ax=ax, column='closeness400', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('closeness400')
plt.show()

#global closeness
primal = momepy.closeness_centrality(primal, name='closeness_global', weight='mm_len')
nodes = momepy.nx_to_gdf(primal, lines=False)
f, ax = plt.subplots(figsize=(15, 15))
nodes.plot(ax=ax, column='closeness_global', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('closeness_global')
plt.show()

#betweenness
primal = momepy.betweenness_centrality(primal, name='betweenness_metric_n', mode='nodes', weight='mm_len')
#node-based betweenness
nodes = momepy.nx_to_gdf(primal, lines=False)
f, ax = plt.subplots(figsize=(15, 15))
nodes.plot(ax=ax, column='betweenness_metric_n', cmap='Spectral_r', scheme='quantiles', k=7, alpha=0.6)
ax.set_axis_off()
ax.set_title('betweenness_metric_n')
plt.show()
#edge-based betweenness
primal = momepy.betweenness_centrality(primal, name='betweenness_metric_e', mode='edges', weight='mm_len')
primal_gdf = momepy.nx_to_gdf(primal, points=False)
f, ax = plt.subplots(figsize=(15, 15))
primal_gdf.plot(ax=ax, column='betweenness_metric_e', cmap='Spectral_r', scheme='quantiles', alpha=0.6)
ax.set_axis_off()
ax.set_title('betweennes edge based')
plt.show()

#straightness (atio between real and Euclidean distance while waking from each node to every other)
primal = momepy.straightness_centrality(primal)

nodes = momepy.nx_to_gdf(primal, lines=False)
f, ax = plt.subplots(figsize=(15, 15))
nodes.plot(ax=ax, column='straightness', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('straightness')
plt.show()
#Node values averaged onto edges
momepy.mean_nodes(primal, 'straightness')
momepy.mean_nodes(primal, 'closeness400')
momepy.mean_nodes(primal, 'closeness_global')
momepy.mean_nodes(primal, 'betweenness_metric_n')

primal_gdf = momepy.nx_to_gdf(primal, points=False)

f, ax = plt.subplots(figsize=(15, 15))
primal_gdf.plot(ax=ax, column='straightness', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('straightness')
plt.show()

#closeness node based mean
f, ax = plt.subplots(figsize=(15, 15))
primal_gdf.plot(ax=ax, column='closeness400', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('closeness400 node based mean')
plt.show()

#closeness global node based mean
f, ax = plt.subplots(figsize=(15, 15))
primal_gdf.plot(ax=ax, column='closeness_global', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('closeness global node based mean')
plt.show()

#betweenness node based mean
f, ax = plt.subplots(figsize=(15, 15))
primal_gdf.plot(ax=ax, column='betweenness_metric_n', cmap='Spectral_r', scheme='quantiles', k=15, alpha=0.6)
ax.set_axis_off()
ax.set_title('betweennes node based mean')
plt.show()

#save back to geopandas
nodes, edges_p = momepy.nx_to_gdf(primal)


#use open street map
#import osmnx as ox
#streets_graph = ox.graph_from_place('Vicenza, Vicenza, Italy', network_type='drive')
#streets_graph = ox.projection.project_graph(streets_graph)
#streets = ox.graph_to_gdfs(ox.get_undirected(streets_graph), nodes=False, edges=True,node_geometry=False, fill_edge_geometry=True)
#streets.plot(figsize=(10, 10), linewidth=0.2).set_axis_off()
#continuity = momepy.COINS(streets)
#stroke_gdf = continuity.stroke_gdf()
#stroke_gdf.plot(stroke_gdf.length,figsize=(15, 15),cmap="viridis_r",linewidth=.5,scheme="headtailbreaks").set_axis_off()