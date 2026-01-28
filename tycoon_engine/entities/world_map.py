"""
World/Map system for tycoon games.

Provides nodes with position and edges with throughput for game world representation.
"""

from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass, field
import math


@dataclass
class Node:
    """
    Represents a node in the world map.
    
    Nodes have x,y coordinates (latitude/longitude) and can store custom properties.
    """
    
    node_id: str
    x: float  # Latitude or x-coordinate
    y: float  # Longitude or y-coordinate
    name: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def distance_to(self, other: "Node") -> float:
        """
        Calculate Euclidean distance to another node.
        
        Args:
            other: Another node
            
        Returns:
            Distance between nodes
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'node_id': self.node_id,
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'properties': self.properties.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Deserialize from dictionary."""
        return cls(
            node_id=data['node_id'],
            x=data['x'],
            y=data['y'],
            name=data.get('name'),
            properties=data.get('properties', {}).copy()
        )


@dataclass
class Edge:
    """
    Represents an edge connecting two nodes.
    
    Edges have throughput and can store custom properties.
    """
    
    edge_id: str
    from_node: str  # Node ID
    to_node: str  # Node ID
    throughput: float = 1.0  # Capacity or flow rate
    bidirectional: bool = True
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def connects(self, node_id: str) -> bool:
        """Check if this edge connects to a specific node."""
        return node_id == self.from_node or node_id == self.to_node
    
    def other_node(self, node_id: str) -> Optional[str]:
        """
        Get the other node connected by this edge.
        
        Args:
            node_id: One of the nodes
            
        Returns:
            The other node ID, or None if node_id is not part of this edge
        """
        if node_id == self.from_node:
            return self.to_node
        elif node_id == self.to_node and self.bidirectional:
            return self.from_node
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'edge_id': self.edge_id,
            'from_node': self.from_node,
            'to_node': self.to_node,
            'throughput': self.throughput,
            'bidirectional': self.bidirectional,
            'properties': self.properties.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        """Deserialize from dictionary."""
        return cls(
            edge_id=data['edge_id'],
            from_node=data['from_node'],
            to_node=data['to_node'],
            throughput=data.get('throughput', 1.0),
            bidirectional=data.get('bidirectional', True),
            properties=data.get('properties', {}).copy()
        )


class WorldMap:
    """
    Manages the game world as a graph of nodes and edges.
    
    Provides methods for adding, removing, and querying nodes and edges.
    """
    
    def __init__(self):
        """Initialize world map."""
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self._next_node_id = 0
        self._next_edge_id = 0
    
    def add_node(
        self,
        x: float,
        y: float,
        name: Optional[str] = None,
        node_id: Optional[str] = None,
        **properties
    ) -> Node:
        """
        Add a node to the map.
        
        Args:
            x: X coordinate (latitude)
            y: Y coordinate (longitude)
            name: Optional name for the node
            node_id: Optional custom node ID, auto-generated if None
            **properties: Additional properties for the node
            
        Returns:
            The created Node
        """
        if node_id is None:
            node_id = self.generate_node_id()
        
        node = Node(
            node_id=node_id,
            x=x,
            y=y,
            name=name,
            properties=properties
        )
        
        self.nodes[node_id] = node
        return node
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node and all its connected edges.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            True if removed, False if not found
        """
        if node_id not in self.nodes:
            return False
        
        # Remove all edges connected to this node
        edges_to_remove = [
            edge_id for edge_id, edge in self.edges.items()
            if edge.connects(node_id)
        ]
        
        for edge_id in edges_to_remove:
            del self.edges[edge_id]
        
        del self.nodes[node_id]
        return True
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[Node]:
        """Get all nodes."""
        return list(self.nodes.values())
    
    def add_edge(
        self,
        from_node: str,
        to_node: str,
        throughput: float = 1.0,
        bidirectional: bool = True,
        edge_id: Optional[str] = None,
        **properties
    ) -> Optional[Edge]:
        """
        Add an edge between two nodes.
        
        Args:
            from_node: Source node ID
            to_node: Target node ID
            throughput: Edge throughput/capacity
            bidirectional: Whether edge works both ways
            edge_id: Optional custom edge ID, auto-generated if None
            **properties: Additional properties for the edge
            
        Returns:
            The created Edge, or None if nodes don't exist
        """
        # Validate nodes exist
        if from_node not in self.nodes or to_node not in self.nodes:
            return None
        
        if edge_id is None:
            edge_id = self.generate_edge_id()
        
        edge = Edge(
            edge_id=edge_id,
            from_node=from_node,
            to_node=to_node,
            throughput=throughput,
            bidirectional=bidirectional,
            properties=properties
        )
        
        self.edges[edge_id] = edge
        return edge
    
    def remove_edge(self, edge_id: str) -> bool:
        """
        Remove an edge.
        
        Args:
            edge_id: ID of the edge to remove
            
        Returns:
            True if removed, False if not found
        """
        if edge_id in self.edges:
            del self.edges[edge_id]
            return True
        return False
    
    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Get an edge by ID."""
        return self.edges.get(edge_id)
    
    def get_all_edges(self) -> List[Edge]:
        """Get all edges."""
        return list(self.edges.values())
    
    def get_node_edges(self, node_id: str) -> List[Edge]:
        """
        Get all edges connected to a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            List of edges connected to the node
        """
        return [
            edge for edge in self.edges.values()
            if edge.connects(node_id)
        ]
    
    def get_neighbors(self, node_id: str) -> List[Tuple[str, Edge]]:
        """
        Get all neighboring nodes and the edges connecting them.
        
        Args:
            node_id: Node ID
            
        Returns:
            List of tuples (neighbor_node_id, edge)
        """
        neighbors = []
        for edge in self.edges.values():
            other = edge.other_node(node_id)
            if other:
                neighbors.append((other, edge))
        return neighbors
    
    def find_path(self, from_node: str, to_node: str) -> Optional[List[str]]:
        """
        Find a path between two nodes using BFS.
        
        Args:
            from_node: Starting node ID
            to_node: Target node ID
            
        Returns:
            List of node IDs forming the path, or None if no path exists
        """
        if from_node not in self.nodes or to_node not in self.nodes:
            return None
        
        if from_node == to_node:
            return [from_node]
        
        # BFS
        visited = {from_node}
        queue = [(from_node, [from_node])]
        
        while queue:
            current, path = queue.pop(0)
            
            for neighbor_id, _ in self.get_neighbors(current):
                if neighbor_id == to_node:
                    return path + [neighbor_id]
                
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))
        
        return None
    
    def get_nodes_in_radius(
        self,
        center_x: float,
        center_y: float,
        radius: float
    ) -> List[Node]:
        """
        Get all nodes within a radius of a point.
        
        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Search radius
            
        Returns:
            List of nodes within radius
        """
        result = []
        for node in self.nodes.values():
            dx = node.x - center_x
            dy = node.y - center_y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= radius:
                result.append(node)
        return result
    
    def clear(self) -> None:
        """Remove all nodes and edges."""
        self.nodes.clear()
        self.edges.clear()
    
    def generate_node_id(self, prefix: str = "node") -> str:
        """Generate a unique node ID."""
        node_id = f"{prefix}_{self._next_node_id}"
        self._next_node_id += 1
        return node_id
    
    def generate_edge_id(self, prefix: str = "edge") -> str:
        """Generate a unique edge ID."""
        edge_id = f"{prefix}_{self._next_edge_id}"
        self._next_edge_id += 1
        return edge_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'nodes': {
                node_id: node.to_dict()
                for node_id, node in self.nodes.items()
            },
            'edges': {
                edge_id: edge.to_dict()
                for edge_id, edge in self.edges.items()
            },
            'next_node_id': self._next_node_id,
            'next_edge_id': self._next_edge_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldMap":
        """Deserialize from dictionary."""
        world_map = cls()
        
        # Restore nodes
        for node_id, node_data in data.get('nodes', {}).items():
            node = Node.from_dict(node_data)
            world_map.nodes[node_id] = node
        
        # Restore edges
        for edge_id, edge_data in data.get('edges', {}).items():
            edge = Edge.from_dict(edge_data)
            world_map.edges[edge_id] = edge
        
        world_map._next_node_id = data.get('next_node_id', 0)
        world_map._next_edge_id = data.get('next_edge_id', 0)
        
        return world_map
