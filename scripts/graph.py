import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Загрузить граф из GraphML файла
G = nx.read_graphml("kb/graph_chunk_entity_relation.graphml")

print(f"📊 Загружено узлов: {G.number_of_nodes()}")
print(f"📊 Загружено рёбер: {G.number_of_edges()}")

# Извлечь информацию о узлах
node_info = {}
entity_types = set()

for node_id in G.nodes():
    # node_id - это название узла (обычно в кавычках)
    entity_type = G.nodes[node_id].get('entity_type', 'UNKNOWN')
    description = G.nodes[node_id].get('description', 'No description')

    # Очистить кавычки из типа
    entity_type = entity_type.strip('"')

    # Сократить описание для отображения (первые 100 символов)
    short_desc = description[:100] + "..." if len(description) > 100 else description

    node_info[node_id] = {
        'name': node_id.strip('"'),  # Убрать кавычки из названия
        'type': entity_type,
        'description': description,
        'short_description': short_desc
    }

    entity_types.add(entity_type)

print(f"\n📋 Найдено типов сущностей: {len(entity_types)}")
for et in sorted(entity_types):
    count = sum(1 for n in node_info.values() if n['type'] == et)
    print(f"  - {et}: {count} узлов")

# Цветовая схема для типов сущностей
type_colors = {
    'EVENT': '#FF6B6B',
    'ORGANIZATION': '#4ECDC4',
    'CONCEPT': '#95E1D3',
    'PERSON': '#FFD93D',
    'LOCATION': '#A8E6CF',
    'UNKNOWN': '#CCCCCC'
}

# Если граф большой, взять подграф
if G.number_of_nodes() > 100:
    # Берём первые 50 узлов
    nodes = list(G.nodes())[:50]
    G_sub = G.subgraph(nodes)
    print(f"\n⚠️  Граф большой, отображаем только {len(nodes)} узлов")
else:
    G_sub = G
    nodes = list(G.nodes())

# Создать визуализацию
plt.figure(figsize=(20, 20))

# Настроить цвета узлов по типам
node_colors = [type_colors.get(node_info[node]['type'], '#CCCCCC') for node in G_sub.nodes()]

# Рисуем
pos = nx.spring_layout(G_sub, k=0.5, iterations=50)

# Рисуем рёбра
nx.draw_networkx_edges(
    G_sub,
    pos,
    edge_color='#DDDDDD',
    arrows=True,
    arrowsize=10,
    width=0.5,
    alpha=0.5
)

# Рисуем узлы
nx.draw_networkx_nodes(
    G_sub,
    pos,
    node_color=node_colors,
    node_size=800,
    alpha=0.9,
    edgecolors='black',
    linewidths=1.5
)

# Рисуем метки (только названия без кавычек)
labels = {node: node_info[node]['name'][:30] for node in G_sub.nodes()}  # Ограничиваем длину
nx.draw_networkx_labels(
    G_sub,
    pos,
    labels,
    font_size=7,
    font_weight='bold'
)

# Добавить легенду
legend_elements = [mpatches.Patch(facecolor=color, edgecolor='black', label=entity_type)
                   for entity_type, color in type_colors.items()
                   if entity_type in entity_types]
plt.legend(handles=legend_elements, loc='upper left', fontsize=10, title='Типы сущностей')

plt.title("MiniRAG Knowledge Graph - Граф знаний", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig("graph_visualization.png", dpi=300, bbox_inches='tight', facecolor='white')
print("\n✅ Граф сохранён в graph_visualization.png")

# Сохранить детальную информацию о узлах в текстовый файл
with open("graph_nodes_info.txt", "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("ИНФОРМАЦИЯ О УЗЛАХ ГРАФА ЗНАНИЙ\n")
    f.write("=" * 80 + "\n\n")

    for node_id in sorted(nodes, key=lambda x: node_info[x]['type']):
        info = node_info[node_id]
        f.write(f"Название: {info['name']}\n")
        f.write(f"Тип: {info['type']}\n")
        f.write(f"Описание: {info['description']}\n")
        f.write("-" * 80 + "\n\n")

print("✅ Информация о узлах сохранена в graph_nodes_info.txt")

plt.show()