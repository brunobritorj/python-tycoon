"""
World/Map system for tycoon games.

Provides a nodes and edges system for representing game worlds with
spatial relationships and connections.
"""

from typing import Dict, Any, Optional, List, Tuple
import math


class Node:
    """
    Represents a node in the world map.
    
    Nodes can represent locations, cities, buildings, or any spatial point
    in the game world.
    """
    
    def __init__(self, node_id: str, x: float, y: float, node_type: str = "default"):
        """
        Initialize a node.
        
        Args:
            node_id: Unique identifier for this node
            x: X position in world coordinates
            y: Y position in world coordinates
            node_type: Type classification (e.g., 'city', 'resource', 'hub')
        """
        self.id = node_id
        self.x = x
        self.y = y
        self.type = node_type
        
        # Custom properties for game-specific data
        self.properties: Dict[str, Any] = {}
        
        # Track connected edges
        self._connected_edges: List[str] = []
    
    def get_position(self) -> Tuple[float, float]:
        """Get node position as tuple."""
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """Set node position."""
        self.x = x
        self.y = y
    
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
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def add_edge(self, edge_id: str) -> None:
        """
        Register an edge connection.
        
        Args:
            edge_id: ID of the connecting edge
        """
        if edge_id not in self._connected_edges:
            self._connected_edges.append(edge_id)
    
    def remove_edge(self, edge_id: str) -> bool:
        """
        Remove an edge connection.
        
        Args:
            edge_id: ID of the edge to remove
            
        Returns:
            True if removed, False if not found
        """
        try:
            self._connected_edges.remove(edge_id)
            return True
        except ValueError:
            return False
    
    def get_connected_edges(self) -> List[str]:
        """Get list of connected edge IDs."""
        return self._connected_edges.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize node to dictionary."""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'type': self.type,
            'properties': self.properties.copy(),
            'connected_edges': self._connected_edges.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Deserialize node from dictionary."""
        node = cls(
            node_id=data['id'],
            x=data['x'],
            y=data['y'],
            node_type=data.get('type', 'default')
        )
        node.properties = data.get('properties', {}).copy()
        node._connected_edges = data.get('connected_edges', []).copy()
        return node


class Edge:
    """
    Represents an edge (connection) between two nodes.
    
    Edges can represent roads, routes, connections, or any relationship
    between nodes with throughput capacity.
    """
    
    def __init__(
        self,
        edge_id: str,
        from_node_id: str,
        to_node_id: str,
        throughput: float = 1.0,
        bidirectional: bool = True
    ):
        """
        Initialize an edge.
        
        Args:
            edge_id: Unique identifier for this edge
            from_node_id: ID of the source node
            to_node_id: ID of the destination node
            throughput: Maximum flow capacity (e.g., traffic, goods per second)
            bidirectional: Whether edge can be traversed in both directions
        """
        self.id = edge_id
        self.from_node_id = from_node_id
        self.to_node_id = to_node_id
        self.throughput = throughput
        self.bidirectional = bidirectional
        
        # Current flow through this edge
        self.current_flow = 0.0
        
        # Custom properties for game-specific data
        self.properties: Dict[str, Any] = {}
    
    def get_capacity_remaining(self) -> float:
        """
        Get remaining capacity on this edge.
        
        Returns:
            Amount of throughput still available
        """
        return max(0.0, self.throughput - self.current_flow)
    
    def is_at_capacity(self) -> bool:
        """Check if edge is at maximum capacity."""
        return self.current_flow >= self.throughput
    
    def can_accommodate(self, flow: float) -> bool:
        """
        Check if edge can accommodate additional flow.
        
        Args:
            flow: Amount of flow to check
            
        Returns:
            True if edge can handle the additional flow
        """
        return (self.current_flow + flow) <= self.throughput
    
    def add_flow(self, amount: float) -> bool:
        """
        Add flow to this edge.
        
        Args:
            amount: Amount of flow to add
            
        Returns:
            True if flow was added, False if would exceed capacity
        """
        if self.can_accommodate(amount):
            self.current_flow += amount
            return True
        return False
    
    def remove_flow(self, amount: float) -> None:
        """
        Remove flow from this edge.
        
        Args:
            amount: Amount of flow to remove
        """
        self.current_flow = max(0.0, self.current_flow - amount)
    
    def reset_flow(self) -> None:
        """Reset current flow to zero."""
        self.current_flow = 0.0
    
    def connects(self, node_id: str) -> bool:
        """
        Check if edge connects to a specific node.
        
        Args:
            node_id: ID of the node to check
            
        Returns:
            True if edge connects to the node
        """
        return node_id == self.from_node_id or node_id == self.to_node_id
    
    def get_other_node(self, node_id: str) -> Optional[str]:
        """
        Get the ID of the other node connected by this edge.
        
        Args:
            node_id: ID of one node
            
        Returns:
            ID of the other node, or None if node_id is not connected
        """
        if node_id == self.from_node_id:
            return self.to_node_id
        elif node_id == self.to_node_id:
            return self.from_node_id if self.bidirectional else None
        return None
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get a custom property."""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """Set a custom property."""
        self.properties[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize edge to dictionary."""
        return {
            'id': self.id,
            'from_node_id': self.from_node_id,
            'to_node_id': self.to_node_id,
            'throughput': self.throughput,
            'bidirectional': self.bidirectional,
            'current_flow': self.current_flow,
            'properties': self.properties.copy()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        """Deserialize edge from dictionary."""
        edge = cls(
            edge_id=data['id'],
            from_node_id=data['from_node_id'],
            to_node_id=data['to_node_id'],
            throughput=data.get('throughput', 1.0),
            bidirectional=data.get('bidirectional', True)
        )
        edge.current_flow = data.get('current_flow', 0.0)
        edge.properties = data.get('properties', {}).copy()
        return edge


class WorldMap:
    """
    Manages the world map with nodes and edges.
    
    Provides graph-based world representation with spatial information.
    """
    
    def __init__(self, map_id: str = "default"):
        """
        Initialize the world map.
        
        Args:
            map_id: Unique identifier for this map
        """
        self.id = map_id
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
    
    def add_node(self, node: Node) -> bool:
        """
        Add a node to the map.
        
        Args:
            node: Node to add
            
        Returns:
            True if added, False if ID already exists
        """
        if node.id in self.nodes:
            return False
        
        self.nodes[node.id] = node
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node from the map.
        
        Also removes all edges connected to this node.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            True if removed, False if not found
        """
        if node_id not in self.nodes:
            return False
        
        # Get connected edges before removing node
        node = self.nodes[node_id]
        edges_to_remove = node.get_connected_edges()
        
        # Remove the node
        del self.nodes[node_id]
        
        # Remove connected edges
        for edge_id in edges_to_remove:
            self.remove_edge(edge_id)
        
        return True
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """
        Get a node by ID.
        
        Args:
            node_id: ID of the node
            
        Returns:
            Node or None if not found
        """
        return self.nodes.get(node_id)
    
    def add_edge(self, edge: Edge) -> bool:
        """
        Add an edge to the map.
        
        Args:
            edge: Edge to add
            
        Returns:
            True if added, False if ID already exists or nodes don't exist
        """
        # Check if edge ID already exists
        if edge.id in self.edges:
            return False
        
        # Check if both nodes exist
        if edge.from_node_id not in self.nodes or edge.to_node_id not in self.nodes:
            return False
        
        # Add edge
        self.edges[edge.id] = edge
        
        # Register edge with nodes
        self.nodes[edge.from_node_id].add_edge(edge.id)
        self.nodes[edge.to_node_id].add_edge(edge.id)
        
        return True
    
    def remove_edge(self, edge_id: str) -> bool:
        """
        Remove an edge from the map.
        
        Args:
            edge_id: ID of the edge to remove
            
        Returns:
            True if removed, False if not found
        """
        if edge_id not in self.edges:
            return False
        
        edge = self.edges[edge_id]
        
        # Remove edge reference from nodes
        if edge.from_node_id in self.nodes:
            self.nodes[edge.from_node_id].remove_edge(edge_id)
        if edge.to_node_id in self.nodes:
            self.nodes[edge.to_node_id].remove_edge(edge_id)
        
        # Remove edge
        del self.edges[edge_id]
        
        return True
    
    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """
        Get an edge by ID.
        
        Args:
            edge_id: ID of the edge
            
        Returns:
            Edge or None if not found
        """
        return self.edges.get(edge_id)
    
    def get_edges_from_node(self, node_id: str) -> List[Edge]:
        """
        Get all edges connected to a node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of edges connected to the node
        """
        node = self.nodes.get(node_id)
        if not node:
            return []
        
        return [
            self.edges[edge_id]
            for edge_id in node.get_connected_edges()
            if edge_id in self.edges
        ]
    
    def get_neighbors(self, node_id: str) -> List[Node]:
        """
        Get all neighboring nodes connected to a node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of neighboring nodes
        """
        edges = self.get_edges_from_node(node_id)
        neighbors = []
        
        for edge in edges:
            other_node_id = edge.get_other_node(node_id)
            if other_node_id and other_node_id in self.nodes:
                neighbors.append(self.nodes[other_node_id])
        
        return neighbors
    
    def get_all_nodes(self) -> List[Node]:
        """Get all nodes in the map."""
        return list(self.nodes.values())
    
    def get_all_edges(self) -> List[Edge]:
        """Get all edges in the map."""
        return list(self.edges.values())
    
    def clear(self) -> None:
        """Remove all nodes and edges from the map."""
        self.nodes.clear()
        self.edges.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize world map to dictionary."""
        return {
            'id': self.id,
            'nodes': {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            'edges': {edge_id: edge.to_dict() for edge_id, edge in self.edges.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldMap":
        """Deserialize world map from dictionary."""
        world_map = cls(map_id=data.get('id', 'default'))
        
        # Add nodes first
        for node_data in data.get('nodes', {}).values():
            node = Node.from_dict(node_data)
            world_map.nodes[node.id] = node
        
        # Then add edges
        for edge_data in data.get('edges', {}).values():
            edge = Edge.from_dict(edge_data)
            world_map.edges[edge.id] = edge
        
        return world_map
