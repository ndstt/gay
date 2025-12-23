from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, Index, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RawPost(Base):
    __tablename__ = "raw_posts"

    source: Mapped[str] = mapped_column(Text, primary_key=True)
    external_id: Mapped[str] = mapped_column(Text, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    lang: Mapped[str | None] = mapped_column(Text, nullable=True)
    metrics_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    raw_json_path: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("idx_raw_posts_published_at", "published_at"),
        Index("idx_raw_posts_source", "source"),
    )


class SourceState(Base):
    __tablename__ = "source_state"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    key: Mapped[str] = mapped_column(Text, nullable=False)
    value_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (UniqueConstraint("source", "key", name="uq_source_state_source_key"),)


class IngestLog(Base):
    __tablename__ = "ingest_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    fetched_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    inserted_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    updated_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
