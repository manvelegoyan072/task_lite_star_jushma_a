from litestar import Litestar
from litestar.config.app import AppConfig
from .routes import router
from .dependencies import provide_db
from litestar.plugins.sql_alchemy import SQLAlchemyAsyncConfig
from dotenv import load_dotenv
import os

load_dotenv()

db_config = SQLAlchemyAsyncConfig(
    connection_string=os.getenv("DATABASE_URL"),
)

app = Litestar(
    route_handlers=[router],
    dependencies={"repo": provide_db},
    plugins=[db_config],
)