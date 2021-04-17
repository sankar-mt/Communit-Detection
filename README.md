# Community-Detection
Detecting communities from a given undirected graph and performing a detailed analysis on the 
communities.(Graph visualisation,Community size, Community description,Frequency plot)

# Dataset Description
• Nodes: 70
• Edges: 181
• Type: Undirected,unweighted

# Tools Used
Micro Web Framework
• Flask
Python packages
• Networkx
Graph manipulation and visualization
• Community
This python package was used to perform community detection using the girvan-newman
algorithm 
• Communities
This python package was used to perform community detection using the louvain-method 
algorithm 
• Matplotlib
Used for plotting the graphs

# Step wise procedure
• Input graph is chosen of the format txt with delimiter ',' 
• The graph is saved locally.
• The graph is built with the edgelist from the txt file using the networkx python package.
• Community detection algorithms are run on the graph and the graphs are coloured and saved as images in png format.
• Analysis is made and result is stored in local variables which are then passed to the html pages for display.
• Results are displayed.(Input grpah, girvan-newman coloured graph, louvain coloured graph,Community size, Community description,Frequency plot)

# Algorithms used for community detection
• Girvan - Newman
• Louvain
