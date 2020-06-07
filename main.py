# Local package imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils
from social_network_analysis.network_utils.coauthor_network import CoAuthorNetwork
from social_network_analysis.network_utils.article_network import ArticleNetwork
from social_network_analysis.network_utils.department_network import DepartmentNetwork
from social_network_analysis.network_utils.network_base import NetworkAnalytics
from social_network_analysis.network_utils.department_yearly_network import  DepartmentYearlyNetwork

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

    # Creating CoAuthor Network and running network analysis
    coauthor_network = CoAuthorNetwork(all_authors, publications)
    coauthor_network.export_network_to_csv(path='output', file_name='CoAuthor Network')
    coauthor_network_analytics = NetworkAnalytics(coauthor_network, 'CoAuthor Network')
    coauthor_network_analytics.run_analysis()
    coauthor_network_analytics.export_metrics_to_file(path='output')

    # Creating Article Network and running network analysis
    article_network = ArticleNetwork(publications)
    article_network.export_network_to_csv(path='output', file_name='Article Network')    
    article_network_analytics = NetworkAnalytics(article_network, 'Article Network')
    article_network_analytics.run_analysis()
    article_network_analytics.export_metrics_to_file(path='output')
    
    # Creating Department network and running network analysis
    department_network = DepartmentNetwork(all_authors)
    department_network.export_network_to_csv(path='output', file_name='Department Network')    
    department_network_analytics = NetworkAnalytics(department_network, 'Department Network')
    department_network_analytics.run_analysis()
    department_network_analytics.export_metrics_to_file(path='output')

    # Creating Department Yearly network and running network analysis
    department_yearly_network = DepartmentYearlyNetwork(all_authors)
    department_yearly_network.export_network_to_csv(path='output', file_name='Department Yearly Network')    
    department_yearly_network_analytics = NetworkAnalytics(department_yearly_network, 'Department Yearly Network')
    department_yearly_network_analytics.run_analysis()
    department_yearly_network_analytics.export_metrics_to_file(path='output')
     

