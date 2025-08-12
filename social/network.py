import random
import numpy as np
import networkx as nx
import logging
import time
from typing import List, Dict, Optional
from social.agent import SocialAgent
from social.config import SimulationConfig

logger = logging.getLogger(__name__)


class NetworkGenerator:
    """
    Generate social networks for innovation diffusion simulation using NetworkX
    
    Based on:
    - Watts & Strogatz (1998) - Small-world networks
    - Barabási & Albert (1999) - Scale-free networks  
    - Erdős-Rényi (1960) - Random networks
    """
    
    @staticmethod
    def create_network(agents: List[SocialAgent], config: SimulationConfig) -> Dict:
        """
        Create social network based on configuration using NetworkX
        
        Args:
            agents: List of social agents
            config: Simulation configuration
            
        Returns:
            Dict with network statistics
        """
        if not agents:
            raise ValueError("Cannot create network: no agents provided")
            
        num_agents = len(agents)
        if num_agents < 2:
            raise ValueError(f"Cannot create network: need at least 2 agents, got {num_agents}")
            
        network_start = time.time()
        
        logger.info(f"Creating {config.network_type} network for {num_agents} agents using NetworkX")
        
        try:
            # Clear existing connections
            for agent in agents:
                agent.connections = []

            # Generate NetworkX graph based on type
            nx_graph = NetworkGenerator._create_networkx_graph(num_agents, config)

            # Map NetworkX graph to agent connections with proper shuffling support
            NetworkGenerator._map_networkx_to_agents(nx_graph, agents, config.network_shuffle, config.network_seed)
            
            # Calculate network statistics using NetworkX
            stats = NetworkGenerator._calculate_networkx_statistics(nx_graph)
            
            # Include networkx graph data for visualization consistency
            stats["networkx_graph"] = nx_graph
            
            network_time = time.time() - network_start
            logger.info(f"Network created in {network_time:.3f}s: "
                       f"{stats['total_edges']} edges, "
                       f"avg degree: {stats['avg_degree']:.1f}")
            
            stats["creation_time"] = network_time
            stats["network_type"] = config.network_type
            return stats
            
        except Exception as e:
            logger.error(f"Error creating network: {e}")
            raise e
    
    @staticmethod
    def _create_networkx_graph(num_agents: int, config: SimulationConfig) -> nx.Graph:
        """
        Create NetworkX graph based on configuration
        
        Args:
            num_agents: Number of nodes in the graph
            config: Simulation configuration
            
        Returns:
            NetworkX graph object
        """
        params = config.network_params
        seed = config.network_seed
        
        if config.network_type == "small_world":
            return NetworkGenerator._create_small_world_nx(num_agents, params, seed)
        elif config.network_type == "scale_free":
            return NetworkGenerator._create_scale_free_nx(num_agents, params, seed)
        elif config.network_type == "random":
            return NetworkGenerator._create_random_nx(num_agents, params, seed)
        else:
            logger.warning(f"Unknown network type {config.network_type}, using small_world")
            return NetworkGenerator._create_small_world_nx(num_agents, params, seed)
    
    @staticmethod
    def _create_small_world_nx(num_agents: int, params: Dict, seed: Optional[int]) -> nx.Graph:
        """
        Create small-world network using NetworkX Watts-Strogatz model
        
        Args:
            num_agents: Number of nodes
            params: Network parameters (k, rewiring_prob)
            
        Returns:
            NetworkX graph
        """
        k = params.get("k", 4)
        rewiring_prob = params.get("rewiring_prob", 0.3)
        
        # Ensure k is even and reasonable
        k = max(2, min(k, num_agents - 1))
        if k % 2 != 0:
            logger.debug("Adjusting k to be even for small-world network")
            k = k + 1 if k < num_agents - 1 else k - 1
        
        logger.debug(f"Creating small-world network: n={num_agents}, k={k}, p={rewiring_prob}")
        
        # Use NetworkX Watts-Strogatz model
        graph = nx.watts_strogatz_graph(num_agents, k, rewiring_prob, seed=seed)
                    
        return graph
    
    @staticmethod
    def _create_scale_free_nx(num_agents: int, params: Dict, seed: Optional[int]) -> nx.Graph:
        """
        Create scale-free network using NetworkX Barabási-Albert model
        
        Args:
            num_agents: Number of nodes
            params: Network parameters (m)
            
        Returns:
            NetworkX graph
        """
        m = params.get("m", 2)
        
        # Ensure m is reasonable
        m = max(1, min(m, num_agents - 1))

        if m != params.get("m", 2):
            logger.debug("Adjusting m for scale-free network")
        
        logger.debug(f"Creating scale-free network: n={num_agents}, m={m}")
        
        # Use NetworkX Barabási-Albert model
        graph = nx.barabasi_albert_graph(num_agents, m, seed=seed)
        return graph
    
    @staticmethod
    def _create_random_nx(num_agents: int, params: Dict, seed: Optional[int]) -> nx.Graph:
        """
        Create random network using NetworkX Erdős-Rényi model
        
        Args:
            num_agents: Number of nodes
            params: Network parameters (p or edge_prob)
            
        Returns:
            NetworkX graph
        """
        p = params.get("p", params.get("edge_prob", 0.1))
        
        logger.debug(f"Creating random network: n={num_agents}, p={p}")
        
        # Use NetworkX Erdős-Rényi model
        graph = nx.erdos_renyi_graph(num_agents, p, seed=seed)
        return graph
    
    @staticmethod
    def _map_networkx_to_agents(nx_graph: nx.Graph, agents: List[SocialAgent], 
                                shuffle: bool = False, seed: Optional[int] = None):
        """
        Map NetworkX graph edges to agent connections with improved shuffling
        
        Args:
            nx_graph: NetworkX graph
            agents: List of agents
            shuffle: Whether to apply random shuffling to connections
            seed: Random seed for shuffling
        """
        # Clear existing connections
        for agent in agents:
            agent.connections = []
        
        # Create mapping for shuffling if enabled
        if shuffle:
            # Create a randomized mapping from graph indices to agent indices
            agent_indices = list(range(len(agents)))
            local_random = random.Random(seed)
            local_random.shuffle(agent_indices)
            # Map from graph node index to shuffled agent index
            index_mapping = {i: agent_indices[i] for i in range(len(agents))}
        else:
            # Direct mapping
            index_mapping = {i: i for i in range(len(agents))}
        
        # Map edges to agent connections using the index mapping
        for edge in nx_graph.edges():
            graph_idx1, graph_idx2 = edge
            
            # Get actual agent indices using mapping
            agent_idx1 = index_mapping.get(graph_idx1)
            agent_idx2 = index_mapping.get(graph_idx2)
            
            if (agent_idx1 is not None and agent_idx2 is not None and 
                agent_idx1 < len(agents) and agent_idx2 < len(agents)):
                
                agent1 = agents[agent_idx1]
                agent2 = agents[agent_idx2]

                nx_graph.nodes[graph_idx1]['agent_id'] = agent1.agent_id
                nx_graph.nodes[graph_idx2]['agent_id'] = agent2.agent_id
                nx_graph.nodes[graph_idx1]['adopter_category'] = agent1.adopter_category
                nx_graph.nodes[graph_idx2]['adopter_category'] = agent2.adopter_category

                # Add bidirectional connections
                if agent2 not in agent1.connections:
                    agent1.add_connection(agent2)
                if agent1 not in agent2.connections:
                    agent2.add_connection(agent1)
    
    @staticmethod
    def _agents_to_networkx(agents: List[SocialAgent]) -> nx.Graph:
        """
        Convert agent connections to NetworkX graph
        
        Args:
            agents: List of agents
            
        Returns:
            NetworkX graph representation
        """
        graph = nx.Graph()
        
        # Add nodes
        for i, agent in enumerate(agents):
            graph.add_node(i, agent_id=agent.agent_id)
        
        # Add edges
        for i, agent in enumerate(agents):
            for connection in agent.connections:
                j = agents.index(connection)
                if not graph.has_edge(i, j):
                    graph.add_edge(i, j)
        
        return graph
    
    @staticmethod
    def validate_network(agents: List[SocialAgent]) -> Dict:
        """
        Validate network structure and agent connections
        
        Args:
            agents: List of agents
            
        Returns:
            Dictionary with validation results
        """
        try:
            if not agents:
                return {
                    "valid": False,
                    "issues": ["No agents provided"],
                    "total_agents": 0,
                    "total_connections": 0
                }
            
            issues = []
            total_connections = 0
            symmetric_issues = 0
            
            # Check for basic issues
            for i, agent in enumerate(agents):
                if not hasattr(agent, 'connections'):
                    issues.append(f"Agent {i} missing connections attribute")
                    continue
                
                if not isinstance(agent.connections, list):
                    issues.append(f"Agent {i} connections is not a list")
                    continue
                
                total_connections += len(agent.connections)
                
                # Check for symmetric connections
                for connection in agent.connections:
                    if connection not in agents:
                        issues.append(f"Agent {i} connected to non-existent agent")
                        continue
                    
                    if agent not in connection.connections:
                        symmetric_issues += 1
            
            # Check network connectivity using NetworkX
            if len(agents) > 1:
                try:
                    nx_graph = NetworkGenerator._agents_to_networkx(agents)
                    is_connected = nx.is_connected(nx_graph)
                    num_components = nx.number_connected_components(nx_graph)
                    
                    if not is_connected and num_components > 1:
                        issues.append(f"Network has {num_components} disconnected components")
                        
                except Exception as e:
                    issues.append(f"NetworkX validation failed: {str(e)}")
            
            # Report symmetric connection issues
            if symmetric_issues > 0:
                issues.append(f"{symmetric_issues} asymmetric connections found")
            
            validation_result = {
                "valid": len(issues) == 0,
                "issues": issues,
                "total_agents": len(agents),
                "total_connections": total_connections // 2,  # Each connection counted twice
                "symmetric_issues": symmetric_issues,
                "warnings": []
            }
            
            # Add warnings for potential issues
            if total_connections == 0:
                validation_result["warnings"].append("No connections found - isolated network")
            
            avg_connections = total_connections / len(agents) if agents else 0
            if avg_connections < 2:
                validation_result["warnings"].append(f"Low average connectivity: {avg_connections:.1f}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Network validation error: {e}")
            return {
                "valid": False,
                "issues": [f"Validation error: {str(e)}"],
                "total_agents": len(agents) if agents else 0,
                "total_connections": 0
            }
    
    @staticmethod
    def _calculate_networkx_statistics(nx_graph: nx.Graph) -> Dict:
        """
        Calculate comprehensive network statistics using NetworkX
        
        Args:
            nx_graph: NetworkX graph

        Returns:
            Dictionary with network statistics
        """
        try:
            num_nodes = nx_graph.number_of_nodes()
            num_edges = nx_graph.number_of_edges()
            
            if num_nodes == 0:
                return {
                    "total_edges": 0,
                    "avg_degree": 0,
                    "density": 0,
                    "avg_clustering": 0,
                    "avg_shortest_path": float('inf'),
                    "diameter": 0,
                    "is_connected": False,
                    "num_components": 0
                }
            
            # Basic metrics
            density = nx.density(nx_graph)
            avg_degree = 2 * num_edges / num_nodes if num_nodes > 0 else 0
            
            # Clustering coefficient
            avg_clustering = nx.average_clustering(nx_graph)
            
            # Connectivity metrics
            is_connected = nx.is_connected(nx_graph)
            num_components = nx.number_connected_components(nx_graph)
            
            # Path length metrics (only for connected graphs)
            if is_connected and num_nodes > 1:
                try:
                    avg_shortest_path = nx.average_shortest_path_length(nx_graph)
                    diameter = nx.diameter(nx_graph)
                except:
                    avg_shortest_path = float('inf')
                    diameter = 0
            else:
                avg_shortest_path = float('inf')
                diameter = 0
            
            # Degree statistics
            degrees = dict(nx_graph.degree())
            degree_values = list(degrees.values())
            
            return {
                "total_edges": num_edges,
                "avg_degree": avg_degree,
                "density": density,
                "avg_clustering": avg_clustering,
                "avg_shortest_path": avg_shortest_path,
                "diameter": diameter,
                "is_connected": is_connected,
                "num_components": num_components,
                "min_degree": min(degree_values) if degree_values else 0,
                "max_degree": max(degree_values) if degree_values else 0,
                "std_degree": np.std(degree_values) if degree_values else 0,
                "isolated_nodes": sum(1 for d in degree_values if d == 0)
            }
            
        except Exception as e:
            logger.error(f"Error calculating network statistics: {e}")
            raise e
