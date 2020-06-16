# Local package imports
from social_network_analysis.data_processing.authors_data_processing import AuthorUtils
from social_network_analysis.data_processing.publications_data_processing import PublicationUtils
from social_network_analysis.network_utils.network_base import NetworkAnalytics
from social_network_analysis.network_utils.network_factory import NetworkFabric

# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'


def process_social_network(network_fabric, social_network_name, output_directory):
    """Creates specified social network, analyses that network and saves results into output directory."""

    # Creating network and exporting nodes and edges to .csv for analysis in 3rd party tools e.g. Gephi.
    network = network_fabric.get_network(social_network_name)    
    network.export_network_to_csv(path=output_directory, file_name=social_network_name)
    
    # Running network analytics, calculating various metrics, using networkx.
    network_analytics = NetworkAnalytics(network, social_network_name)
    network_analytics.run_analysis()
    network_analytics.export_metrics_to_file(path=output_directory)

def create_and_process_social_networks(network_fabric, output_directory):
    """Creates various social network and export network's nodes, edges and metrics for further analysis."""
    # Creating CoAuthor Network and running network analysis
    coauthor_network_name = 'CoAuthor Network'
    process_social_network(network_fabric, coauthor_network_name, output_directory)
    
    # Creating Article Network and running network analysis
    article_network_name = 'Article Network'
    process_social_network(network_fabric, article_network_name, output_directory)
    
    # Creating Department network and running network analysis
    department_network_name = 'Department Network'
    process_social_network(network_fabric, department_network_name, output_directory)
    
    # Creating Department Yearly network and running network analysis
    department_yearly_network_name = 'Department Yearly Network'
    process_social_network(network_fabric, department_yearly_network_name, output_directory)
    
    # Creating Author-Publications network and running network analysis
    author_publication_network_name = 'Author Publications Network'
    process_social_network(network_fabric, author_publication_network_name, output_directory)
    
    # Creating Author-Publications network and running network analysis
    article_paper_network_name = 'Article Paper Network'
    process_social_network(network_fabric, article_paper_network_name, output_directory)
    
    # Creating Publications Yearly network and running network analysis
    publications_yearly_network_name = 'Publications Yearly Network'
    process_social_network(network_fabric, publications_yearly_network_name, output_directory)


def import_and_clean_dataset(path, authors_file_name, publications_file_name):
    """Imports specified dataset from a given path, cleans it and returns cleaned set of authors and publications."""
    all_authors = AuthorUtils.read_all_authors('dataset', authors_file_name)
    all_publication_records = PublicationUtils.read_all_publications('dataset', publications_file_name)
    return (all_authors, all_publication_records)

def process_dataset(all_authors, all_publication_records):
    """Processes dataset, matches published research papers with all of the coauthors associated with that paper.""" 
    publications = PublicationUtils.map_publications_with_users(all_publication_records, all_authors)
    AuthorUtils.update_author_collaborators_and_publications_info(publications)
    return publications

if __name__ == '__main__':

    # Importing dataset
    cleaned_dataset = import_and_clean_dataset(path='dataset', authors_file_name=AUTORS_FILE_NAME, publications_file_name=PUBLICATIONS_FILE_NAME)
    all_authors = cleaned_dataset[0]
    all_publication_records = cleaned_dataset[1]

    # Processing dataset
    publications = process_dataset(all_authors, all_publication_records)
    
    # Creating social networks, running analytics and exporting network's nodes, edges and metrics for further analysis
    network_fabric = NetworkFabric(all_authors, publications)
    create_and_process_social_networks(network_fabric, output_directory='output')

    
    