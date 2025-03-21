from dependency_injector import containers, providers
from main.data_access_layer import SqlAlchemyDbContext
from main.application_layer.middleware.middleware import LoggingMiddleware, AuthMiddleware
from main.use_case_layer.user_service import UserService
from main.application_layer.controller.AuthController import AuthController
from main.application_layer import PyLogger
from main.data_access_layer import UnitOfWork


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db_context = providers.Singleton(
        SqlAlchemyDbContext,
        db_config={
            'db_type': config.DB_TYPE,
            'host': config.DB_HOST,
            'port': config.DB_PORT,
            'username': config.DB_USER,
            'password': config.DB_PASSWORD,
            'database': config.DB_NAME,
            'driver': config.DB_DRIVER
        },
        engine_params={
            'echo': config.DB_ECHO,
            'pool_size': config.DB_POOL_SIZE,
            'max_overflow': config.DB_MAX_OVERFLOW,
            'pool_timeout': config.DB_POOL_TIMEOUT
        }
    )

    logger = providers.Singleton(PyLogger)

    uow = providers.Factory(
        UnitOfWork,
        db_context=db_context
    )

    logging_middleware = providers.Singleton(LoggingMiddleware)
    auth_middleware = providers.Singleton(AuthMiddleware)


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    infrastructure = providers.DependenciesContainer()

    user_service = providers.Factory(
        UserService,
        uow=infrastructure.uow,
        logger=infrastructure.logger
    )


class ControllerContainer(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()

    auth_controller = providers.Factory(
        AuthController,
        auth_service=services.user_service
    )


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    infrastructure = providers.Container(
        InfrastructureContainer,
        config=config
    )

    services = providers.Container(
        ServiceContainer,
        config=config,
        infrastructure=infrastructure
    )

    controllers = providers.Container(
        ControllerContainer,
        services=services
    )