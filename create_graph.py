import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from itertools import combinations

df = pd.read_csv('ud_faculty_scholar_publications.csv')
print(df.columns)
df = df[['Author Name', 'Title']]
df = df.drop_duplicates()

# Group by 'Title' and get the authors for each paper
grouped = df.groupby('Title')['Author Name'].apply(list)

# Initialize an empty graph
G = nx.Graph()

# add "publication count" to the graph
node_amounts = df.groupby('Author Name').size().to_dict()
for author, amount in node_amounts.items():
    G.add_node(author, amount=amount)

# Iterate through papers with multiple authors
for authors in grouped:
    # Create all pairs of authors that collaborated on this paper
    for author1, author2 in combinations(set(authors), 2):
        if G.has_edge(author1, author2):
            # If the edge already exists, increment the weight (collaboration count)
            G[author1][author2]['weight'] += 1
        else:
            # Otherwise, create a new edge with weight 1
            G.add_edge(author1, author2, weight=1)

# Generate positions for nodes using spring layout
pos = nx.spring_layout(G, seed=42)

# Prepare the node positions and edge data for Plotly
edge_x = []
edge_y = []
edge_weights = []
for u, v, data in G.edges(data=True):
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_weights.append(data['weight'])

    # 1. Save as GraphML (preserves all graph structure and attributes)
nx.write_graphml(G, "collaboration_network_noduplicates_simple.graphml")

nx.write_gml(G, "collaboration_graph_noduplicates_simple.gml")
