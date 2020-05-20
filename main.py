# Local project imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils


# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'


import csv
import os
from enum import Enum
from itertools import combinations

class Node():
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
                node_writer = csv.writer(node_file, delimiter=',', quoting=csv.QUOTE_NONE)

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
    autoincrement = 1
    header = ['Id',	'Source', 'Target', 'Type',	'Weight']
    
    def __init__(self, source, target, edge_type, weight):
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


if __name__ == '__main__':

    all_authors = AuthorUtils.read_all_authors('dataset', AUTORS_FILE_NAME)
    all_publication_records = PublicationUtils.read_all_publications('dataset', PUBLICATIONS_FILE_NAME)
    
    # print(all_publication_records[62].author)
    # print(PublicationUtils._format_publication_author_name(all_publication_records[62].author))
    
    # print(all_publication_records[0].get_unique_publication_id())
    # print(AuthorUtils.get_all_authors_names(all_authors)[0])

    publications = PublicationUtils.map_publications_with_users(all_publication_records, all_authors)
    # print(len(publications))


    # nodes = []
    # for author_name in all_authors:
    #     author = all_authors[author_name]
    #     attributes = {
    #         'name': author.get_author_full_name().title(), 
    #         'faculty':author.faculty.title(), 
    #         'department':author.department.title()
    #         }
    #     node = Node(attributes, id=author.id)
    #     nodes.append(node)
    # Node.export_to_csv(nodes, 'output', 'CoAuthor Network - Nodes')

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
        # print(coauthors, edges[coauthors])
        coauthors_edges.append(edge)
    Edge.export_to_csv(coauthors_edges, 'output', 'CoAuthor Network - Edges')

    

