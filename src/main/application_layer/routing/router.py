from typing import Dict, List, Callable, Optional
from flask import Request, Response, Blueprint

class Route:
    def __init__(self, path: str, handler: Callable, methods: List[str], middlewares: List[Callable] = None):
        self.path = path
        self.handler = handler
        self.methods = methods
        self.middlewares = middlewares or []

class Router:
    def __init__(self, prefix: str = "", parent: Optional['Router'] = None):
        self.blueprints: Dict[str, Blueprint] = {}
        self._routes: Dict[str, Route] = {}
        self.prefix = prefix
        self.parent = parent
        self.middlewares: List[Callable] = []

    def add_route(self, path: str, handler: Callable, methods: List[str], middlewares: List[Callable] = None):
        full_path = f"{self.prefix}{path}".replace("//", "/")
        if self.parent:
            self.parent.add_route(full_path, handler, methods, self.middlewares + (middlewares or []))
        else:
            self._routes[full_path] = Route(full_path, handler, methods, self.middlewares + (middlewares or []))

    def group(self, prefix: str, middlewares: List[Callable] = None) -> 'Router':
        """Tạo subgroup với prefix và middlewares, liên kết với router cha."""
        subgroup = Router(prefix=f"{self.prefix}{prefix}", parent=self)
        subgroup.middlewares = self.middlewares + (middlewares or [])
        return subgroup

    def post(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['POST'], middlewares)

    def register_blueprint(self, name: str, blueprint: Blueprint):
        self.blueprints[name] = blueprint

    def _apply_middlewares(self, handler: Callable, middlewares: List[Callable]) -> Callable:
        for middleware in reversed(middlewares):
            handler = middleware(handler)
        return handler

    def generate_routes(self) -> List[Blueprint]:
        for path, route in self._routes.items():
            bp = Blueprint(f'route_{path}', __name__)
            wrapped_handler = self._apply_middlewares(
                route.handler,
                self.middlewares + route.middlewares
            )
            bp.add_url_rule(
                path,
                view_func=wrapped_handler,
                methods=route.methods
            )
            self.register_blueprint(f'bp_{path}', bp)
        return list(self.blueprints.values())