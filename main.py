# Local package imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils
from social_network_analysis.network_utils.coauthor_network import CoAuthorNetwork
from social_network_analysis.network_utils.article_network import ArticleNetwork
from social_network_analysis.network_utils.department_network import DepartmentNetwork

# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'

if __name__ == '__main__':

    # Importing dataset
    all_authors = AuthorUtils.read_all_authors('dataset', AUTORS_FILE_NAME)
    all_publication_records = PublicationUtils.read_all_publications('dataset', PUBLICATIONS_FILE_NAME)

    # Processing dataset
    publications = PublicationUtils.map_publications_with_users(all_publication_records, all_authors)
    
    # Updating author collaboration info from publications
    AuthorUtils.update_author_collaborators_and_publications_info(publications)

    # # Creating CoAuthor Network
    coauthor_network = CoAuthorNetwork(all_authors, publications)
    coauthor_network.export_network_to_csv(path='output', file_name='CoAuthor Network')

    # # Creating Article Network
    article_network = ArticleNetwork(publications)
    article_network.export_network_to_csv(path='output', file_name='Article Network')

    # Creating Department network
    department_network = DepartmentNetwork(all_authors)
    department_network.export_network_to_csv(path='output', file_name='Department Network')
    
        

