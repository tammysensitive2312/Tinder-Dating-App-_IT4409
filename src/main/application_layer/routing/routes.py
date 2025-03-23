from main.application_layer.routing.router import Router
from main.application_layer.pylog import PyLogger as log


def setup_router(app, container):
    router = Router()
    router.middlewares = []

    global_group = router.group('/api/v1')

    not_auth_group = global_group.group('/auth')
    not_auth_group.post('/signup', container.controllers.auth_controller().register)
    # not_auth_group.post('/login', container.controllers.auth_controller().login)
    # not_auth_group.post('/refresh-token', container.controllers.auth_controller().refresh_token)
    # not_auth_group.post('/reset-password', container.controllers.auth_controller().reset_password)
    # not_auth_group.put('/reset-password', container.controllers.auth_controller().reset_password)

    for bp in router.generate_routes():
        app.register_blueprint(bp)