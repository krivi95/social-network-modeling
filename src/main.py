# Local project imports
from data_processing.authors_data_processing import AuthorUtils
from data_processing.publications_data_processing import PublicationUtils


# Input file names
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'

if __name__ == '__main__':

    all_authors = AuthorUtils.read_all_authors('./dataset', AUTORS_FILE_NAME)
    all_publication_records = PublicationUtils.read_all_publications('./dataset', PUBLICATIONS_FILE_NAME)
    
    # print(all_publication_records[62].author)
    # print(PublicationUtils._format_publication_author_name(all_publication_records[62].author))
    
    # print(all_publication_records[0].get_unique_publication_id())
    # print(AuthorUtils.get_all_authors_names(all_authors)[0])

    publications = PublicationUtils.map_publications_with_users(all_publication_records, all_authors)
    print(len(publications))
