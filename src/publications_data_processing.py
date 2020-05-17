import pandas as pd
import os
import math
from collections import namedtuple 

# We only process following publications
VALID_PUBLICATION_TYPES = [
    'Article', 
    'Article in Press', 
    'Book Chapter',
    'Conference Paper', 
    'Review', 
]

# FILE COLUMN NAMES
PUBLICATIONS_PAPER_TITLE = 'Naslov'
PUBLICATIONS_AUTHOR = 'UB zaposleni'
PUBLICATIONS_AUTHORS = 'Autori'
PUBLICATIONS_YEAR = 'Godina'
PUBLICATIONS_TYPE = 'Tip rada'
PUBLICATIONS_ARTICLE_NAME = 'Ime dokumenta'

# PUBLICATIONS_CITATIONS = 'Broj citiranja'
# PUBLICATIONS_CITE_FACTOR_2017 = 'Cite factor 2017'
# PUBLICATIONS_SJIR = 'SJIR'
# PUBLICATIONS_SNIP = 'SNIP'

# Publication = namedtuple('Publication', ['title', 'authors', 'year', 'type', 'article'])

class Publication:
    """
    Class containing necessary information about publications and co-authors
    Provides some additional methods for cleaning up dataset.
    """ 
    def __init__(self, author, publication_title, publication_authors, publication_year, publication_type, article_name):
        self.author = author
        self.publication_title = publication_title
        self.publication_authors = publication_authors
        self.publication_year = publication_year 
        self.publication_type = publication_type
        self.article_name = article_name 
    
    def clean_data(self):
        self._validate_article_name()
        self._validate_author_name()
        self._change_all_names_to_lower_case()
        self._replace_latin_characters()

    def _validate_article_name(self):
        if isinstance(self.article_name, float) and math.isnan(self.article_name):
            self.article_name = None 

    def _validate_author_name(self):
            self.author = self.author.replace('N/A', '')

    def _change_all_names_to_lower_case(self):
        self.author = self.author.lower()
        self.publication_title = self.publication_title.lower()
        self.publication_authors = self.publication_authors.lower()
        self.publication_type = self.publication_type.lower()
        if self.article_name: 
            self.article_name = self.article_name.lower()

    def _replace_latin_characters(self):
        def replace_characters(name):
            name = name.replace('ć', 'c')
            name = name.replace('č', 'c')
            name = name.replace('š', 's')
            name = name.replace('đ', 'dj')
            name = name.replace('ž', 'z')
            return name
        self.author = replace_characters(self.author.lower())
        self.publication_title = replace_characters(self.publication_title)
        self.publication_authors = replace_characters(self.publication_authors)
        self.publication_type = replace_characters(self.publication_type)
        if self.article_name:
            self.article_name = replace_characters(self.article_name)

    def __repr__(self):
        return f'Publication: {self.publication_title}, {self.publication_year}, {self.article_name} \
                \n             author = {self.author} \
                \n             co-authors = {self.publication_authors}'

class PublicationUtils:
    """
    Class containint various utility methods for dealing with publication and various information about scientific publications,  
    """

    @staticmethod
    def read_all_publications(path, file_name):
        """
        Reads publication and keeps orginal raw format from dataset. 
        Keeps only one record per publication (in dataset if there are e.g. 3 authors for one publication there will be 3 rows for same publication, 
        for each author separately). One publication is identified by: list of authors and title of paper. Additional info is also stored for further
        analysis.
        Returns unique set of publications
        """
        publications = []
        data = pd.read_excel(os.path.join(path, file_name))
        for column, row in data.iterrows():
            if row[PUBLICATIONS_TYPE] not in VALID_PUBLICATION_TYPES:
                continue
            publication = Publication(author=row[PUBLICATIONS_AUTHOR],
                                      publication_title=row[PUBLICATIONS_PAPER_TITLE],
                                      publication_authors=row[PUBLICATIONS_AUTHORS],
                                      publication_year=row[PUBLICATIONS_YEAR],
                                      publication_type=row[PUBLICATIONS_TYPE],
                                      article_name=row[PUBLICATIONS_ARTICLE_NAME])
            publication.clean_data()
            publications.append(publication)
        return publications


if __name__ == '__main__':
    
    from authors_data_processing import AuthorUtils, AUTORS_FILE_NAME

    # Input file name
    PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus.xlsx'

    all_authors = AuthorUtils.read_all_authors('./dataset', AUTORS_FILE_NAME)
    all_publications = PublicationUtils.read_all_publications('./dataset', PUBLICATIONS_FILE_NAME)
    # print(len(all_publications))
    print(all_publications[0])