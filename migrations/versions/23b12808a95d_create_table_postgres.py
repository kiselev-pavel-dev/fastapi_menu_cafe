"""Create table postgres

Revision ID: 23b12808a95d
Revises:
Create Date: 2023-01-24 19:53:17.654200

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "23b12808a95d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_menus_description"),
        "menus",
        ["description"],
        unique=False,
    )
    op.create_index(op.f("ix_menus_id"), "menus", ["id"], unique=False)
    op.create_index(op.f("ix_menus_title"), "menus", ["title"], unique=False)
    op.create_table(
        "submenus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("menu_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["menu_id"], ["menus.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_submenus_description"),
        "submenus",
        ["description"],
        unique=False,
    )
    op.create_index(op.f("ix_submenus_id"), "submenus", ["id"], unique=False)
    op.create_index(
        op.f("ix_submenus_title"),
        "submenus",
        ["title"],
        unique=False,
    )
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.String(), nullable=True),
        sa.Column("submenu_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["submenu_id"],
            ["submenus.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dishes_description"),
        "dishes",
        ["description"],
        unique=False,
    )
    op.create_index(op.f("ix_dishes_id"), "dishes", ["id"], unique=False)
    op.create_index(op.f("ix_dishes_title"), "dishes", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dishes_title"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_id"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_description"), table_name="dishes")
    op.drop_table("dishes")
    op.drop_index(op.f("ix_submenus_title"), table_name="submenus")
    op.drop_index(op.f("ix_submenus_id"), table_name="submenus")
    op.drop_index(op.f("ix_submenus_description"), table_name="submenus")
    op.drop_table("submenus")
    op.drop_index(op.f("ix_menus_title"), table_name="menus")
    op.drop_index(op.f("ix_menus_id"), table_name="menus")
    op.drop_index(op.f("ix_menus_description"), table_name="menus")
    op.drop_table("menus")
    # ### end Alembic commands ###
