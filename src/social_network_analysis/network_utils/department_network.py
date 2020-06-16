from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

PUBLICATION_TYPE_TO_EXCLUDE = 'conference paper'

class DepartmentNetwork(Network):
    """Class for creating Department graph, connecting faculty departments with published papers."""

    def __init__(self, authors):
        super().__init__()
        self.authors = authors
        self.create_nodes()
        self.create_edges()

    def create_node_attribute_template(self):
        return {
            'department': '',
            'faculty': '',
            'publication': '',
            'publication_type': '',
            'node_type': ''
        }

    def create_nodes(self):
        """Creates nodes for network - departments and published papers by professors from taht department."""        
        try:
            self.nodes = []
            self.departments = dict()
            self.papers = dict()
            for author_name in self.authors:
                if self.authors[author_name].department not in self.departments:
                    # Creating department nodes
                    attributes = self.create_node_attribute_template()
                    attributes['department'] = self.authors[author_name].department
                    attributes['faculty'] = self.authors[author_name].faculty
                    attributes['node_type'] = 'department'
                    node = Node(attributes)
                    self.departments[self.authors[author_name].department] = node 
                    self.nodes.append(node)
                # Creating published papers nodes
                for published_paper in self.authors[author_name].papers:
                    attributes = self.create_node_attribute_template()
                    attributes['publication'] = published_paper[0]  
                    attributes['publication_type'] = published_paper[1]  
                    attributes['node_type'] = 'paper'
                    node = Node(attributes)
                    self.papers[published_paper[0]] = node

            for paper_name in self.papers:
                self.nodes.append(self.papers[paper_name])
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creates edges (connecting two articles if at least one author exists who published papers in both articles)."""
        try:
            self.edges = []
            for author_name in self.authors:
                department = self.departments[self.authors[author_name].department]
                for published_paper in self.authors[author_name].papers:
                    paper = self.papers[published_paper[0]]
                    self.edges.append(Edge(source=department.id, target=paper.id, edge_type=EdgeType.DIRECTED.value))
        except Exception as e:
            print(e)
            return None