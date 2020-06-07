import csv
import os
import io
import networkx as nx
from enum import Enum
from abc import ABC, abstractmethod
from collections import OrderedDict 

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
                    try:
                        node_writer.writerow([node.id] + [node.attributes[attribute] for attribute in node.attributes.keys()])
                    except Exception as e:
                        node_writer.writerow([node.id] + [node.attributes[attribute].encode('utf-8') for attribute in node.attributes.keys()])
                        print('\t Character coding error:' + str(e))
                        print('\t Character coding error:' + str(node.attributes))
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
        print(f'Exporting network {file_name}(nodes and edges) to csv...')
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


class NetworkAnalytics():
    """Class that calculates various network's metrics using networx module."""

    def __init__(self, network, network_name=""):
        self.network_name = network_name
        self.metrics = OrderedDict()
        self.G = nx.Graph(name=network_name)
        for node in network.nodes:
            self.G.add_node(node.id, attributes=node.attributes)
        for edge in network.edges:
            self.G.add_edge(edge.source, edge.target, weight=edge.weight)

    def export_metrics_to_file(self, path):
        """Exports Network Analysis calculated metrics and data to file."""
        print(f'Exporting analysis for {self.network_name}...')
        full_file_path = os.path.join(path, self.network_name + ' - Analytics') + '.txt'
        with io.open(full_file_path, 'w', encoding="utf8") as f:
            f.write(self.__repr__())
        return full_file_path

    def run_analysis(self):
        """Calculates various network's metrics and saves it into metrics dicitonary. Returns dictionary with calculated metrics."""

        print(f'Running network analysis for {self.network_name}...')

        self.metrics['Info'] = nx.info(self.G)

        self.metrics["Network density"] = nx.density(self.G)
        self.metrics["Network components"] = len(list(nx.connected_components(self.G)))

        # Calculating centrality metrics
        degree_centrality_dict = nx.degree_centrality(self.G) 
        closeness_centrality_dict = nx.closeness_centrality(self.G)
        betweenness_centrality_dict = nx.betweenness_centrality(self.G)
        eigenvector_centrality_dict = nx.eigenvector_centrality(self.G)

        # Assigning centralities to nodes
        nx.set_node_attributes(self.G, degree_centrality_dict, 'degree_centrality')
        nx.set_node_attributes(self.G, closeness_centrality_dict, 'closeness_centrality')
        nx.set_node_attributes(self.G, betweenness_centrality_dict, 'betweenness_centrality')
        nx.set_node_attributes(self.G, eigenvector_centrality_dict, 'eigenvector_centrality')

        # Calculating average centralities for entire network
        number_of_nodes = len(self.G.nodes)
        self.metrics['Average Degree Centrality'] = sum(degree_centrality_dict.values()) / number_of_nodes
        self.metrics['Average Closeness Centrality'] = sum(closeness_centrality_dict.values()) / number_of_nodes
        self.metrics['Average Betweenness Centrality'] = sum(betweenness_centrality_dict.values()) / number_of_nodes
        self.metrics['Average Eigenvector Centrality'] = sum(eigenvector_centrality_dict.values()) / number_of_nodes
        
        return self.metrics

    def __repr__(self):
        """String data format of Network Analysis. Contains general network info, calculated metrics and list of nodes and their attributes."""
        if len(self.metrics) == 0:
            return self.__class__
        analytics = ''
        for metric in self.metrics:
            if metric == 'Info':
                # Network general info
                analytics += '--------- NETWORK GENERAL DATA -----------\n'
                analytics += f'{self.metrics[metric]} \n'
                analytics += '--------- NETWORK ANALYSIS DATA -----------\n'
            else:
                # Network's calculated metrics
                analytics += f'{metric}: {self.metrics[metric]} \n'  

        # Printing each separate node and its attributes and metrics
        analytics += '--------- NETWORK NODES -----------\n'
        analytics += 'Node Id, Column dicitonary\n'
        for node in self.G.nodes.data():
            analytics += str(node[0]) 
            analytics += ','
            analytics += str(node[1]) 
            analytics += '\n'
        return analytics