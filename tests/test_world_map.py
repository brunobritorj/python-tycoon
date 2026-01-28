"""
Tests for world map system.
"""

import pytest
import math
from tycoon_engine.systems.world_map import Node, Edge, WorldMap


def test_node_initialization():
    """Test node initialization."""
    node = Node("node_1", 100.0, 200.0, "city")
    
    assert node.id == "node_1"
    assert node.x == 100.0
    assert node.y == 200.0
    assert node.type == "city"
    assert len(node.properties) == 0


def test_node_position():
    """Test node position get/set."""
    node = Node("node_1", 10.0, 20.0)
    
    assert node.get_position() == (10.0, 20.0)
    
    node.set_position(50.0, 60.0)
    assert node.x == 50.0
    assert node.y == 60.0


def test_node_distance():
    """Test distance calculation between nodes."""
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 3.0, 4.0)
    
    # Distance should be 5 (3-4-5 triangle)
    distance = node1.distance_to(node2)
    assert abs(distance - 5.0) < 0.001


def test_node_properties():
    """Test node custom properties."""
    node = Node("node_1", 0.0, 0.0)
    
    node.set_property("population", 10000)
    node.set_property("resources", ["gold", "iron"])
    
    assert node.get_property("population") == 10000
    assert node.get_property("resources") == ["gold", "iron"]
    assert node.get_property("nonexistent", "default") == "default"


def test_node_edge_tracking():
    """Test node tracking of connected edges."""
    node = Node("node_1", 0.0, 0.0)
    
    node.add_edge("edge_1")
    node.add_edge("edge_2")
    
    edges = node.get_connected_edges()
    assert len(edges) == 2
    assert "edge_1" in edges
    assert "edge_2" in edges
    
    # Add duplicate - should not add again
    node.add_edge("edge_1")
    assert len(node.get_connected_edges()) == 2


def test_node_remove_edge():
    """Test removing edge from node."""
    node = Node("node_1", 0.0, 0.0)
    
    node.add_edge("edge_1")
    assert node.remove_edge("edge_1") is True
    assert node.remove_edge("edge_1") is False


def test_node_serialization():
    """Test node serialization."""
    node = Node("node_1", 100.0, 200.0, "city")
    node.set_property("name", "Capital")
    node.add_edge("edge_1")
    
    data = node.to_dict()
    assert data['id'] == "node_1"
    assert data['x'] == 100.0
    assert data['y'] == 200.0
    assert data['type'] == "city"
    assert data['properties']['name'] == "Capital"
    assert "edge_1" in data['connected_edges']
    
    # Deserialize
    node2 = Node.from_dict(data)
    assert node2.id == node.id
    assert node2.x == node.x
    assert node2.y == node.y
    assert node2.get_property("name") == "Capital"


def test_edge_initialization():
    """Test edge initialization."""
    edge = Edge("edge_1", "node_a", "node_b", throughput=10.0, bidirectional=True)
    
    assert edge.id == "edge_1"
    assert edge.from_node_id == "node_a"
    assert edge.to_node_id == "node_b"
    assert edge.throughput == 10.0
    assert edge.bidirectional is True
    assert edge.current_flow == 0.0


def test_edge_capacity():
    """Test edge capacity calculations."""
    edge = Edge("edge_1", "a", "b", throughput=100.0)
    
    assert edge.get_capacity_remaining() == 100.0
    assert edge.is_at_capacity() is False
    
    edge.current_flow = 50.0
    assert edge.get_capacity_remaining() == 50.0
    
    edge.current_flow = 100.0
    assert edge.is_at_capacity() is True
    assert edge.get_capacity_remaining() == 0.0


def test_edge_flow_management():
    """Test adding and removing flow."""
    edge = Edge("edge_1", "a", "b", throughput=100.0)
    
    # Add flow
    assert edge.add_flow(50.0) is True
    assert edge.current_flow == 50.0
    
    # Add more flow
    assert edge.add_flow(30.0) is True
    assert edge.current_flow == 80.0
    
    # Try to exceed capacity
    assert edge.add_flow(30.0) is False
    assert edge.current_flow == 80.0
    
    # Remove flow
    edge.remove_flow(30.0)
    assert edge.current_flow == 50.0


def test_edge_reset_flow():
    """Test resetting edge flow."""
    edge = Edge("edge_1", "a", "b", throughput=100.0)
    
    edge.add_flow(75.0)
    edge.reset_flow()
    
    assert edge.current_flow == 0.0


def test_edge_can_accommodate():
    """Test checking if edge can accommodate flow."""
    edge = Edge("edge_1", "a", "b", throughput=100.0)
    edge.current_flow = 70.0
    
    assert edge.can_accommodate(20.0) is True
    assert edge.can_accommodate(30.0) is True
    assert edge.can_accommodate(31.0) is False


def test_edge_connects():
    """Test checking if edge connects to a node."""
    edge = Edge("edge_1", "node_a", "node_b")
    
    assert edge.connects("node_a") is True
    assert edge.connects("node_b") is True
    assert edge.connects("node_c") is False


def test_edge_get_other_node():
    """Test getting the other node in an edge."""
    edge_bi = Edge("edge_1", "node_a", "node_b", bidirectional=True)
    edge_uni = Edge("edge_2", "node_a", "node_b", bidirectional=False)
    
    # Bidirectional edge
    assert edge_bi.get_other_node("node_a") == "node_b"
    assert edge_bi.get_other_node("node_b") == "node_a"
    
    # Unidirectional edge
    assert edge_uni.get_other_node("node_a") == "node_b"
    assert edge_uni.get_other_node("node_b") is None  # Can't go backwards
    
    # Non-connected node
    assert edge_bi.get_other_node("node_c") is None


def test_edge_properties():
    """Test edge custom properties."""
    edge = Edge("edge_1", "a", "b")
    
    edge.set_property("road_type", "highway")
    edge.set_property("condition", 0.9)
    
    assert edge.get_property("road_type") == "highway"
    assert edge.get_property("condition") == 0.9
    assert edge.get_property("nonexistent", "default") == "default"


def test_edge_serialization():
    """Test edge serialization."""
    edge = Edge("edge_1", "node_a", "node_b", throughput=50.0, bidirectional=False)
    edge.current_flow = 25.0
    edge.set_property("type", "road")
    
    data = edge.to_dict()
    assert data['id'] == "edge_1"
    assert data['from_node_id'] == "node_a"
    assert data['to_node_id'] == "node_b"
    assert data['throughput'] == 50.0
    assert data['bidirectional'] is False
    assert data['current_flow'] == 25.0
    assert data['properties']['type'] == "road"
    
    # Deserialize
    edge2 = Edge.from_dict(data)
    assert edge2.id == edge.id
    assert edge2.from_node_id == edge.from_node_id
    assert edge2.throughput == edge.throughput
    assert edge2.current_flow == edge.current_flow


def test_world_map_initialization():
    """Test world map initialization."""
    world_map = WorldMap("map_1")
    
    assert world_map.id == "map_1"
    assert len(world_map.nodes) == 0
    assert len(world_map.edges) == 0


def test_world_map_add_node():
    """Test adding nodes to world map."""
    world_map = WorldMap()
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    
    assert world_map.add_node(node1) is True
    assert world_map.add_node(node2) is True
    
    # Try to add duplicate
    assert world_map.add_node(node1) is False


def test_world_map_remove_node():
    """Test removing nodes from world map."""
    world_map = WorldMap()
    node = Node("n1", 0.0, 0.0)
    
    world_map.add_node(node)
    assert world_map.remove_node("n1") is True
    assert world_map.remove_node("n1") is False


def test_world_map_get_node():
    """Test getting node from world map."""
    world_map = WorldMap()
    node = Node("n1", 0.0, 0.0)
    
    world_map.add_node(node)
    
    retrieved = world_map.get_node("n1")
    assert retrieved == node
    
    assert world_map.get_node("nonexistent") is None


def test_world_map_add_edge():
    """Test adding edges to world map."""
    world_map = WorldMap()
    
    # Add nodes first
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    # Add edge
    edge = Edge("e1", "n1", "n2")
    assert world_map.add_edge(edge) is True
    
    # Check that nodes have edge registered
    assert "e1" in node1.get_connected_edges()
    assert "e1" in node2.get_connected_edges()


def test_world_map_add_edge_invalid_nodes():
    """Test adding edge with non-existent nodes."""
    world_map = WorldMap()
    
    # Add edge without nodes
    edge = Edge("e1", "n1", "n2")
    assert world_map.add_edge(edge) is False


def test_world_map_remove_edge():
    """Test removing edges from world map."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    edge = Edge("e1", "n1", "n2")
    world_map.add_edge(edge)
    
    assert world_map.remove_edge("e1") is True
    assert world_map.remove_edge("e1") is False
    
    # Check that nodes no longer have edge
    assert "e1" not in node1.get_connected_edges()
    assert "e1" not in node2.get_connected_edges()


def test_world_map_remove_node_removes_edges():
    """Test that removing a node also removes connected edges."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    edge = Edge("e1", "n1", "n2")
    world_map.add_edge(edge)
    
    # Remove node
    world_map.remove_node("n1")
    
    # Edge should also be removed
    assert world_map.get_edge("e1") is None


def test_world_map_get_edges_from_node():
    """Test getting edges connected to a node."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    node3 = Node("n3", 20.0, 20.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    world_map.add_node(node3)
    
    edge1 = Edge("e1", "n1", "n2")
    edge2 = Edge("e2", "n1", "n3")
    world_map.add_edge(edge1)
    world_map.add_edge(edge2)
    
    edges = world_map.get_edges_from_node("n1")
    assert len(edges) == 2
    assert edge1 in edges
    assert edge2 in edges


def test_world_map_get_neighbors():
    """Test getting neighboring nodes."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    node3 = Node("n3", 20.0, 20.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    world_map.add_node(node3)
    
    edge1 = Edge("e1", "n1", "n2")
    edge2 = Edge("e2", "n1", "n3")
    world_map.add_edge(edge1)
    world_map.add_edge(edge2)
    
    neighbors = world_map.get_neighbors("n1")
    assert len(neighbors) == 2
    assert node2 in neighbors
    assert node3 in neighbors


def test_world_map_get_all():
    """Test getting all nodes and edges."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    edge = Edge("e1", "n1", "n2")
    world_map.add_edge(edge)
    
    all_nodes = world_map.get_all_nodes()
    assert len(all_nodes) == 2
    
    all_edges = world_map.get_all_edges()
    assert len(all_edges) == 1


def test_world_map_clear():
    """Test clearing the world map."""
    world_map = WorldMap()
    
    node1 = Node("n1", 0.0, 0.0)
    node2 = Node("n2", 10.0, 10.0)
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    edge = Edge("e1", "n1", "n2")
    world_map.add_edge(edge)
    
    world_map.clear()
    
    assert len(world_map.get_all_nodes()) == 0
    assert len(world_map.get_all_edges()) == 0


def test_world_map_serialization():
    """Test world map serialization."""
    world_map = WorldMap("test_map")
    
    node1 = Node("n1", 0.0, 0.0, "city")
    node2 = Node("n2", 10.0, 10.0, "town")
    world_map.add_node(node1)
    world_map.add_node(node2)
    
    edge = Edge("e1", "n1", "n2", throughput=50.0)
    world_map.add_edge(edge)
    
    # Serialize
    data = world_map.to_dict()
    assert data['id'] == "test_map"
    assert 'n1' in data['nodes']
    assert 'n2' in data['nodes']
    assert 'e1' in data['edges']
    
    # Deserialize
    world_map2 = WorldMap.from_dict(data)
    assert world_map2.id == world_map.id
    assert world_map2.get_node("n1") is not None
    assert world_map2.get_node("n2") is not None
    assert world_map2.get_edge("e1") is not None
