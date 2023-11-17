#script for showing how all components needed for code development are related to each other
import networkx as nx
import matplotlib.pyplot as plt

#create directed graph
G=nx.DiGraph()

#add components
G.add_node("Python interpreter") #the software that executes Python commands and scripts
G.add_node("Python script") #a file containing Python commands
G.add_node("PyCharm") #IDE integrated development environment software
G.add_node("PyCharm console") #interface to Python interpreter within IDE
G.add_node("Github repository") #one specific code repository at Github online
G.add_node("Github") #cloud for code versioning and code sharing
G.add_node("Github account") #account for Github
G.add_node("Github Desktop") #software for synchronizing offline and online repositories and code versioning
G.add_node("input data") #data stored on local disc that a code can read
G.add_node("output data") #data (files) created by the execution of a code
G.add_node("directory") #storage
G.add_node("local repository") #a code repository stored at local harddisc, available offline
G.add_node("Python library") #example is networkx

#add edges
G.add_edge("Python script","Python interpreter") #Python script is executed by interpreter
G.add_edge("Python library", "Python interpreter") #a Python library is added to the Python interpreter (e.g., import networkx)
G.add_edge("directory", "Python script") #Python script is a file stored in directory
G.add_edge("Python script","directory")  #if Python script is edited, directory is modified
G.add_edge("Python script","local repository")  #if Python script is edited, local repository is modified
G.add_edge("local repository","Python script")  #if local repository is synchronized, Python script is changed
G.add_edge("Python script", "PyCharm") #Python script can be accessed and read by PyCharm
G.add_edge("PyCharm", "Python script") #PyCharm can edit the Python script
G.add_edge("PyCharm", "PyCharm console") #PyCharm can send a script to be executed in console (=Python interpreter)
G.add_edge("PyCharm console", "Python interpreter") #PyCharm console executes a script and uses Python interpreter
G.add_edge("Python interpreter", "PyCharm console") #Python interpreter sends output to PyCharm console
G.add_edge("directory", "local repository")
G.add_edge("local repository","directory")
G.add_edge("directory", "input data") #a directory on local hard disc stores data (files)
G.add_edge("input data", "directory") #data can be manipulated and modified - this changes the directory
G.add_edge("Python interpreter", "directory") #with the execution of a Python script in the interpreter, the directory can be modfied
G.add_edge("Python interpreter", "input data") #with the execution of a Python script in the interpreter, the input data can be modfied-->attention!
G.add_edge("Github repository", "Github Desktop") #Github Desktop is the link between offline and online files and the code versioning system
G.add_edge("Python script", "local repository") #Github Desktop monitors changes in Python script
G.add_edge("Github Desktop", "local repository") #Github Desktop updates a local script if online version is updated
G.add_edge("local repository","Github Desktop") #Github Desktop synchronizes updates of local scripts with repository
G.add_edge("Github Desktop", "Github repository") #Github Desktop synchronizes offline and online versions of repository
G.add_edge("Github", "Github repository") #Github provides space for repository
G.add_edge("Github", "Github account") #Github account
G.add_edge("Python interpreter", "output data") #Python can write output data to local disc
G.add_edge("output data", "directory")
G.add_edge("Github account", "Github repository")

#draw the graph
nx.draw_kamada_kawai(G, with_labels=True)
#nx.draw(G, with_labels=True)
#nx.draw_shell(G, with_labels=True)
#nx.draw_spectral(G, with_labels=True)
#nx.draw_spring(G, with_labels=True)

#write the output for Gephi
nx.write_graphml(G,"C:/DATA/ide.graphml")

#draw the graph with matplotlib
plt.figure(figsize=(10,7))
pos=nx.kamada_kawai_layout(G)
nx.draw(G, pos, with_labels=True)
plt.show()
print("Hallo Zäme")