"""Test script for Knowledge Graph visualization improvements."""
import sys
import importlib.util
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import networkx as nx

# Load module with emoji in filename
module_path = Path(__file__).parent.parent / "pages" / "2_🕸️_Knowledge_Graph.py"
spec = importlib.util.spec_from_file_location("knowledge_graph", module_path)
knowledge_graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(knowledge_graph)

load_graph_data = knowledge_graph.load_graph_data
create_graph_visualization = knowledge_graph.create_graph_visualization


def test_load_graph():
    """Test loading graph data."""
    print("🧪 Test 1: Loading graph data...")
    G = load_graph_data()

    if G is None:
        print("   ❌ FAILED: Graph data not found")
        return False

    print(f"   ✅ PASSED: Loaded {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return True


def test_basic_visualization(G):
    """Test basic visualization without filters."""
    print("\n🧪 Test 2: Basic visualization (50 nodes)...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(G, max_nodes=50)
        print(f"   ✅ PASSED: Created {len(nodes)} nodes and {len(edges)} edges")
        print(f"      - Entity count: {entity_count}")
        print(f"      - Edge count: {edge_count}")
        return True
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_type_filter(G):
    """Test filtering by entity types."""
    print("\n🧪 Test 3: Filtering by entity type (CONCEPT only)...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(
            G,
            max_nodes=50,
            selected_types=['CONCEPT']
        )

        # Verify all nodes are CONCEPT type
        all_concept = all(node_data[node_id]['type'] == 'CONCEPT' for node_id in node_data)

        if all_concept:
            print(f"   ✅ PASSED: All {len(nodes)} nodes are CONCEPT type")
            return True
        else:
            print(f"   ❌ FAILED: Found non-CONCEPT nodes")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_connection_filter(G):
    """Test filtering by minimum connections."""
    print("\n🧪 Test 4: Filtering by min connections (min=3)...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(
            G,
            max_nodes=50,
            min_connections=3
        )

        # Verify all nodes have at least 3 connections
        all_valid = all(node_data[node_id]['connections'] >= 3 for node_id in node_data)

        if all_valid:
            min_conn = min(node_data[node_id]['connections'] for node_id in node_data) if node_data else 0
            max_conn = max(node_data[node_id]['connections'] for node_id in node_data) if node_data else 0
            print(f"   ✅ PASSED: All {len(nodes)} nodes have 3+ connections")
            print(f"      - Connection range: {min_conn} to {max_conn}")
            return True
        else:
            print(f"   ❌ FAILED: Found nodes with < 3 connections")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_search_filter(G):
    """Test search functionality."""
    print("\n🧪 Test 5: Search filter (query='agent')...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(
            G,
            max_nodes=50,
            search_query="agent"
        )

        # Verify all nodes contain 'agent' in name
        all_match = all('agent' in node_data[node_id]['name'].lower() for node_id in node_data)

        if all_match or len(nodes) == 0:
            print(f"   ✅ PASSED: Found {len(nodes)} nodes matching 'agent'")
            if node_data:
                print(f"      - Sample: {list(node_data.values())[0]['name']}")
            return True
        else:
            print(f"   ❌ FAILED: Found non-matching nodes")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_combined_filters(G):
    """Test multiple filters combined."""
    print("\n🧪 Test 6: Combined filters (type=CONCEPT, min_conn=2, search='system')...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(
            G,
            max_nodes=50,
            selected_types=['CONCEPT'],
            min_connections=2,
            search_query="system"
        )

        print(f"   ✅ PASSED: Filters applied successfully")
        print(f"      - Nodes: {len(nodes)}")
        print(f"      - Edges: {len(edges)}")
        if node_data:
            print(f"      - Sample: {list(node_data.values())[0]['name']} ({list(node_data.values())[0]['connections']} connections)")
        return True
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_node_properties(G):
    """Test node properties (size, tooltips)."""
    print("\n🧪 Test 7: Node properties...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(G, max_nodes=20)

        # Check node properties
        node = nodes[0]
        has_title = hasattr(node, 'title') and node.title is not None
        has_size = hasattr(node, 'size') and node.size > 0
        has_color = hasattr(node, 'color') and node.color is not None
        has_font = hasattr(node, 'font') and isinstance(node.font, dict)

        if all([has_title, has_size, has_color, has_font]):
            print(f"   ✅ PASSED: Node properties are correct")
            print(f"      - Title: {node.title[:50]}...")
            print(f"      - Size: {node.size}")
            print(f"      - Color: {node.color}")
            print(f"      - Font: {node.font}")
            return True
        else:
            print(f"   ❌ FAILED: Missing node properties")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def test_edge_properties(G):
    """Test edge properties (no labels, tooltips, opacity)."""
    print("\n🧪 Test 8: Edge properties...")

    try:
        nodes, edges, node_data, entity_count, edge_count = create_graph_visualization(G, max_nodes=20)

        if not edges:
            print(f"   ⚠️  SKIPPED: No edges in visualization")
            return True

        # Check edge properties
        edge = edges[0]
        no_label = edge.label == ""
        has_title = hasattr(edge, 'title') and edge.title is not None
        has_color = hasattr(edge, 'color') and isinstance(edge.color, dict)
        has_smooth = hasattr(edge, 'smooth') and isinstance(edge.smooth, dict)

        if all([no_label, has_title, has_color, has_smooth]):
            print(f"   ✅ PASSED: Edge properties are correct")
            print(f"      - Label: '{edge.label}' (empty)")
            print(f"      - Title: {edge.title}")
            print(f"      - Color: {edge.color}")
            print(f"      - Smooth: {edge.smooth}")
            return True
        else:
            print(f"   ❌ FAILED: Incorrect edge properties")
            print(f"      - no_label: {no_label}, has_title: {has_title}, has_color: {has_color}, has_smooth: {has_smooth}")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Knowledge Graph Visualization Test Suite")
    print("=" * 60)

    # Load graph
    G = load_graph_data()
    if G is None:
        print("\n❌ Cannot proceed: Graph data not found")
        return

    # Run tests
    tests = [
        ("Load graph data", lambda: test_load_graph()),
        ("Basic visualization", lambda: test_basic_visualization(G)),
        ("Type filter", lambda: test_type_filter(G)),
        ("Connection filter", lambda: test_connection_filter(G)),
        ("Search filter", lambda: test_search_filter(G)),
        ("Combined filters", lambda: test_combined_filters(G)),
        ("Node properties", lambda: test_node_properties(G)),
        ("Edge properties", lambda: test_edge_properties(G)),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")

    print("-" * 60)
    print(f"Result: {passed}/{total} tests passed ({passed*100//total}%)")

    if passed == total:
        print("\n🎉 All tests passed! Graph visualization is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")


if __name__ == "__main__":
    main()
