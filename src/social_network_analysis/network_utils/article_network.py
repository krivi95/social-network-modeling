from ..data_processing.authors_data_processing import Author
from .network_base import Node, Edge, EdgeType, Network

PUBLICATION_TYPE_TO_EXCLUDE = 'conference paper'

class ArticleNetwork(Network):
    """Class responsible for parsing inputed data, creating nodes and edges for Article graph and exporting to csv."""

    def __init__(self, publicaions):
        super().__init__()
        self.article = None
        self.publications = publicaions
        self.create_nodes()
        self.create_edges()

    def create_nodes(self):
        """Creates Articles."""        
        try:
            articles = dict()
            for publication_name in self.publications:
                publication_article_name = self.publications[publication_name].get_article_name()
                publication_type = self.publications[publication_name].get_publication_type()
                if publication_article_name not in articles and publication_type != PUBLICATION_TYPE_TO_EXCLUDE:
                    attributes = {'name': publication_article_name}
                    node = Node(attributes)
                    articles[publication_article_name] = node
            # Saving article dictionary for node creation
            self.articles = articles
            self.nodes = [articles[article_name] for article_name in articles]
        except Exception as e:
            print(e)
            return None

    def create_edges(self):
        """Creates edges (connecting two articles if at least one author exists who published papers in both articles)."""
        try:
            edges = dict()
            for publication_name in self.publications:
                publication_article_name = self.publications[publication_name].get_article_name()
                publication_authors = self.publications[publication_name].authors
                publication_type = self.publications[publication_name].get_publication_type()
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
                                article_id = self.articles[article_name].id
                                publication_article_id = self.articles[publication_article_name].id
                                edges[(publication_article_name, article_name)] = Edge(source=article_id, target=publication_article_id, edge_type=EdgeType.UNDIRRECTED.value)
            self.edges = [edges[key] for key in edges]
            return self.edges
        except Exception as e:
            print(e)
            return None