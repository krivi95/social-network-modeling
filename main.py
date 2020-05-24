# Local package imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils
from social_network_analysis.graph_utils.coauthor_network import CoAuthorNetwork
from social_network_analysis.graph_utils.article_network import ArticleNetwork

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
    AuthorUtils.updade_author_collaborators_and_publications_info(publications)

    # Creating CoAuthor Network
    CoAuthorNetwork.export_edges_to_csv(publications, path='output', file_name='CoAuthor Network - Edges')
    CoAuthorNetwork.export_nodes_to_csv(all_authors, path='output', file_name='CoAuthor Network - Nodes')

    # Creating Article Network
    articles = ArticleNetwork.create_article_nodes(publications)
    ArticleNetwork.export_nodes_to_csv([articles[article_name] for article_name in articles], path='output', file_name='Article Network - Nodes')
    ArticleNetwork.export_edges_to_csv(publications, articles, path='output', file_name='Article Network - Edges')
   
    
    
        
    

