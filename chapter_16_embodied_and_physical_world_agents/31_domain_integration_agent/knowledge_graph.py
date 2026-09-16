from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class GraphEdge:
    target_id: str
    relation: str
    weight: float

class HeterogeneousDomainGraph:
    """
    Cross-domain dependency graph G = (V, E) connecting heterogeneous infrastructure entities.
    """
    def __init__(self):
        self.adjacency: Dict[str, List[GraphEdge]] = {}

    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float):
        if source_id not in self.adjacency:
            self.adjacency[source_id] = []
        self.adjacency[source_id].append(GraphEdge(target_id=target_id, relation=relation, weight=weight))

    def propagate_influence(self, source_id: str, initial_strength: float = 1.0, threshold: float = 0.1) -> Dict[str, Tuple[float, List[str]]]:
        """
        Weighted Breadth-First Traversal with multiplicative attenuation.
        Returns: {node_id: (impact_strength, [propagation_path])}
        """
        impacts = {source_id: (initial_strength, [source_id])}
        queue = deque([(source_id, initial_strength, [source_id])])

        while queue:
            node_id, strength, path = queue.popleft()
            for edge in self.adjacency.get(node_id, []):
                propagated = round(strength * edge.weight, 3)
                if propagated < threshold:
                    continue  # Attenuation cutoff

                new_path = path + [edge.target_id]
                if edge.target_id not in impacts or propagated > impacts[edge.target_id][0]:
                    impacts[edge.target_id] = (propagated, new_path)
                    queue.append((edge.target_id, propagated, new_path))
        return impacts