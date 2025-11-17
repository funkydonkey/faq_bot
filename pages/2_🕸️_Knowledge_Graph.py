"""Knowledge Graph visualization page for FAQ Bot."""
import os
import sys
import streamlit as st
from pathlib import Path
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx

# Add current directory and parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Page configuration
st.set_page_config(
    page_title="Knowledge Graph - FAQ Bot",
    page_icon="🕸️",
    layout="wide"
)


def load_graph_data():
    """Load graph data from GraphML file."""
    kb_dir = Path(__file__).parent.parent / "kb"
    graphml_file = kb_dir / "graph_chunk_entity_relation.graphml"

    if not graphml_file.exists():
        return None

    # Load GraphML using NetworkX
    G = nx.read_graphml(str(graphml_file))
    return G


def create_graph_visualization(G, max_nodes=50, selected_types=None, min_connections=0, search_query=""):
    """Create interactive graph visualization from NetworkX graph with filtering.

    Args:
        G: NetworkX graph
        max_nodes: Maximum number of nodes to display
        selected_types: List of entity types to show (None = all)
        min_connections: Minimum number of connections per node
        search_query: Search string to filter nodes by name
    """
    nodes = []
    edges = []

    # Цветовая схема для типов сущностей
    type_colors = {
        'EVENT': '#FF6B6B',          # Красный
        'ORGANIZATION': '#4ECDC4',   # Бирюзовый
        'CONCEPT': '#95E1D3',        # Светло-зеленый
        'PERSON': '#FFD93D',         # Желтый
        'LOCATION': '#A8E6CF',       # Светло-зеленый
        'ROLE': '#DDA15E',           # Коричневый
        'TECHNOLOGY': '#606C38',     # Темно-зеленый
        'UNKNOWN': '#CCCCCC'         # Серый
    }

    # Фильтровать узлы по критериям
    filtered_nodes = []
    for node_id in G.nodes():
        entity_type = G.nodes[node_id].get('entity_type', 'UNKNOWN').strip('"')
        entity_name = node_id.strip('"').lower()

        # Фильтр по типам
        if selected_types and entity_type not in selected_types:
            continue

        # Фильтр по количеству связей
        node_connections = G.degree(node_id)
        if node_connections < min_connections:
            continue

        # Фильтр по поисковому запросу
        if search_query and search_query.lower() not in entity_name:
            continue

        filtered_nodes.append((node_id, node_connections))

    # Сортировка по количеству связей (самые связные узлы первыми)
    filtered_nodes.sort(key=lambda x: x[1], reverse=True)

    # Получить топ узлов (ограничить для производительности)
    all_nodes = [node_id for node_id, _ in filtered_nodes[:max_nodes]]
    entity_count = len(all_nodes)

    # Создать словарь node_id -> index и node_data для быстрого поиска
    node_id_map = {}
    node_data = {}

    for idx, node_id in enumerate(all_nodes):
        # Извлечь данные узла из GraphML
        entity_type = G.nodes[node_id].get('entity_type', 'UNKNOWN').strip('"')
        description = G.nodes[node_id].get('description', 'No description')
        entity_name = node_id.strip('"')

        # Количество связей для определения размера узла
        node_connections = G.degree(node_id)

        # Сократить описание для tooltip
        short_desc = description[:200] + "..." if len(description) > 200 else description

        # Определить цвет по типу
        color = type_colors.get(entity_type, type_colors['UNKNOWN'])

        # Динамический размер узла на основе количества связей (от 15 до 40)
        node_size = min(15 + node_connections * 2, 40)

        # Сохранить маппинг для создания ребер
        node_id_map[node_id] = idx

        # Сохранить данные узла для детального отображения
        node_data[idx] = {
            'id': node_id,
            'name': entity_name,
            'type': entity_type,
            'description': description,
            'connections': node_connections
        }

        # Сократить label для читаемости
        short_label = entity_name[:30] + "..." if len(entity_name) > 30 else entity_name

        nodes.append(
            Node(
                id=idx,
                label=short_label,
                size=node_size,
                color=color,
                title=f"📌 {entity_name}\n🏷️ Type: {entity_type}\n🔗 Connections: {node_connections}\n📝 {short_desc}",
                font={
                    'size': 14,
                    'color': '#ffffff',
                    'face': 'arial',
                    'strokeWidth': 3,
                    'strokeColor': '#000000'
                },
                shape="dot",
                borderWidth=2,
                borderWidthSelected=4
            )
        )

    # Извлечь рёбра только между отображаемыми узлами
    edge_count = 0
    for source, target in G.edges():
        # Проверить, что оба узла в подграфе
        if source in node_id_map and target in node_id_map:
            edge_data = G.edges[source, target]
            keywords = edge_data.get('keywords', '')
            weight = edge_data.get('weight', 1.0)

            # Определить ширину связи на основе веса
            try:
                edge_width = min(1 + float(weight) * 2, 5)
            except (ValueError, TypeError):
                edge_width = 2

            # Tooltip с полной информацией о связи
            edge_title = f"Relation: {keywords}" if keywords else "Semantic connection"

            edges.append(
                Edge(
                    source=node_id_map[source],
                    target=node_id_map[target],
                    label="",  # Убрать метки для чистоты визуализации
                    title=edge_title,
                    color={
                        "color": "#848484",
                        "opacity": 0.5
                    },
                    width=edge_width,
                    smooth={
                        "type": "continuous"
                    }
                )
            )
            edge_count += 1

    return nodes, edges, node_data, entity_count, edge_count


def main():
    """Main Knowledge Graph visualization page."""

    # Custom CSS
    st.markdown("""
        <style>
        /* Match chat page styling */
        .stButton > button {
            background-color: #4A90E2 !important;
            border-color: #4A90E2 !important;
            color: white !important;
        }

        .stButton > button:hover {
            background-color: #357ABD !important;
            border-color: #357ABD !important;
        }

        /* Info boxes */
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0f2f6;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.title("🕸️ Knowledge Graph")
    st.caption("Interactive visualization of the document knowledge base")

    # Load graph data
    with st.spinner("Loading knowledge graph data..."):
        G = load_graph_data()

    if G is None:
        st.error("❌ Knowledge base not found. Please index documents first.")
        st.info("💡 Run the indexing process to create the knowledge graph:\n\n`python -m src.indexing`")
        return

    # Get total statistics
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()

    # Count entity types
    entity_types = {}
    for node_id in G.nodes():
        entity_type = G.nodes[node_id].get('entity_type', 'UNKNOWN').strip('"')
        entity_types[entity_type] = entity_types.get(entity_type, 0) + 1

    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Фильтры графа")

        # Максимальное количество узлов
        max_nodes = st.slider(
            "Максимум узлов",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Ограничение количества отображаемых узлов"
        )

        # Фильтр по типам сущностей
        st.subheader("🏷️ Типы узлов")
        available_types = sorted(list(entity_types.keys()))

        # Выбрать все / Снять все
        col1, col2 = st.columns(2)
        with col1:
            select_all = st.button("✓ Все", use_container_width=True)
        with col2:
            deselect_all = st.button("✗ Снять", use_container_width=True)

        # Инициализировать состояние фильтра типов
        if 'selected_types' not in st.session_state or select_all:
            st.session_state.selected_types = available_types
        if deselect_all:
            st.session_state.selected_types = []

        selected_types = []
        for entity_type in available_types:
            count = entity_types[entity_type]
            is_selected = st.checkbox(
                f"{entity_type} ({count})",
                value=entity_type in st.session_state.selected_types,
                key=f"type_{entity_type}"
            )
            if is_selected:
                selected_types.append(entity_type)

        st.session_state.selected_types = selected_types

        st.divider()

        # Минимальное количество связей
        min_connections = st.slider(
            "Мин. количество связей",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            help="Показать только узлы с минимальным количеством связей"
        )

        # Поиск узла
        search_query = st.text_input(
            "🔍 Поиск узла",
            placeholder="Введите название...",
            help="Фильтровать узлы по названию"
        )

        st.divider()

        # Режим отображения
        st.subheader("📊 Режим отображения")
        view_mode = st.radio(
            "Выберите режим:",
            ["Сетевой", "Иерархический"],
            help="Сетевой - естественное расположение, Иерархический - древовидная структура"
        )

        st.divider()

        # Настройки физики (только для сетевого режима)
        if view_mode == "Сетевой":
            st.subheader("⚙️ Настройки физики")
            spring_length = st.slider(
                "Расстояние между узлами",
                min_value=100,
                max_value=500,
                value=200,
                step=25,
                help="Желаемое расстояние между связанными узлами"
            )

        st.divider()

        # Легенда
        st.subheader("🎨 Цвета узлов")
        st.markdown("""
        - 🔴 **EVENT**: События
        - 🔵 **ORGANIZATION**: Организации
        - 🟢 **CONCEPT**: Концепции
        - 🟡 **PERSON**: Люди
        - 🟢 **LOCATION**: Места
        - 🟤 **ROLE**: Роли
        - 🟢 **TECHNOLOGY**: Технологии
        - ⚪ **UNKNOWN**: Неизвестно

        💡 **Размер узла** = количество связей
        """)

        st.divider()

        # Статистика
        st.subheader("📊 Общая статистика")
        st.write(f"**Всего узлов:** {total_nodes}")
        st.write(f"**Всего связей:** {total_edges}")

    # Create visualization with filters
    with st.spinner("Строим интерактивный граф..."):
        nodes, edges, node_data, filtered_count, edge_count = create_graph_visualization(
            G,
            max_nodes=max_nodes,
            selected_types=selected_types if selected_types else None,
            min_connections=min_connections,
            search_query=search_query
        )

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего узлов", total_nodes)
    with col2:
        st.metric("Всего связей", total_edges)
    with col3:
        st.metric("Отображено узлов", len(nodes))
    with col4:
        st.metric("Отображено связей", edge_count)

    # Предупреждение если нет узлов после фильтрации
    if len(nodes) == 0:
        st.warning("⚠️ Нет узлов, соответствующих выбранным фильтрам. Попробуйте изменить критерии фильтрации.")
        return

    st.divider()

    # Graph configuration with advanced physics
    if view_mode == "Иерархический":
        # Иерархический режим
        config = Config(
            width="100%",
            height=900,
            directed=True,
            hierarchical=True,
            physics={
                'enabled': True,
                'hierarchicalRepulsion': {
                    'centralGravity': 0.0,
                    'springLength': 150,
                    'springConstant': 0.01,
                    'nodeDistance': 200,
                    'damping': 0.09
                },
                'solver': 'hierarchicalRepulsion',
                'stabilization': {'iterations': 1000}
            }
        )
    else:
        # Сетевой режим с улучшенной физикой forceAtlas2Based
        config = Config(
            width="100%",
            height=900,
            directed=True,
            hierarchical=False,
            physics={
                'enabled': True,
                'solver': 'forceAtlas2Based',
                'forceAtlas2Based': {
                    'gravitationalConstant': -50,
                    'centralGravity': 0.01,
                    'springLength': spring_length,
                    'springConstant': 0.08,
                    'damping': 0.4,
                    'avoidOverlap': 1
                },
                'stabilization': {
                    'enabled': True,
                    'iterations': 1000,
                    'updateInterval': 25
                }
            }
        )

    # Display graph
    if nodes and edges:
        st.subheader("📊 Интерактивный граф знаний")
        st.caption("🖱️ **Кликните на узел** для просмотра деталей. **Перетаскивайте узлы** для изменения расположения. **Наведите курсор** на узел/связь для подробной информации.")

        # Добавляем информацию о текущих настройках
        mode_text = "Иерархический" if view_mode == "Иерархический" else f"Сетевой (расстояние: {spring_length}px)"
        st.info(f"📊 Режим: {mode_text} | 👁️ Узлов: {len(nodes)} | 🔗 Связей: {edge_count}")

        return_value = agraph(nodes=nodes, edges=edges, config=config)

        # Обработка клика на узел
        if return_value:
            try:
                node_id = int(return_value)
                if node_id in node_data:
                    st.divider()
                    st.subheader("📝 Детали выбранного узла")

                    node_info = node_data[node_id]

                    # Отображение информации о узле
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📌 Название", node_info['name'])
                    with col2:
                        st.metric("🏷️ Тип", node_info['type'])
                    with col3:
                        st.metric("🔗 Связей", node_info['connections'])

                    st.markdown("**📝 Описание:**")
                    st.write(node_info['description'])

                    # Найти связанные узлы
                    st.markdown("**🔗 Связанные узлы:**")
                    related_nodes = []

                    for edge in edges:
                        if edge.source == node_id:
                            target_info = node_data.get(edge.target)
                            if target_info:
                                related_nodes.append({
                                    'Направление': '→',
                                    'Название': target_info['name'],
                                    'Тип': target_info['type'],
                                    'Связей': target_info['connections']
                                })
                        elif edge.target == node_id:
                            source_info = node_data.get(edge.source)
                            if source_info:
                                related_nodes.append({
                                    'Направление': '←',
                                    'Название': source_info['name'],
                                    'Тип': source_info['type'],
                                    'Связей': source_info['connections']
                                })

                    if related_nodes:
                        import pandas as pd
                        df = pd.DataFrame(related_nodes)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info("Нет связанных узлов в текущем отображении")

            except (ValueError, KeyError) as e:
                st.warning(f"Не удалось загрузить информацию об узле: {e}")
    else:
        st.warning("⚠️ Нет данных для отображения графа.")

    # Additional info
    with st.expander("ℹ️ О графе знаний и его использовании"):
        st.markdown("""
        ### 📚 Как это работает

        Этот интерактивный граф визуализирует знания, извлечённые из документов с помощью **MiniRAG**:
        1. 📄 Документы разбиваются на фрагменты (chunks)
        2. 🤖 AI извлекает сущности (люди, места, концепции, события и т.д.)
        3. 🔗 Определяются семантические связи между сущностями
        4. 📊 Граф визуализирует сеть концепций и их взаимосвязи

        ### 🎮 Интерактивные возможности

        - 👆 **Клик на узел** - просмотр полной информации и связанных узлов
        - 🖱️ **Перетаскивание** - изменение расположения узлов
        - 🔍 **Наведение курсора** - быстрый просмотр описания узла/связи
        - 🔎 **Масштабирование** - колесико мыши для zoom
        - 📌 **Закрепление** - перетащите узел для фиксации позиции

        ### 🎛️ Фильтры и настройки

        **Фильтры:**
        - 📊 **Максимум узлов** (10-200) - ограничение для производительности
        - 🏷️ **Типы узлов** - выборочное отображение по категориям
        - 🔗 **Мин. связей** - показать только важные узлы
        - 🔍 **Поиск** - найти конкретный узел по названию

        **Режимы отображения:**
        - 🕸️ **Сетевой** - естественное органическое расположение (forceAtlas2Based)
        - 🌲 **Иерархический** - древовидная структура сверху-вниз

        ### ⚙️ Алгоритм физики (Сетевой режим)

        Используется **forceAtlas2Based** - продвинутый алгоритм для больших графов:
        - `gravitationalConstant: -50` - отталкивание узлов друг от друга
        - `centralGravity: 0.01` - слабое притяжение к центру
        - `springLength: 100-500px` - желаемое расстояние между связанными узлами
        - `springConstant: 0.08` - жёсткость связей
        - `damping: 0.4` - замедление движения для стабилизации
        - `avoidOverlap: 1` - предотвращение наложения узлов
        - **Стабилизация:** 1000 итераций для достижения оптимального расположения

        ### 🎨 Визуальные подсказки

        - **Размер узла** = количество связей (больше связей → больше узел)
        - **Цвет узла** = тип сущности (см. легенду в сайдбаре)
        - **Толщина связи** = вес/важность связи
        - **Белый текст** с чёрной обводкой для максимальной читаемости

        ### 💡 Советы

        1. Начните с **малого количества узлов** (20-30) для изучения структуры
        2. Используйте **фильтр по типам** для фокусировки на интересующих сущностях
        3. **Увеличьте мин. связей** для отображения только ключевых узлов
        4. **Поиск узла** поможет найти конкретную концепцию
        5. **Иерархический режим** удобен для изучения направленных зависимостей
        """)


if __name__ == "__main__":
    main()
