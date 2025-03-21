from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class SqlAlchemyDbContext:
    def __init__(self, connection_string=None, db_config=None, engine_params=None):
        # Ưu tiên sử dụng connection_string nếu được cung cấp
        if connection_string:
            self.connection_string = connection_string
        # Nếu không có connection_string nhưng có db_config, xây dựng connection_string
        elif db_config:
            self.connection_string = self._build_connection_string(db_config)
        else:
            raise ValueError("Either connection_string or db_config must be provided")

        # Sử dụng engine_params được cung cấp hoặc tạo dict rỗng
        engine_params = engine_params or {}

        # Tạo engine với connection_string và các tham số
        self.engine = create_engine(self.connection_string, **engine_params)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.Model = declarative_base()

    def _build_connection_string(self, config):
        """Build connection string based on database type and config"""
        if not all(key in config for key in ['db_type', 'host', 'username', 'password', 'database']):
            raise ValueError("Missing required database configuration parameters")

        db_type = config['db_type'].lower()

        if db_type == 'postgresql':
            return f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', '5432')}/{config['database']}"

        elif db_type == 'mysql':
            return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', '3306')}/{config['database']}"

        elif db_type == 'sqlite':
            return f"sqlite:///{config['database']}"

        elif db_type == 'mssql':
            driver = config.get('driver', '')
            connection = f"mssql+pyodbc://{config['username']}:{config['password']}@{config['host']}:{config.get('port', '1433')}/{config['database']}"
            if driver:
                connection += f"?driver={driver}"
            return connection

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def init_db(self):
        self.Model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(bind=self.engine)