# Local project imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils
from social_network_analysis.graph_utils.coauthor_network import CoAuthorNetwork

# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'



if __name__ == '__main__':

    # Importing dataset
    all_authors = AuthorUtils.read_all_authors('dataset', AUTORS_FILE_NAME)
    all_publication_records = PublicationUtils.read_all_publications('dataset', PUBLICATIONS_FILE_NAME)

    # Processing dataset
    publications = PublicationUtils.map_publications_with_users(all_publication_records, all_authors)
    
    # Creating CoAuthor Network
    CoAuthorNetwork.export_nodes_to_csv(all_authors, path='output', file_name='CoAuthor Network - Nodes')
    CoAuthorNetwork.export_edges_to_csv(publications, path='output', file_name='CoAuthor Network - Edges')

    

