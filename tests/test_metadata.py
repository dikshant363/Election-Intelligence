"""Tests for declarative base and constraint metadata naming conventions."""

from app.database.base import Base, BaseModel
from app.database.metadata import metadata


def test_naming_convention_keys() -> None:
    """Verify metadata constraint naming conventions for Alembic compatibility."""
    assert metadata.naming_convention is not None
    assert metadata.naming_convention["pk"] == "pk_%(table_name)s"
    assert (
        metadata.naming_convention["fk"]
        == "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    )
    assert metadata.naming_convention["ix"] == "ix_%(table_name)s_%(column_0_label)s"
    assert metadata.naming_convention["uq"] == "uq_%(table_name)s_%(column_0_name)s"
    assert metadata.naming_convention["ck"] == "ck_%(table_name)s_%(constraint_name)s"


def test_base_model_abstract_structure() -> None:
    """Verify abstract BaseModel attribute structure."""
    assert Base is not None
    assert BaseModel.__abstract__ is True
    assert hasattr(BaseModel, "id")
    assert hasattr(BaseModel, "created_at")
    assert hasattr(BaseModel, "updated_at")
    assert hasattr(BaseModel, "deleted_at")
    assert hasattr(BaseModel, "version")
