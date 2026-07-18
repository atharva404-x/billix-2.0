"""
Billix — SQLAlchemy declarative base.

All ORM models must inherit from ``Base`` defined here. This ensures a single
metadata registry that Alembic can introspect for auto-generating migrations.
"""

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase):
    """
    Base class for all Billix ORM models.

    Usage::

        from app.db.base import Base

        class User(Base):
            __tablename__ = "users"
            ...
    """

    pass
