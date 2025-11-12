import networkx as nx
import matplotlib.pyplot as plt

# Загрузить граф
G = nx.read_graphml("kb/graph_chunk_entity_relation.graphml")

# Создать визуализацию
plt.figure(figsize=(15, 15))

# Если граф большой, возьмите подграф
if G.number_of_nodes() > 100:
    # Берём первые 50 узлов
    nodes = list(G.nodes())[:50]
    G_sub = G.subgraph(nodes)
else:
    G_sub = G

# Рисуем
pos = nx.spring_layout(G_sub, k=0.5, iterations=50)
nx.draw(
    G_sub, 
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=500,
    font_size=8,
    font_weight='bold',
    edge_color='gray',
    arrows=True
)

plt.title("MiniRAG Knowledge Graph")
plt.tight_layout()
plt.savefig("graph_visualization.png", dpi=300, bbox_inches='tight')
plt.show()

print("✅ Граф сохранён в graph_visualization.png")