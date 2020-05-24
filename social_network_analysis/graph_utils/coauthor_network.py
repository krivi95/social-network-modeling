from itertools import combinations

from ..data_processing.authors_data_processing import Author
from .graph_base import Node, Edge, EdgeType


class CoAuthorNetwork():
    """Class responsible for parsing inputed data, creating nodes and edges for CoAuthor graph and exporting to csv."""
  
    @staticmethod
    def export_nodes_to_csv(all_authors, path, file_name):
        """Exporting nodes (Authors and their attributes) to csv."""
        try:
            nodes = []
            for author_name in all_authors:
                author = all_authors[author_name]
                if len(author.collaborators) > 0:
                    # We are exporting only authors from UoB that have collaborationg with each other. 
                    attributes = {
                        'name': author.get_author_full_name().title(), 
                        'faculty':author.faculty.title(), 
                        'department':author.department.title()
                        }
                    node = Node(attributes, id=author.id)
                    nodes.append(node)
            Node.export_to_csv(nodes, path, file_name)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def export_edges_to_csv(publications, path, file_name):
        """Exporting edges (connecting two authors based on publication collaboration) to csv."""
        try:
            edges = dict()
            for key in publications:
                authors = publications[key].authors
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
            Edge.export_to_csv(coauthors_edges, path, file_name)
            return True
        except Exception as e:
            print(e)
            return False
   