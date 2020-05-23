# Local package imports
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
    # CoAuthorNetwork.export_nodes_to_csv(all_authors, path='output', file_name='CoAuthor Network - Nodes')
    # CoAuthorNetwork.export_edges_to_csv(publications, path='output', file_name='CoAuthor Network - Edges')

   
    
    # update author publications and collaborators
    for publication_name in publications:
        authors = publications[publication_name].authors
        publication_article_name = publications[publication_name].get_article_name()
        publication_type = publications[publication_name].get_publication_type()
        if publication_type != 'conference paper':
            for author in authors:
                # Adding current article into list of aricles wher author was publishing
                author.articles.add(publication_article_name)

                # Adding collaborators to list of collaborators, other authors that this one was working with
                collaborators = authors - set([author])     
                for collaborator in collaborators:
                    author.collaborators.add(collaborator)




    from social_network_analysis.graph_utils.graph_base import Node, Edge, EdgeType

    # create article nodes
    articles = dict()
    for publication_name in publications:
        publication_article_name = publications[publication_name].get_article_name()
        publication_type = publications[publication_name].get_publication_type()
        if publication_article_name not in articles and publication_type != 'conference paper':
            attributes = {'name': publication_article_name}
            node = Node(attributes)
            articles[publication_article_name] = node
    Node.export_to_csv([articles[article_name] for article_name in articles], 'output', 'Article Network - Nodes')

 
    edges = dict()
    for publication_name in publications:
        publication_article_name = publications[publication_name].get_article_name()
        publication_authors = publications[publication_name].authors
        publication_type = publications[publication_name].get_publication_type()
        if publication_type != 'conference paper':
            for author in publication_authors:
                # For current article, where this paper was published,
                # we look at other artiles where authors for this paper were publishing as well.
                # For those article pairs, we create new link.
                for article_name in author.articles:
                    if article_name == publication_article_name:
                        continue
                    if (article_name, publication_article_name) not in edges and (publication_article_name, article_name) not in edges: 
                        article_id = articles[article_name].id
                        publication_article_id = articles[publication_article_name].id
                        edges[(publication_article_name, article_name)] = Edge(source=article_id, target=publication_article_id, edge_type=EdgeType.UNDIRRECTED.value)
    
    Edge.export_to_csv([edges[key] for key in edges], 'output', 'Article Network - Edges')
        
    

