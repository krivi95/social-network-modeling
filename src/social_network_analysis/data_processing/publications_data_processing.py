# Standart libarry imports
import os
import math
from collections import namedtuple

# Third party imports
import pandas as pd

# Local project imports
from .authors_data_processing import AuthorUtils
from .settings import PUBLICATIONS_ARTICLE_NAME, PUBLICATIONS_AUTHOR, PUBLICATIONS_AUTHORS, PUBLICATIONS_PAPER_TITLE, PUBLICATIONS_TYPE, PUBLICATIONS_YEAR, VALID_PUBLICATION_TYPES
                      

# Each publication is uniquely identified by following fields: title, authors and year
UniquePublication = namedtuple('UniquePublication', ['authors', 'year', 'title'])

class PublicationRecord:
    """
    Class containing necessary information about publications and co-authors from input file.
    Provides some additional methods for cleaning up dataset.
    One instance represents one row in input file.
    """ 
    def __init__(self, author, publication_title, publication_authors, publication_year, publication_type, article_name):
        self.author = author
        self.publication_title = publication_title
        self.publication_authors = publication_authors
        self.publication_year = publication_year 
        self.publication_type = publication_type
        self.article_name = article_name 

    def get_unique_publication_id(self):
        """Returns tuble of attributs that is unique for each publication"""
        return UniquePublication(title=self.publication_title, authors=self.publication_authors, year=self.publication_year)
        
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

class Publication:
    """
    Contains full information on publication. It has mapped authors with entiries from authors sourse file.
    It contains all occurences of one, same publication but under different authors found in source file 
    (for each of the co-authors there will be duplicated entry for that publication). 
    """ 
    def __init__(self):
        self.authors = set()
        self.publication_records = []

    def add_mapped_author(self, author):
        self.authors.add(author)

    def add_publication_record(self, publication_record):
        self.publication_records.append(publication_record)
    
    def get_publication_title(self):
        if self.publication_records is None:
            return None
        return self.publication_records[0].publication_title

    def get_publication_year(self):
        if self.publication_records is None:
            return None
        return self.publication_records[0].publication_year

    def get_publication_type(self):
        if self.publication_records is None:
            return None
        return self.publication_records[0].publication_type
    
    def get_article_name(self):
        if self.publication_records is None:
            return None
        return self.publication_records[0].article_name
    

class PublicationUtils:
    """
    Class containint various utility methods for dealing with publication and various information about scientific publications,  
    """

    @staticmethod
    def read_all_publications(path, file_name):
        """
        Reads publication records and keeps orginal raw format from dataset. 
        """
        print('Importing Publications (authors published reasearch papaers) dataset...')
        publications = []
        data = pd.read_excel(os.path.join(path, file_name))
        for column, row in data.iterrows():
            if row[PUBLICATIONS_TYPE] not in VALID_PUBLICATION_TYPES:
                continue
            publication = PublicationRecord(author=row[PUBLICATIONS_AUTHOR],
                                      publication_title=row[PUBLICATIONS_PAPER_TITLE],
                                      publication_authors=row[PUBLICATIONS_AUTHORS],
                                      publication_year=row[PUBLICATIONS_YEAR],
                                      publication_type=row[PUBLICATIONS_TYPE],
                                      article_name=row[PUBLICATIONS_ARTICLE_NAME])
            publication.clean_data()
            publications.append(publication)
        return publications

    @staticmethod
    def map_publications_with_users(publication_records, authors):
        """
        Keeps only one main record per publication (in dataset if there are e.g. 3 authors for one publication there will be 3 rows for same publication, 
        for each author separately). One publication is identified by: list of authors, year and title of paper. 
        Returns dictionary of publications. 
        """
        publications = dict()
        author_names = AuthorUtils.get_all_authors_names(authors)
        author_names_no_middle = AuthorUtils.format_all_authors_by_first_and_last_name(authors)
        for publication_record in publication_records:
            mapped_author = PublicationUtils._map_publication_author_name_with_author_entry(publication_record.author, authors, author_names, author_names_no_middle)
            if mapped_author is None:
                print("NON EXISTING USER", publication_record.author)
            else:
                unique_publication_id = publication_record.get_unique_publication_id()
                if unique_publication_id not in publications:
                    publications[unique_publication_id] = Publication()                                        
                publications[unique_publication_id].add_mapped_author(mapped_author)
                publications[unique_publication_id].add_publication_record(publication_record)
        return publications

    @staticmethod
    def _map_publication_author_name_with_author_entry(publication_author_name, authors, author_names, author_names_no_middle):
        """Returns mapped author if found."""
        full_author_name = PublicationUtils._format_publication_author_name(publication_author_name)
        if full_author_name in author_names:
            # match by full name: first, middle and last name
            return authors[full_author_name]
        elif full_author_name in author_names_no_middle:
            return authors[author_names_no_middle[full_author_name]]
        else:
            # TODO: log non-existing authors
            return None
        
    @staticmethod
    def _format_publication_author_name(publication_author_name):
        """Returns tuple (first name, middle name, last name) scraped from author's name in publication entry. Name can be found in various formats."""
        first_name = None
        middle_name = None
        last_name = None
        partial_names = publication_author_name.split()
        if len(partial_names) > 4:
            # maximum allowed format is: "LastName1 LastName2 FirstName MN"
            # TODO: log wrong author name format
            return None
        if len(partial_names[-1]) == 1:
            # middle name
            middle_name = partial_names[-1]
            first_name = partial_names[-2]
            last_name = ' '.join(partial_names[:-2])
        else:
            first_name = partial_names[-1]
            last_name = ' '.join(partial_names[:-1])
        return (first_name, middle_name, last_name)


