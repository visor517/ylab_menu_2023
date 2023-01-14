import sqlalchemy

from .base import metadata


menus = sqlalchemy.Table(
    'menus',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('title', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('description', sqlalchemy.String),
)

sub_menus = sqlalchemy.Table(
    'sub_menus',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('title', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('description', sqlalchemy.String),
)

dishes = sqlalchemy.Table(
    'dishes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('title', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('price', sqlalchemy.String),
)
