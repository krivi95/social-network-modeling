import csv
import os
from enum import Enum
from abc import ABC, abstractmethod

class Node():
    """
    Class representing node in a graph. Node can have many attributes (storred in a dictionary).
    """
    autoincrement = 1

    def __init__(self, attributes, id = None):
        self.attributes = attributes
        if id:
            self.id = id
        else:    
            self.id = Node.autoincrement
            Node.autoincrement += 1

    @staticmethod
    def export_to_csv(nodes, path, file_name):
        if nodes is None:
            return None
        else:
            full_file_path = os.path.join(path, file_name) + '.csv'
            with open(full_file_path, mode='w', newline='\n') as node_file:
                node_writer = csv.writer(node_file, delimiter=',', quotechar = '"')

                # Writing header
                # First column is id, followed by attributes from Node's attribute dictionary (keys)
                node_writer.writerow(['Id'] + list(nodes[0].attributes))
                for node in nodes:
                    node_writer.writerow([node.id] + [node.attributes[attribute] for attribute in node.attributes.keys()])
            return full_file_path


class EdgeType(Enum):
    UNDIRRECTED = 'undirected'
    DIRECTED = 'directed'


class Edge():
    """
    Class representing link between two nodes in a graph.
    """
    autoincrement = 1
    header = ['Id',	'Source', 'Target', 'Type',	'Weight']
    
    def __init__(self, source, target, edge_type, weight=1):
        self.id = Node.autoincrement
        Node.autoincrement += 1
        self.source = source
        self.target = target
        self.type = edge_type
        self.weight = weight

    @staticmethod
    def export_to_csv(nodes, path, file_name):
        if nodes is None:
            return None
        else:
            full_file_path = os.path.join(path, file_name) + '.csv'
            with open(full_file_path, mode='w', newline='\n') as node_file:
                edge_writer = csv.writer(node_file, delimiter=',', quoting=csv.QUOTE_NONE)

                # Writing header
                edge_writer.writerow(nodes[0].header)
                for node in nodes:
                    edge_writer.writerow([node.id, node.source, node.target, node.type, node.weight])
            return full_file_path



class Network(ABC):
    """Class representing social network that consists of nodes and edges connecting those nodes."""
    
    @abstractmethod
    def __init__(self):
        self.nodes = None
        self.edges = None

    @abstractmethod
    def create_nodes(self):
        pass

    @abstractmethod
    def create_edges(self):
        pass

    def export_network_to_csv(self, path, file_name):
        """Exports notwork's nodes and grapsh to separate csv files."""
        self._export_nodes_to_csv(path, file_name + ' - Nodes')
        self._export_edges_to_csv(path, file_name + ' - Edges')

    def _export_nodes_to_csv(self, path, file_name):
        try:
            Node.export_to_csv(self.nodes, path, file_name)
            return True
        except Exception as e:
            print(e)
            return False

    def _export_edges_to_csv(self, path, file_name):
        try:
            Edge.export_to_csv(self.edges, path, file_name)
            return True
        except Exception as e:
            print(e)
            return False