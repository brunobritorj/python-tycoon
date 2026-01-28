"""
Tests for world map system.
"""

import pytest
import math
from tycoon_engine.entities.world_map import Node, Edge, WorldMap


def test_node_creation():
    """Test node creation."""
    node = Node(node_id="node_1", x=10.0, y=20.0, name="City A")
    assert node.node_id == "node_1"
    assert node.x == 10.0
    assert node.y == 20.0
    assert node.name == "City A"


def test_node_distance():
    """Test distance calculation between nodes."""
    node1 = Node(node_id="n1", x=0.0, y=0.0)
    node2 = Node(node_id="n2", x=3.0, y=4.0)
    
    distance = node1.distance_to(node2)
    assert distance == 5.0  # 3-4-5 triangle


def test_node_properties():
    """Test node custom properties."""
    node = Node(node_id="n1", x=0.0, y=0.0)
    
    node.set_property("population", 10000)
    node.set_property("type", "city")
    
    assert node.get_property("population") == 10000
    assert node.get_property("type") == "city"
    assert node.get_property("nonexistent", "default") == "default"


def test_node_serialization():
    """Test node serialization."""
    node = Node(
        node_id="n1",
        x=45.5,
        y=-73.6,
        name="Montreal",
        properties={"population": 1700000}
    )
    
    # Serialize
    data = node.to_dict()
    assert data['node_id'] == "n1"
    assert data['x'] == 45.5
    assert data['y'] == -73.6
    assert data['name'] == "Montreal"
    
    # Deserialize
    node2 = Node.from_dict(data)
    assert node2.node_id == "n1"
    assert node2.x == 45.5
    assert node2.y == -73.6
    assert node2.name == "Montreal"
    assert node2.properties["population"] == 1700000


def test_edge_creation():
    """Test edge creation."""
    edge = Edge(
        edge_id="e1",
        from_node="n1",
        to_node="n2",
        throughput=100.0
    )
    assert edge.edge_id == "e1"
    assert edge.from_node == "n1"
    assert edge.to_node == "n2"
    assert edge.throughput == 100.0
    assert edge.bidirectional is True


def test_edge_connects():
    """Test edge connection check."""
    edge = Edge(edge_id="e1", from_node="n1", to_node="n2")
    
    assert edge.connects("n1") is True
    assert edge.connects("n2") is True
    assert edge.connects("n3") is False


def test_edge_other_node():
    """Test getting the other node of an edge."""
    edge = Edge(edge_id="e1", from_node="n1", to_node="n2", bidirectional=True)
    
    assert edge.other_node("n1") == "n2"
    assert edge.other_node("n2") == "n1"
    assert edge.other_node("n3") is None


def test_edge_unidirectional():
    """Test unidirectional edge."""
    edge = Edge(edge_id="e1", from_node="n1", to_node="n2", bidirectional=False)
    
    assert edge.other_node("n1") == "n2"
    assert edge.other_node("n2") is None  # Can't go backwards


def test_edge_properties():
    """Test edge custom properties."""
    edge = Edge(edge_id="e1", from_node="n1", to_node="n2")
    
    edge.set_property("distance", 100)
    edge.set_property("type", "highway")
    
    assert edge.get_property("distance") == 100
    assert edge.get_property("type") == "highway"


def test_edge_serialization():
    """Test edge serialization."""
    edge = Edge(
        edge_id="e1",
        from_node="n1",
        to_node="n2",
        throughput=250.0,
        bidirectional=False,
        properties={"distance": 50}
    )
    
    # Serialize
    data = edge.to_dict()
    assert data['edge_id'] == "e1"
    assert data['from_node'] == "n1"
    assert data['to_node'] == "n2"
    assert data['throughput'] == 250.0
    assert data['bidirectional'] is False
    
    # Deserialize
    edge2 = Edge.from_dict(data)
    assert edge2.edge_id == "e1"
    assert edge2.from_node == "n1"
    assert edge2.to_node == "n2"
    assert edge2.throughput == 250.0
    assert edge2.bidirectional is False
    assert edge2.properties["distance"] == 50


def test_world_map_creation():
    """Test world map creation."""
    world_map = WorldMap()
    assert len(world_map.nodes) == 0
    assert len(world_map.edges) == 0


def test_world_map_add_node():
    """Test adding nodes to world map."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0, name="City A")
    assert node1 is not None
    assert len(world_map.nodes) == 1
    
    node2 = world_map.add_node(x=30.0, y=40.0, name="City B")
    assert len(world_map.nodes) == 2


def test_world_map_add_node_with_properties():
    """Test adding nodes with custom properties."""
    world_map = WorldMap()
    
    node = world_map.add_node(
        x=10.0,
        y=20.0,
        name="City",
        population=50000,
        type="urban"
    )
    
    assert node.get_property("population") == 50000
    assert node.get_property("type") == "urban"


def test_world_map_remove_node():
    """Test removing nodes."""
    world_map = WorldMap()
    
    node = world_map.add_node(x=10.0, y=20.0)
    node_id = node.node_id
    
    assert world_map.remove_node(node_id) is True
    assert world_map.remove_node(node_id) is False  # Already removed
    assert len(world_map.nodes) == 0


def test_world_map_get_node():
    """Test getting nodes."""
    world_map = WorldMap()
    
    node = world_map.add_node(x=10.0, y=20.0, name="Test")
    
    retrieved = world_map.get_node(node.node_id)
    assert retrieved == node
    assert retrieved.name == "Test"
    
    assert world_map.get_node("nonexistent") is None


def test_world_map_get_all_nodes():
    """Test getting all nodes."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    node3 = world_map.add_node(x=50.0, y=60.0)
    
    all_nodes = world_map.get_all_nodes()
    assert len(all_nodes) == 3
    assert node1 in all_nodes
    assert node2 in all_nodes
    assert node3 in all_nodes


def test_world_map_add_edge():
    """Test adding edges."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    
    edge = world_map.add_edge(node1.node_id, node2.node_id, throughput=100.0)
    
    assert edge is not None
    assert edge.from_node == node1.node_id
    assert edge.to_node == node2.node_id
    assert edge.throughput == 100.0
    assert len(world_map.edges) == 1


def test_world_map_add_edge_invalid_nodes():
    """Test adding edge with invalid nodes."""
    world_map = WorldMap()
    
    edge = world_map.add_edge("invalid1", "invalid2")
    assert edge is None
    assert len(world_map.edges) == 0


def test_world_map_remove_edge():
    """Test removing edges."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    edge = world_map.add_edge(node1.node_id, node2.node_id)
    
    edge_id = edge.edge_id
    assert world_map.remove_edge(edge_id) is True
    assert world_map.remove_edge(edge_id) is False  # Already removed
    assert len(world_map.edges) == 0


def test_world_map_remove_node_with_edges():
    """Test that removing a node also removes its edges."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    node3 = world_map.add_node(x=50.0, y=60.0)
    
    world_map.add_edge(node1.node_id, node2.node_id)
    world_map.add_edge(node1.node_id, node3.node_id)
    
    assert len(world_map.edges) == 2
    
    world_map.remove_node(node1.node_id)
    
    assert len(world_map.nodes) == 2
    assert len(world_map.edges) == 0  # Both edges removed


def test_world_map_get_node_edges():
    """Test getting edges connected to a node."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    node3 = world_map.add_node(x=50.0, y=60.0)
    
    edge1 = world_map.add_edge(node1.node_id, node2.node_id)
    edge2 = world_map.add_edge(node1.node_id, node3.node_id)
    world_map.add_edge(node2.node_id, node3.node_id)
    
    node1_edges = world_map.get_node_edges(node1.node_id)
    assert len(node1_edges) == 2
    assert edge1 in node1_edges
    assert edge2 in node1_edges


def test_world_map_get_neighbors():
    """Test getting neighbor nodes."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    node3 = world_map.add_node(x=50.0, y=60.0)
    
    world_map.add_edge(node1.node_id, node2.node_id)
    world_map.add_edge(node1.node_id, node3.node_id)
    
    neighbors = world_map.get_neighbors(node1.node_id)
    assert len(neighbors) == 2
    
    neighbor_ids = [n_id for n_id, _ in neighbors]
    assert node2.node_id in neighbor_ids
    assert node3.node_id in neighbor_ids


def test_world_map_find_path():
    """Test pathfinding."""
    world_map = WorldMap()
    
    # Create a simple path: A -> B -> C
    node_a = world_map.add_node(x=0.0, y=0.0, name="A")
    node_b = world_map.add_node(x=10.0, y=0.0, name="B")
    node_c = world_map.add_node(x=20.0, y=0.0, name="C")
    
    world_map.add_edge(node_a.node_id, node_b.node_id)
    world_map.add_edge(node_b.node_id, node_c.node_id)
    
    path = world_map.find_path(node_a.node_id, node_c.node_id)
    
    assert path is not None
    assert len(path) == 3
    assert path[0] == node_a.node_id
    assert path[1] == node_b.node_id
    assert path[2] == node_c.node_id


def test_world_map_find_path_no_path():
    """Test pathfinding when no path exists."""
    world_map = WorldMap()
    
    node_a = world_map.add_node(x=0.0, y=0.0)
    node_b = world_map.add_node(x=10.0, y=0.0)
    
    # No edge between them
    path = world_map.find_path(node_a.node_id, node_b.node_id)
    assert path is None


def test_world_map_find_path_same_node():
    """Test pathfinding from node to itself."""
    world_map = WorldMap()
    
    node = world_map.add_node(x=0.0, y=0.0)
    path = world_map.find_path(node.node_id, node.node_id)
    
    assert path == [node.node_id]


def test_world_map_nodes_in_radius():
    """Test finding nodes within radius."""
    world_map = WorldMap()
    
    # Create nodes at different distances from origin
    node1 = world_map.add_node(x=0.0, y=0.0)  # Distance 0
    node2 = world_map.add_node(x=3.0, y=4.0)  # Distance 5
    node3 = world_map.add_node(x=10.0, y=0.0)  # Distance 10
    
    # Find nodes within radius 6 from origin
    nodes = world_map.get_nodes_in_radius(0.0, 0.0, 6.0)
    
    assert len(nodes) == 2
    assert node1 in nodes
    assert node2 in nodes
    assert node3 not in nodes


def test_world_map_clear():
    """Test clearing world map."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0)
    node2 = world_map.add_node(x=30.0, y=40.0)
    world_map.add_edge(node1.node_id, node2.node_id)
    
    assert len(world_map.nodes) == 2
    assert len(world_map.edges) == 1
    
    world_map.clear()
    
    assert len(world_map.nodes) == 0
    assert len(world_map.edges) == 0


def test_world_map_generate_ids():
    """Test ID generation."""
    world_map = WorldMap()
    
    node_id1 = world_map.generate_node_id()
    node_id2 = world_map.generate_node_id()
    
    assert node_id1 != node_id2
    assert node_id1.startswith("node_")
    
    edge_id1 = world_map.generate_edge_id()
    edge_id2 = world_map.generate_edge_id()
    
    assert edge_id1 != edge_id2
    assert edge_id1.startswith("edge_")


def test_world_map_serialization():
    """Test world map serialization."""
    world_map = WorldMap()
    
    node1 = world_map.add_node(x=10.0, y=20.0, name="City A")
    node2 = world_map.add_node(x=30.0, y=40.0, name="City B")
    edge = world_map.add_edge(node1.node_id, node2.node_id, throughput=150.0)
    
    # Serialize
    data = world_map.to_dict()
    assert len(data['nodes']) == 2
    assert len(data['edges']) == 1
    
    # Deserialize
    world_map2 = WorldMap.from_dict(data)
    assert len(world_map2.nodes) == 2
    assert len(world_map2.edges) == 1
    
    # Verify node data
    node1_restored = world_map2.get_node(node1.node_id)
    assert node1_restored is not None
    assert node1_restored.name == "City A"
    assert node1_restored.x == 10.0
    assert node1_restored.y == 20.0
    
    # Verify edge data
    edge_restored = world_map2.get_edge(edge.edge_id)
    assert edge_restored is not None
    assert edge_restored.throughput == 150.0


def test_world_map_complex_graph():
    """Test a more complex graph structure."""
    world_map = WorldMap()
    
    # Create a pentagon of nodes
    nodes = []
    for i in range(5):
        angle = i * 2 * math.pi / 5
        x = 100 * math.cos(angle)
        y = 100 * math.sin(angle)
        node = world_map.add_node(x=x, y=y, name=f"Node {i}")
        nodes.append(node)
    
    # Connect each node to the next (pentagon edges)
    for i in range(5):
        world_map.add_edge(
            nodes[i].node_id,
            nodes[(i + 1) % 5].node_id,
            throughput=10.0
        )
    
    assert len(world_map.nodes) == 5
    assert len(world_map.edges) == 5
    
    # Check that we can find a path
    path = world_map.find_path(nodes[0].node_id, nodes[2].node_id)
    assert path is not None
    assert len(path) >= 3  # At least start, intermediate, end
