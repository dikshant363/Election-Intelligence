"""Models package initialization.

Infrastructure base models only - no business entities in Milestone 9.
"""

from app.database.base import Base, BaseModel

__all__ = ["Base", "BaseModel"]
