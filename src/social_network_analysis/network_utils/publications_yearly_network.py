from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

class PublicationsYearlyNetwork(Network):
    """Class for creating Publications Yearly graph, connecting research papers with years when they were published."""

    def __init__(self, publications):
        super().__init__()
        self.publications = publications
        self.create_nodes()
        self.create_edges()

    def create_node_attribute_template(self):
        return {
            'name': '',
            'node_type': '',
            'department': set(),
            'faculty': set()
        }

    def create_nodes(self):
        """Creates nodes for network - research papers (publications) and years."""        
        try:
            self.nodes = []
            self.years = dict()
            self.papers = dict()
            for unique_publication_id in self.publications:
                publication_name = self.publications[unique_publication_id].get_publication_title()
                year_of_publishing = self.publications[unique_publication_id].get_publication_year()
                if year_of_publishing not in self.years:
                    # Adding year node
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = year_of_publishing
                    attributes['node_type'] = 'year'
                    node = Node(attributes)
                    self.years[year_of_publishing] = node 
                    self.nodes.append(node)
                if publication_name not in self.papers:
                    # Adding research paper node (for each faculty and department where )
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = publication_name
                    attributes['node_type'] = 'publication'
                    for author in self.publications[unique_publication_id].authors:
                        attributes['faculty'].add(author.faculty)
                        attributes['department'].add(author.department)
                    # Convering set of faculties and departments into string for analysis in Gephi
                    attributes['faculty'] = str(attributes['faculty'])
                    attributes['department'] = str(attributes['department'])                    
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
                publication_name = self.publications[unique_publication_id].get_publication_title()
                year_of_publishing = self.publications[unique_publication_id].get_publication_year()    
                self.edges.append(Edge(source=self.papers[publication_name].id, target=self.years[year_of_publishing].id, edge_type=EdgeType.DIRECTED.value))
        except Exception as e:
            print(e)
            return None