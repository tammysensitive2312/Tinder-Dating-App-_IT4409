from main.application_layer.routing.router import Router
from main.application_layer.middleware.middleware import LoggingMiddleware as logging_middleware


def setup_router(app, container):
    router = Router()
    router.middlewares = [logging_middleware]
    v1_group = router.group('/api/v1')
    v1_group.post('/register', container.auth_controller().register)

    for bp in router.generate_routes():
        app.register_blueprint(bp)