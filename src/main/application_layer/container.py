from dependency_injector import containers, providers

from main.application_layer.controllers.auth_controller import AuthController
from main.application_layer.middlewares.middleware import LoggingMiddleware, AuthMiddleware
from main.application_layer.pylog import PyLogger
from main.data_access_layer import SqlAlchemyDbContext
from main.data_access_layer import UnitOfWork
from main.use_case_layer.user_service import UserService

from main.application_layer.constants import (
    DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD,
    DB_NAME, DB_DRIVER, DB_ECHO, DB_POOL_SIZE,
    DB_MAX_OVERFLOW, DB_POOL_TIMEOUT
)


class InfrastructureContainer(containers.DeclarativeContainer):

    db_context = providers.Singleton(
        SqlAlchemyDbContext,
        db_config={
            'db_type': DB_TYPE,
            'host': DB_HOST,
            'port': DB_PORT,
            'username': DB_USER,
            'password': DB_PASSWORD,
            'database': DB_NAME,
            'driver': DB_DRIVER
        },
        engine_params={
            'echo': DB_ECHO,
            'pool_size': DB_POOL_SIZE,
            'max_overflow': DB_MAX_OVERFLOW,
            'pool_timeout': DB_POOL_TIMEOUT
        }
    )

    logger = providers.Singleton(PyLogger)

    uow = providers.Factory(
        UnitOfWork,
        db_context=db_context
    )

    logging_middleware = providers.Singleton(
        LoggingMiddleware,
        app=providers.Object(None),
        logger=logger
    )
    auth_middleware = providers.Factory(
        AuthMiddleware,
        uow=uow
    )

class ServiceContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    user_service = providers.Factory(
        UserService,
        uow=infrastructure.uow,
        logger=infrastructure.logger
    )

class ControllerContainer(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    logger = providers.Dependency()

    auth_controller = providers.Factory(
        AuthController,
        auth_service=services.user_service,
        logger=logger
    )

class AppContainer(containers.DeclarativeContainer):

    infrastructure = providers.Container(InfrastructureContainer)

    services = providers.Container(
        ServiceContainer,
        infrastructure=infrastructure
    )

    controllers = providers.Container(
        ControllerContainer,
        services=services,
        logger=infrastructure.logger
    )