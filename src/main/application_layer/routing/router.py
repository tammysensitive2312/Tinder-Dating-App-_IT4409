from typing import Dict, List, Callable, Optional

from flask import Blueprint


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
        self._root = None

    @property
    def root(self):
        """Trả về router gốc."""
        if self.parent is None:
            return self

        if self._root is None:
            self._root = self.parent.root
        return self._root

    def get_full_prefix(self):
        """Tính toán prefix đầy đủ bao gồm cả prefix của các parent."""
        if self.parent is None:
            return self.prefix

        parent_prefix = self.parent.get_full_prefix()
        combined = f"{parent_prefix}{self.prefix}"
        return combined.replace("//", "/")

    def add_route(self, path: str, handler: Callable, methods: List[str], middlewares: List[Callable] = None):
        """Thêm route vào router."""
        # Đảm bảo path bắt đầu bằng /
        if not path.startswith('/'):
            path = '/' + path

        # Tính toán đường dẫn đầy đủ
        full_prefix = self.get_full_prefix()
        full_path = f"{full_prefix}{path}".replace("//", "/")

        # Đảm bảo đường dẫn đầy đủ bắt đầu bằng /
        if not full_path.startswith('/'):
            full_path = '/' + full_path

        # Thêm route vào router gốc
        combined_middlewares = self.middlewares + (middlewares or [])
        if self.parent is None:
            # Đây là router gốc, lưu route
            print(f"Registering route: {full_path}")
            self._routes[full_path] = Route(full_path, handler, methods, combined_middlewares)
        else:
            # Chuyển route lên router gốc
            self.root._routes[full_path] = Route(full_path, handler, methods, combined_middlewares)

    def group(self, prefix: str, middlewares: List[Callable] = None) -> 'Router':
        """Tạo subgroup với prefix và middlewares, liên kết với router cha."""
        if not prefix.startswith('/'):
            prefix = '/' + prefix

        subgroup = Router(prefix=prefix, parent=self)
        subgroup.middlewares = self.middlewares + (middlewares or [])

        full_prefix = subgroup.get_full_prefix()
        print(f"Created group with prefix: {prefix}, full prefix: {full_prefix}")

        return subgroup

    def post(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['POST'], middlewares)

    def get(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['GET'], middlewares)

    def put(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['PUT'], middlewares)

    def delete(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['DELETE'], middlewares)

    def patch(self, path: str, handler: Callable, middlewares: List[Callable] = None):
        self.add_route(path, handler, ['PATCH'], middlewares)

    def register_blueprint(self, name: str, blueprint: Blueprint):
        self.blueprints[name] = blueprint

    def _apply_middlewares(self, handler: Callable, middlewares: List[Callable]) -> Callable:
        """Áp dụng middleware cho handler."""
        for middleware in reversed(middlewares):
            handler = middleware(handler)
        return handler

    def generate_routes(self) -> List[Blueprint]:
        """Tạo các blueprint từ routes đã đăng ký."""
        blueprints = []

        for path, route in self._routes.items():
            # Tạo blueprint với tên duy nhất dựa trên đường dẫn
            bp_name = f"route_{path.replace('/', '_').lstrip('_')}"
            bp = Blueprint(bp_name, __name__)

            wrapped_handler = self._apply_middlewares(
                route.handler,
                route.middlewares
            )

            print(f"Adding URL rule: {path} with methods {route.methods}")

            bp.add_url_rule(
                path,
                view_func=wrapped_handler,
                methods=route.methods
            )

            blueprints.append(bp)
            self.register_blueprint(f"bp_{path}", bp)

        return blueprints