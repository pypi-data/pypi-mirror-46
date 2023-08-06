from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from podder_task_base.settings import PIPELINE_DATABASE_URL
from podder_task_base.settings import PIPELINE_READ_ONLY_DATABASE_URL

from .sqlalchemy_logger_setting import SqlalchemyLoggerSetting

if PIPELINE_DATABASE_URL is not None:
    engine: Engine = create_engine(PIPELINE_DATABASE_URL, echo=False)
    Session: DeclarativeMeta = sessionmaker(bind=engine)
    SqlalchemyLoggerSetting()
else:
    Session: DeclarativeMeta = None

if PIPELINE_READ_ONLY_DATABASE_URL:
    read_only_engine: Engine = create_engine(PIPELINE_READ_ONLY_DATABASE_URL, echo=False)
    ReadOnlySession: DeclarativeMeta = sessionmaker(bind=read_only_engine)
elif PIPELINE_DATABASE_URL:
    read_only_engine: Engine = create_engine(PIPELINE_DATABASE_URL, echo=False)
    ReadOnlySession: DeclarativeMeta = sessionmaker(bind=read_only_engine)
else:
    ReadOnlySession: DeclarativeMeta = None