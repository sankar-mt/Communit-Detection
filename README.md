# Community-Detection
Detecting communities from a given undirected graph and performing a detailed analysis on the 
communities.(Graph visualisation,Community size, Community description,Frequency plot)

# Dataset Description
• Nodes: 70<br/>
• Edges: 181<br/>
• Type: Undirected,unweighted<br/>

# Tools Used
Micro Web Framework<br/>
• Flask<br/>
Python packages
• Networkx<br/>
Graph manipulation and visualization
• Community<br/>
This python package was used to perform community detection using the girvan-newman
algorithm <br/>
• Communities<br/>
This python package was used to perform community detection using the louvain-method 
algorithm <br/>
• Matplotlib<br/>
Used for plotting the graphs<br/>

# Step wise procedure
• Input graph is chosen of the format txt with delimiter ',' <br/>
• The graph is saved locally.<br/>
• The graph is built with the edgelist from the txt file using the networkx python package.<br/>
• Community detection algorithms are run on the graph and the graphs are coloured and saved as images in png format.<br/>
• Analysis is made and result is stored in local variables which are then passed to the html pages for display.<br/>
• Results are displayed.(Input grpah, girvan-newman coloured graph, louvain coloured graph,Community size, Community description,Frequency plot)<br/>

# Algorithms used for community detection
• Girvan - Newman<br/>
• Louvain
