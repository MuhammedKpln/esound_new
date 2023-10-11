from dependency_injector import containers, providers

from auth import Auth
from config import Config
from services.graphql import GraphQLRequest


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    graphql_request = providers.Singleton(GraphQLRequest)
    auth = providers.Singleton(
        Auth
    )
