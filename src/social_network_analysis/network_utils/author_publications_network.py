from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

class AuthorPublicationsNetwork(Network):
    """Class for creating network conncting Author with their Publications."""

    def __init__(self, authors):
        super().__init__()
        self.authors = authors
        self.create_nodes()
        self.create_edges()

    def create_node_attribute_template(self):
        return {
            'author_name': '',
            'paper_name': '',
            'node_type': ''
        }

    def create_nodes(self):
        """Creates nodes for network - authors and papers that they published."""        
        try:
            self.nodes = []
            self.papers = dict()
            self.author_nodes = dict()
            for author_name in self.authors:
                # Creating Author nodes
                author = self.authors[author_name]
                attributes = self.create_node_attribute_template()
                attributes['author_name'] = self.authors[author_name].get_author_full_name()
                attributes['node_type'] = 'author'
                node = Node(attributes)
                self.author_nodes[self.authors[author_name].get_author_full_name()] = node
                self.nodes.append(node)
                 # Creating publication paper nodes
                for published_paper in self.authors[author_name].papers:
                    if published_paper not in self.papers:
                        attributes = self.create_node_attribute_template()
                        attributes['paper_name'] = published_paper[0]  
                        attributes['node_type'] = published_paper[1]    # publication type
                        node = Node(attributes)
                        self.papers[published_paper] = node
                        self.nodes.append(node)
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creates edges (connecting authors and papers if author published that paper)."""
        try:
            self.edges = []         
            for author_name in self.authors:
                author = self.authors[author_name]
                for published_paper in self.authors[author_name].papers:
                    paper = self.papers[published_paper] 
                    author_node = self.author_nodes[self.authors[author_name].get_author_full_name()]
                    self.edges.append(Edge(source=author_node.id, target=paper.id, edge_type=EdgeType.DIRECTED.value))

        except Exception as e:
            print(e)
            return None