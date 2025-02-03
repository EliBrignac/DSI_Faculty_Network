import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from itertools import combinations
import time


import openai
api_key = "APIKey"  # Set your OpenAI API key

openai_client = openai.OpenAI(api_key=api_key)  # Ensure you replace this with your actual API key
def check_similarity(interest1, interest2):
    """Use an LLM to determine if two research topics are similar."""
    prompt = f"Are the following research topics conceptually similar? Respond with 'Yes' or 'No' only.\n\n1. {interest1}\n2. {interest2}\n\nAnswer:"

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that determines research field similarity."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content.strip().lower()
    return answer == "yes"

df = pd.read_csv('ud_faculty_joined.csv')
print(df.columns)
df = df[['Author Name', 'Title', 'Research Interests']]
#print(df['Research Interests'])

#print(df['Research Interests'].unique())
df = df.drop_duplicates()
df = df.dropna(subset=['Research Interests'])

# Group by 'Title' and get the authors for each paper
grouped = df.groupby('Title')['Author Name'].apply(list)

# Initialize an empty graph
G = nx.Graph()

# add "publication count" to the graph
node_amounts = df.groupby('Author Name').size().to_dict()
for author, amount in node_amounts.items():
    G.add_node(author, amount=amount, interests=df[df['Author Name'] == author]['Research Interests'].values[0])


edge_count = 0
for authors in grouped:
    for author1, author2 in combinations(set(authors), 2):
        #print(research_similarity)
        if G.has_edge(author1, author2):
            continue
        else:
            #print(G.nodes[author1]['interests'], G.nodes[author2]['interests'])

            a1_interests = G.nodes[author1]['interests'].split(',')
            a2_interests = G.nodes[author2]['interests'].split(',')

            # get similarity of research interests
            w = 0
            for interest1 in a1_interests:
                for interest2 in a2_interests:
                    interest1 = interest1.strip()
                    interest2 = interest2.strip()
                    interest1 = interest1.lower()
                    interest2 = interest2.lower()
                    interest1 = interest1.replace('.', '')  
                    interest2 = interest2.replace('.', '')
                    research_similarity = check_similarity(interest1, interest2)
                    if research_similarity == True:
                        w += 1
                        print(interest1, interest2)
            if w > 0:
                edge_count += 1
                G.add_edge(author1, author2, weight=w)

print(edge_count)

# # Iterate through papers with multiple authors
# for authors in grouped:
#     # Create all pairs of authors that collaborated on this paper
#     for author1, author2 in combinations(set(authors), 2):
#         if G.has_edge(author1, author2):
#             # If the edge already exists, increment the weight (collaboration count)
#             G[author1][author2]['weight'] += 1
#         else:
#             # Otherwise, create a new edge with weight 1
#             G.add_edge(author1, author2, weight=1)

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

#     # 1. Save as GraphML (preserves all graph structure and attributes)
# nx.write_graphml(G, "collaboration_network_with_interests.graphml")

nx.write_gml(G, "collaboration_network_with_interests.gml")
