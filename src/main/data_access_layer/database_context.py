import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


class SqlAlchemyDbContext:
    def __init__(self, env_file_path='.env'):
        # Load environment variables
        load_dotenv(env_file_path)
        connection_string = os.getenv('DATABASE_URL')
        if not connection_string:
            db_type = os.getenv('DB_TYPE')
            host = os.getenv('DB_HOST')
            port = os.getenv('DB_PORT')
            username = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            database = os.getenv('DB_NAME')

            if not all([db_type, host, username, password, database]):
                raise ValueError("Missing required database configuration. Please check your .env file.")

            connection_string = self._build_connection_string({
                'db_type': db_type,
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'database': database
            })

        engine_params = {
            'echo': os.getenv('DB_ECHO', '').lower() == 'true'
        }

        if os.getenv('DB_POOL_SIZE'):
            engine_params['pool_size'] = int(os.getenv('DB_POOL_SIZE'))

        if os.getenv('DB_MAX_OVERFLOW'):
            engine_params['max_overflow'] = int(os.getenv('DB_MAX_OVERFLOW'))

        if os.getenv('DB_POOL_TIMEOUT'):
            engine_params['pool_timeout'] = int(os.getenv('DB_POOL_TIMEOUT'))

        self.engine = create_engine(connection_string, **engine_params)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.Model = declarative_base()

    def _build_connection_string(self, config):
        """Build connection string based on database type and config"""
        db_type = config['db_type'].lower()

        if db_type == 'postgresql':
            return f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', '5432')}/{config['database']}"

        elif db_type == 'mysql':
            return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config.get('port', '3306')}/{config['database']}"

        elif db_type == 'sqlite':
            return f"sqlite:///{config['database']}"

        elif db_type == 'mssql':
            driver = os.getenv('DB_DRIVER', '')
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