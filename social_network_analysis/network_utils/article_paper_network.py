from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

class ArticlePaperNetwork(Network):
    """Class for creating Article Paper graph, connecting research papers with articles where they were published."""

    def __init__(self, publications):
        super().__init__()
        self.publications = publications
        self.create_nodes()
        self.create_edges()

    def create_node_attribute_template(self):
        return {
            'name': '',
            'node_type': ''
        }

    def create_nodes(self):
        """Creates nodes for network - articles and research papers (publications)."""        
        try:
            self.nodes = []
            self.articles = dict()
            self.papers = dict()
            for unique_publication_id in self.publications:
                article_name = self.publications[unique_publication_id].get_article_name()
                publication_name = self.publications[unique_publication_id].get_publication_title()
                if article_name not in self.articles:
                    # Adding article node
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = article_name
                    attributes['node_type'] = 'article'
                    node = Node(attributes)
                    self.articles[article_name] = node 
                    self.nodes.append(node)
                if publication_name not in self.papers:
                    # Adding research paper node
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = publication_name
                    attributes['node_type'] = 'publication'
                    node = Node(attributes)
                    self.papers[publication_name] = node 
                    self.nodes.append(node)
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creates edges (connecting publications with articles if they were published in that article)."""
        try:
            self.edges = []
            for unique_publication_id in self.publications:
                article_name = self.publications[unique_publication_id].get_article_name()
                publication_name = self.publications[unique_publication_id].get_publication_title()       
                self.edges.append(Edge(source=self.papers[publication_name].id, target=self.articles[article_name].id, edge_type=EdgeType.DIRECTED.value))
        except Exception as e:
            print(e)
            return None