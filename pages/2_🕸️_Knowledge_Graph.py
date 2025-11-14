"""Knowledge Graph visualization page for FAQ Bot."""
import os
import sys
import json
import streamlit as st
from pathlib import Path
from streamlit_agraph import agraph, Node, Edge, Config

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
    """Load graph data from MiniRAG knowledge base."""
    kb_dir = Path(__file__).parent.parent / "kb"

    # Load entities
    entities_file = kb_dir / "vdb_entities.json"
    relationships_file = kb_dir / "vdb_relationships.json"

    if not entities_file.exists() or not relationships_file.exists():
        return None, None

    with open(entities_file, 'r', encoding='utf-8') as f:
        entities_data = json.load(f)

    with open(relationships_file, 'r', encoding='utf-8') as f:
        relationships_data = json.load(f)

    return entities_data, relationships_data


def create_graph_visualization(entities_data, relationships_data, max_nodes=50):
    """Create interactive graph visualization using streamlit-agraph."""
    nodes = []
    edges = []

    # Extract entities (limit to max_nodes for performance)
    entity_count = 0
    entity_map = {}

    if entities_data and 'data' in entities_data:
        for entity_id, entity_info in list(entities_data['data'].items())[:max_nodes]:
            entity_count += 1
            entity_name = entity_info.get('entity_name', f'Entity {entity_id}')
            entity_type = entity_info.get('entity_type', 'unknown')
            description = entity_info.get('description', '')[:100]  # Truncate description

            # Map entity name to ID for edge creation
            entity_map[entity_name] = entity_id

            # Determine node color based on entity type
            color = "#4A90E2"  # Default blue
            if entity_type.lower() in ['person', 'people']:
                color = "#E74C3C"  # Red for people
            elif entity_type.lower() in ['organization', 'company']:
                color = "#9B59B6"  # Purple for organizations
            elif entity_type.lower() in ['location', 'place']:
                color = "#2ECC71"  # Green for locations
            elif entity_type.lower() in ['concept', 'idea']:
                color = "#F39C12"  # Orange for concepts

            nodes.append(
                Node(
                    id=entity_id,
                    label=entity_name[:30],  # Truncate long names
                    size=20,
                    color=color,
                    title=f"{entity_name}\nType: {entity_type}\n{description}"
                )
            )

    # Extract relationships (limit for performance)
    edge_count = 0
    if relationships_data and 'data' in relationships_data:
        for _, rel_info in list(relationships_data['data'].items())[:max_nodes * 2]:
            src_name = rel_info.get('src_tgt', ['', ''])[0]
            tgt_name = rel_info.get('src_tgt', ['', ''])[1]
            relation_type = rel_info.get('keywords', 'relates to')

            # Get entity IDs from names
            src_id = entity_map.get(src_name)
            tgt_id = entity_map.get(tgt_name)

            if src_id and tgt_id:
                edge_count += 1
                edges.append(
                    Edge(
                        source=src_id,
                        target=tgt_id,
                        label=relation_type[:20],  # Truncate long labels
                        color="#95A5A6"
                    )
                )

    return nodes, edges, entity_count, edge_count


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
        entities_data, relationships_data = load_graph_data()

    if entities_data is None or relationships_data is None:
        st.error("❌ Knowledge base not found. Please index documents first.")
        st.info("💡 Run the indexing process to create the knowledge graph:\n\n`python -m src.indexing`")
        return

    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Graph Controls")

        max_nodes = st.slider(
            "Maximum nodes",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Limit number of nodes for better performance"
        )

        st.divider()

        # Legend
        st.subheader("🎨 Node Colors")
        st.markdown("""
        - 🔴 **Red**: People
        - 🟣 **Purple**: Organizations
        - 🟢 **Green**: Locations
        - 🟠 **Orange**: Concepts
        - 🔵 **Blue**: Other entities
        """)

    # Create visualization
    with st.spinner("Building interactive graph..."):
        nodes, edges, entity_count, edge_count = create_graph_visualization(
            entities_data,
            relationships_data,
            max_nodes=max_nodes
        )

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Entities", entity_count)
    with col2:
        st.metric("Total Relationships", edge_count)
    with col3:
        st.metric("Displayed Nodes", len(nodes))

    st.divider()

    # Graph configuration
    config = Config(
        width="100%",
        height=600,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False,
        node={
            'labelProperty': 'label',
            'renderLabel': True,
            'fontSize': 12,
            'fontColor': 'black'
        },
        link={
            'labelProperty': 'label',
            'renderLabel': True,
            'fontSize': 10,
            'fontColor': '#666'
        }
    )

    # Display graph
    if nodes and edges:
        st.subheader("📊 Interactive Knowledge Graph")
        st.caption("Click and drag nodes to explore relationships. Hover over nodes for details.")

        return_value = agraph(nodes=nodes, edges=edges, config=config)

        # Show selected node info
        if return_value:
            st.info(f"Selected: {return_value}")
    else:
        st.warning("⚠️ No graph data available to display.")

    # Additional info
    with st.expander("ℹ️ About the Knowledge Graph"):
        st.markdown("""
        This interactive graph visualizes the knowledge extracted from your documents using MiniRAG.

        **How it works:**
        1. Documents are split into chunks
        2. AI extracts entities (people, places, concepts, etc.)
        3. Relationships between entities are identified
        4. The graph shows connections between concepts

        **Tips:**
        - Drag nodes to rearrange the layout
        - Hover over nodes to see detailed information
        - Adjust "Maximum nodes" in the sidebar to show more/fewer entities
        - Different colors represent different entity types
        """)


if __name__ == "__main__":
    main()
