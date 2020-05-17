import pandas as pd
import os
import math

# Input file names
AUTORS_FILE_NAME = 'UB_cs_authors.xlsx'
PUBLICATIONS_FILE_NAME = 'UB_cs_papers_scopus'

# Sheet names
FACULTY_NAMES = [
    'matematicki fakultet',
    'elektrotehnicki fakultet',
    'fakultet organizacionih nauka'
]

# FILE COLUMN NAMES
AUTHORS_FIRST_NAME = 'Ime'
AUTHORS_LAST_NAME = 'Prezime'
AUTHORS_MIDDLE_NAME = 'Srednje ime'
AUTHORS_DEPARTMENT_NAME = 'Odsek'
AUTHORS_FACULTY_NAME = 'Fakultet'

class Author():
    autoincrement = 1

    def __init__(self, first_name, last_name, middle_name, department, faculty):
        self.id = Author.autoincrement
        Author.autoincrement += 1
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.department = department
        self.faculty = faculty
        self.number_of_publications = 0
        self.collaborators = []

    def clean_data(self):
        self.validate_middle_name()
        self.change_all_names_to_lower_case()
        self.replace_latin_characters()

    def validate_middle_name(self):
        if isinstance(self.middle_name, float) and math.isnan(self.middle_name):
            self.middle_name = None 

    def change_all_names_to_lower_case(self):
         self.first_name = self.first_name.lower()
         self.last_name = self.last_name.lower()
         self.department = self.department.lower()
         self.faculty = self.faculty.lower()
         if self.middle_name:
             self.middle_name = self.middle_name.lower()

    def replace_latin_characters(self):
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

    def get_author_full_name(self):
        if self.middle_name:
            return f'{self.first_name} {self.middle_name}. {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Author: {self.first_name}, {self.middle_name}, {self.last_name} \
                \n        department = {self.department} \
                \n        faculty = {self.faculty}'


def read_all_authors():
    """Reads authors data from input file, does necessary data cleaning and returns dictionary of authors as result."""
    authors = dict()
    for faculty_name in FACULTY_NAMES:
        data = pd.read_excel(os.path.join('data', AUTORS_FILE_NAME), sheet_name=faculty_name)
        for column, row in data.iterrows():
            author = Author(row[AUTHORS_FIRST_NAME], row[AUTHORS_LAST_NAME], row[AUTHORS_MIDDLE_NAME], row[AUTHORS_DEPARTMENT_NAME], row[AUTHORS_FACULTY_NAME])
            author.clean_data()
            authors[author.get_author_full_name_tuple]= author
    return authors

# def clean_authors_data


if __name__ == '__main__':
    all_authors = read_all_authors()
    # for full_author_name in all_authors:
    #     print(all_authors[full_author_name])
    print(len(all_authors))

 

