# Standart libarry imports
import os
import math

# Standart libary imports
import pandas as pd

# Local project imports
from .settings import AUTHORS_DEPARTMENT_NAME, AUTHORS_FACULTY_NAME, AUTHORS_FIRST_NAME, AUTHORS_LAST_NAME, AUTHORS_MIDDLE_NAME, FACULTY_NAMES

class Author():
    """
    Author class containing all necessary attributes for nodes in scientific collaboration network graph.
    Provides some additional methods for cleaning up dataset.
    """
    autoincrement = 1

    def __init__(self, first_name, last_name, middle_name, department, faculty):
        self.id = Author.autoincrement
        Author.autoincrement += 1
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.department = department
        self.faculty = faculty
        self.collaborators = set()
        self.articles = set()
        self.papers = set()

    def clean_data(self):
        self._validate_middle_name()
        self._change_all_names_to_lower_case()
        self._replace_latin_characters()

    def _validate_middle_name(self):
        if isinstance(self.middle_name, float) and math.isnan(self.middle_name):
            self.middle_name = None 

    def _change_all_names_to_lower_case(self):
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.department = self.department.lower()
        self.faculty = self.faculty.lower()
        if self.middle_name:
            self.middle_name = self.middle_name.lower()

    def _replace_latin_characters(self):
        def replace_characters(name):
            name.replace('ć', 'c')
            name.replace('č', 'c')
            name.replace('š', 's')
            name.replace('đ', 'dj')
            name.replace('ž', 'z')
            return name
        self.first_name = replace_characters(self.first_name)
        self.last_name = replace_characters(self.last_name)
        self.department = replace_characters(self.department)
        self.faculty = replace_characters(self.faculty)
        if self.middle_name:
            self.middle_name = replace_characters(self.middle_name)
    
    def get_author_full_name_tuple(self):
        return (self.first_name, self.middle_name, self.last_name)

    def get_author_only_first_and_last_name_tuple(self):
        return (self.first_name, None, self.last_name)

    def get_author_full_name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name}. {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Author: {self.first_name}, {self.middle_name}, {self.last_name} \
                \n        department = {self.department} \
                \n        faculty = {self.faculty}'

class AuthorUtils():
    """
    Class containint various utility methods for dealing with authors as nodes of the scientific collaboration network graph. 
    """
    @staticmethod
    def read_all_authors(path, file_name):
        """Reads authors data from input file, does necessary data cleaning and returns dictionary of authors as result."""
        print('Importing Authors dataset...')
        authors = dict()
        for faculty_name in FACULTY_NAMES:
            data = pd.read_excel(os.path.join(path, file_name), sheet_name=faculty_name)
            for column, row in data.iterrows():
                author = Author(row[AUTHORS_FIRST_NAME], row[AUTHORS_LAST_NAME], row[AUTHORS_MIDDLE_NAME], row[AUTHORS_DEPARTMENT_NAME], row[AUTHORS_FACULTY_NAME])
                author.clean_data()
                authors[author.get_author_full_name_tuple()]= author
        return authors

    @staticmethod
    def get_all_authors_names(authors):
        """Returns list of tuples representing author names: (first name, middle name, last name)"""
        if not isinstance(authors, dict):
            return None
        else:
            return list(authors.keys())
    
    @staticmethod
    def format_all_authors_by_first_and_last_name(authors):
        """
        Returns dictionary containing mappings, without middle name if existed, "new author key" -> "original author key":
        (first name, None, last name) -> (first name, middle_name, last name)
        """
        if not isinstance(authors, dict):
            return None
        else:
            new_authors_dictionary = dict()
            for author_name in authors:
                new_authors_dictionary[(author_name[0], None, author_name[2])] = author_name
            return new_authors_dictionary

    @staticmethod
    def update_author_collaborators_and_publications_info(publications):
        """Based on extracted publications and it's mappings with authors, updates author's list of collaborators and articles where he was publishing."""
        # update author publications and collaborators
        for publication_name in publications:
            authors = publications[publication_name].authors
            publication_article_name = publications[publication_name].get_article_name()
            publication_type = publications[publication_name].get_publication_type()
            publication_title = publications[publication_name].get_publication_title()
            publication_year = publications[publication_name].get_publication_year()
            for author in authors:
                # Adding current article into list of aricles where author was publishing
                author.articles.add((publication_article_name, publication_type))

                # Adding current publication title to list of published papers 
                author.papers.add((publication_title, publication_type, publication_year))

                # Adding collaborators to list of collaborators, other authors that this one was working with
                collaborators = authors - set([author])     
                for collaborator in collaborators:
                    author.collaborators.add(collaborator)
