from .coauthor_network import CoAuthorNetwork
from .article_network import ArticleNetwork
from .department_network import DepartmentNetwork
from .department_yearly_network import  DepartmentYearlyNetwork
from .author_publications_network import AuthorPublicationsNetwork
from .article_paper_network import ArticlePaperNetwork
from .publications_yearly_network import PublicationsYearlyNetwork

class NetworkFabric:
    """Produces various social networks for analysis."""
    
    def __init__(self, authors, publications):
        self.authors = authors
        self.publications = publications

    def get_network(self, network_type):
        """Creates new network based on provided network type."""
        if network_type == 'CoAuthor Network':
            return CoAuthorNetwork(self.authors, self.publications)
        elif network_type == 'Article Network':
            return ArticleNetwork(self.publications)
        elif network_type == 'Department Network':
            return DepartmentNetwork(self.authors)
        elif network_type == 'Department Yearly Network':
            return DepartmentYearlyNetwork(self.authors)
        elif network_type == 'Author Publications Network':
            return AuthorPublicationsNetwork(self.authors)
        elif network_type == 'Article Paper Network':
            return ArticlePaperNetwork(self.publications)
        elif network_type == 'Publications Yearly Network':
            return PublicationsYearlyNetwork(self.publications)