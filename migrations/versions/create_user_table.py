from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os
from app.models import User

load_dotenv()


alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "migrations")
alembic_cfg.set_main_option("version_locations", "migrations/versions")
alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


engine = create_async_engine(os.getenv("DATABASE_URL"))


def upgrade():
    with engine.connect() as connection:
        alembic_cfg.attributes["connection"] = connection
        alembic_cfg.attributes["target_metadata"] = User.metadata
        command.upgrade(alembic_cfg, "head")

def downgrade():
    with engine.connect() as connection:
        alembic_cfg.attributes["connection"] = connection
        alembic_cfg.attributes["target_metadata"] = User.metadata
        command.downgrade(alembic_cfg, "-1")

if __name__ == "__main__":
    upgrade()