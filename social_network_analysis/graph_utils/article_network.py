from ..data_processing.authors_data_processing import Author
from .graph_base import Node, Edge, EdgeType

PUBLICATION_TYPE_TO_EXCLUDE = 'conference paper'

class ArticleNetwork():

    @staticmethod
    def create_article_nodes(publications):
        """Goes through publications and searches for article where those papers were published."""        
        try:
            articles = dict()
            for publication_name in publications:
                publication_article_name = publications[publication_name].get_article_name()
                publication_type = publications[publication_name].get_publication_type()
                if publication_article_name not in articles and publication_type != PUBLICATION_TYPE_TO_EXCLUDE:
                    attributes = {'name': publication_article_name}
                    node = Node(attributes)
                    articles[publication_article_name] = node
            return articles
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def export_nodes_to_csv(artcles, path, file_name):
        """Exporting nodes (Articles) to csv."""
        try:
            Node.export_to_csv(artcles, path, file_name)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def export_edges_to_csv(publications, articles, path, file_name):
        """Exporting edges (connecting two articles if at least one author exists who published papers in both articles)."""
        try:
            edges = dict()
            for publication_name in publications:
                publication_article_name = publications[publication_name].get_article_name()
                publication_authors = publications[publication_name].authors
                publication_type = publications[publication_name].get_publication_type()
                if publication_type != PUBLICATION_TYPE_TO_EXCLUDE:
                    for author in publication_authors:
                        # For current article, where this paper was published,
                        # we look at other artiles where authors for this paper were publishing as well.
                        # For those article pairs, we create new link.
                        for article in author.articles:
                            article_name = article[0] 
                            if article_name == publication_article_name:
                                continue
                            if article[1] == PUBLICATION_TYPE_TO_EXCLUDE:
                                continue
                            if (article_name, publication_article_name) not in edges and (publication_article_name, article_name) not in edges: 
                                article_id = articles[article_name].id
                                publication_article_id = articles[publication_article_name].id
                                edges[(publication_article_name, article_name)] = Edge(source=article_id, target=publication_article_id, edge_type=EdgeType.UNDIRRECTED.value)
            Edge.export_to_csv([edges[key] for key in edges], path, file_name)
            return True
        except Exception as e:
            print(e)
            return False