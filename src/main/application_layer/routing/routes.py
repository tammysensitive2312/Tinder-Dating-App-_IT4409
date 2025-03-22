from main.application_layer.routing.router import Router


def setup_router(app, container):
    router = Router()
    router.middlewares = []

    global_group = router.group('/api/v1')
    global_group.post('/register', container.controllers.auth_controller().register)

    for bp in router.generate_routes():
        app.register_blueprint(bp)