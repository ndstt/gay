"""create tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2025-12-24 03:15:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_posts",
        sa.Column("source", sa.Text(), primary_key=True, nullable=False),
        sa.Column("external_id", sa.Text(), primary_key=True, nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("author", sa.Text(), nullable=True),
        sa.Column("published_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "ingested_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("lang", sa.Text(), nullable=True),
        sa.Column("metrics_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_json_path", sa.Text(), nullable=True),
    )
    op.create_index("idx_raw_posts_published_at", "raw_posts", ["published_at"], unique=False)
    op.create_index("idx_raw_posts_source", "raw_posts", ["source"], unique=False)

    op.create_table(
        "source_state",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("value_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("source", "key", name="uq_source_state_source_key"),
    )

    op.create_table(
        "ingest_logs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column(
            "started_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("ended_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("fetched_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("inserted_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("updated_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("error_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("extra_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("ingest_logs")
    op.drop_table("source_state")
    op.drop_index("idx_raw_posts_source", table_name="raw_posts")
    op.drop_index("idx_raw_posts_published_at", table_name="raw_posts")
    op.drop_table("raw_posts")
