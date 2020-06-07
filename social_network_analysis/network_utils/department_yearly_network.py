from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

PUBLICATION_TYPE_TO_EXCLUDE = 'conference paper'

class DepartmentYearlyNetwork(Network):
    """Class for creating Department Yearly graph, connecting faculty/departments with years when there were published papers."""

    def __init__(self, authors):
        super().__init__()
        self.authors = authors
        self.create_nodes()
        self.create_edges()

    def create_node_attribute_template(self):
        return {
            'name': '',
            'node_type': ''
        }

    def create_nodes(self):
        """Creates nodes for network - departments/faculties and years in which papers were published."""        
        try:
            self.nodes = []
            self.departments = dict()
            self.faculties = dict()
            self.years = dict()
            for author_name in self.authors:
                if self.authors[author_name].department not in self.departments:
                    # Creating department nodes
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = self.authors[author_name].department
                    attributes['node_type'] = 'department'
                    node = Node(attributes)
                    self.departments[self.authors[author_name].department] = node 
                    self.nodes.append(node)
                if self.authors[author_name].faculty not in self.faculties:
                    # Creating faculty nodes
                    attributes = self.create_node_attribute_template()
                    attributes['name'] = self.authors[author_name].faculty
                    attributes['node_type'] = 'faculty'
                    node = Node(attributes)
                    self.faculties[self.authors[author_name].faculty] = node 
                    self.nodes.append(node)
                # Creating years nodes (year in which paper was published)
                for published_paper in self.authors[author_name].papers:
                    if published_paper[2] not in self.years:
                        attributes = self.create_node_attribute_template()
                        attributes['name'] = published_paper[2]  
                        attributes['node_type'] = 'year_of_publishing'
                        node = Node(attributes)
                        self.years[published_paper[2]] = node
                        self.nodes.append(node)
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creates edges (connecting department/faculty with year if there was author from that organization who published in that year)."""
        try:
            # For excluding double entry for paper 
            # e.g. tho authors from same faculty/department published paper together (only one egde should be added).
            added_papers = set() 
            edges = dict()
            for author_name in self.authors:
                department = self.departments[self.authors[author_name].department]
                faculty = self.faculties[self.authors[author_name].faculty]
                for published_paper in self.authors[author_name].papers:
                    paper_name = published_paper[0] 
                    paper_type = published_paper[1]
                    paper_year = published_paper[2]

                    year = self.years[published_paper[2]]
                    
                    if (paper_name, paper_type, paper_year, faculty.id) not in added_papers:
                        # Adding edge for faculty
                        if (faculty.id, year.id) in edges:
                            edges[(faculty.id, year.id)].weight += 1
                        else:
                            edges[(faculty.id, year.id)] = Edge(source=faculty.id, target=year.id, edge_type=EdgeType.DIRECTED.value) 
                        added_papers.add((paper_name, paper_type, paper_year, faculty.id))
                    if (paper_name, paper_type, paper_year, department.id) not in added_papers:
                        # Adding edge for department
                        if (department.id, year.id) in edges:
                            edges[(department.id, year.id)].weight += 1
                        else:
                            edges[(department.id, year.id)] = Edge(source=department.id, target=year.id, edge_type=EdgeType.DIRECTED.value)
                        added_papers.add((paper_name, paper_type, paper_year, department.id))

            self.edges = []
            for edge_id_pair in edges:
                self.edges.append(edges[edge_id_pair])            
        except Exception as e:
            print(e)
            return None