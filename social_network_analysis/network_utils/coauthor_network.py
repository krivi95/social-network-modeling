from itertools import combinations

from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network


class CoAuthorNetwork(Network):
    """Class responsible for parsing inputed data, creating nodes and edges for CoAuthor graph and exporting to csv."""

    def __init__(self, all_authors, publications):
        super().__init__()
        self.all_authors = all_authors
        self.publications = publications
        self.create_nodes()
        self.create_edges()
  
    def create_nodes(self):
        """Creating nodes - Authors with their attributes."""
        try:
            nodes = []
            for author_name in self.all_authors:
                author = self.all_authors[author_name]
                if len(author.collaborators) > 0:
                    # We are exporting only authors from UoB that have collaborationg with each other. 
                    attributes = {
                        'name': author.get_author_full_name().title(), 
                        'faculty':author.faculty.title(), 
                        'department':author.department.title()
                        }
                    node = Node(attributes, id=author.id)
                    nodes.append(node)
            self.nodes = nodes
            return nodes
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creating edges (connecting two authors based on publication collaboration)."""
        try:
            edges = dict()
            for key in self.publications:
                authors = self.publications[key].authors
                if len(authors) > 1:
                    # We create edge only if we have more that 2 authors workig on paper (creating combinations from list of authors)
                    links = combinations(authors, 2)
                    for link in links:
                        # Key in dictionary of edges is tuple of two authors (position matters)
                        # Weight of edge between two authors is increased each time we find new collaboration on publication
                        if (link[0].id, link[1].id) in edges:
                            edges[link[0].id, link[1].id] += 1
                        elif (link[1].id, link[0].id) in edges:
                            edges[link[1].id, link[0].id] += 1
                        else:
                            edges[link[0].id, link[1].id] = 1

            coauthors_edges = [] 
            for coauthors in edges:
                edge = Edge(source=coauthors[0], target=coauthors[1], edge_type=EdgeType.UNDIRRECTED.value, weight=edges[coauthors])
                coauthors_edges.append(edge)
            self.edges = coauthors_edges
            return coauthors_edges
        except Exception as e:
            print(e)
            return None
   