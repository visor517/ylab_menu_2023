import sqlalchemy

from db.base import metadata


menus = sqlalchemy.Table(
    'menus',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
)

sub_menus = sqlalchemy.Table(
    'sub_menus',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('menu', sqlalchemy.String, sqlalchemy.ForeignKey('menus.id'), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
)

dishes = sqlalchemy.Table(
    'dishes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('sub_menu', sqlalchemy.String, sqlalchemy.ForeignKey('sub_menus.id'), nullable=False),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('description', sqlalchemy.String),
    sqlalchemy.Column('price', sqlalchemy.String),
)
