# Local package imports
from social_network_analysis.network_utils.network_factory import NetworkFabric
from social_network_utils import import_and_clean_dataset, process_dataset, create_and_process_social_networks

# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'

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

    
    