from main.application_layer.routing.router import Router
from main.application_layer.container import InfrastructureContainer



def setup_router(app, container):
    router = Router()
    router.middlewares = []

    logging_middleware = InfrastructureContainer.logging_middleware(app=app)
    auth_middleware = InfrastructureContainer.auth_middleware()

    global_group = router.group('/api/v1')

    not_auth_group = global_group.group('/auth')
    not_auth_group.post('/signup', container.controllers.auth_controller().register)
    not_auth_group.post('/login', container.controllers.auth_controller().login)
    not_auth_group.post('/refresh-token', container.controllers.auth_controller().refresh_token)
    not_auth_group.post('/reset-password', container.controllers.auth_controller().reset_password)
    not_auth_group.put('/reset-password', container.controllers.auth_controller().confirm_reset_password)
    '''api này cần auth'''
    not_auth_group.post('/change-password',
                        container.controllers.auth_controller().change_password,
                        [auth_middleware])

    for bp in router.generate_routes():
        app.register_blueprint(bp)