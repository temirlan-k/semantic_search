from logging.config import fileConfig
import os
import re

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.infrastructure.database import models
from src.infrastructure.database.models.mixins import Base
from config.config import settings

DATABASES = {
    "url": str(settings.db.url),
    "metadata": Base.metadata,
}


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = DATABASES["metadata"]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def process_revision_directives(context, revision, directives):
    if not directives:
        return

    migration_script = directives[0]

    specific_version_path = os.path.join(context.script.dir, "versions", "default")
    os.makedirs(specific_version_path, exist_ok=True)

    max_num = 0
    pattern = re.compile(r'^(\d+)_')
    try:
        for filename in os.listdir(specific_version_path):
            match = pattern.match(filename)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
    except FileNotFoundError:
        pass

    new_rev_id = f"{max_num + 1:04d}_{migration_script.rev_id}"
    migration_script.rev_id = new_rev_id

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option(DATABASES["url"])
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_cfg = config.get_section(config.config_ini_section)
    alembic_cfg["sqlalchemy.url"] = DATABASES["url"]
    connectable = engine_from_config(
        alembic_cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            process_revision_directives=process_revision_directives
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
