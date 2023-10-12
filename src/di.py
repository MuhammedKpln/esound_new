from dependency_injector import containers, providers

from auth import Auth
from config import Config
from database.database import Database
from services.graphql import GraphQLRequest


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    database = providers.Singleton(Database)
    graphql_request = providers.Singleton(GraphQLRequest)
    auth = providers.Singleton(
        Auth
    )
