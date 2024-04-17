"""Add initial data

Revision ID: 5057313c2e61
Revises: 1761300297b8
Create Date: 2024-04-16 03:55:40.152418

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select

# revision identifiers, used by Alembic.
revision: str = "5057313c2e61"
down_revision: str = "1761300297b8"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    cities_table = sa.table(
        "cities", sa.column("id", sa.Integer), sa.column("name", sa.String)
    )

    # Измените вызов select, чтобы передавать столбцы напрямую, а не в списке
    present_cities = conn.execute(
        select(cities_table.c.name)  # Используйте select без квадратных скобок
    ).fetchall()
    present_cities = {name[0] for name in present_cities}

    cities_data = [
        "Renton",
        "SoDo",
        "Factoria",
        "Issaquah",
        "Seattle",
        "Bellevue",
        "Redmond",
        "Eastlake",
        "Northup",
    ]
    new_cities = [
        {"name": name} for name in cities_data if name not in present_cities
    ]
    if new_cities:
        conn.execute(cities_table.insert(), new_cities)

    city_ids = conn.execute(
        select(
            cities_table.c.id, cities_table.c.name
        )  # Аналогично, без квадратных скобок
    ).fetchall()
    city_id_map = {name: id for id, name in city_ids}

    routes_table = sa.table(
        "routes",
        sa.column("id", sa.Integer),
        sa.column("from_city_id", sa.Integer),
        sa.column("to_city_id", sa.Integer),
        sa.column("distance", sa.Integer),
    )

    routes_data = [
        ("Renton", "SoDo", 12),
        ("SoDo", "Renton", 12),
        ("Renton", "Factoria", 8),
        ("Factoria", "Renton", 8),
        ("Renton", "Issaquah", 12),
        ("Issaquah", "Renton", 12),
        ("SoDo", "Factoria", 8),
        ("Factoria", "SoDo", 8),
        ("SoDo", "Seattle", 1),
        ("Seattle", "SoDo", 1),
        ("Factoria", "Bellevue", 2),
        ("Bellevue", "Factoria", 2),
        ("Factoria", "Redmond", 9),
        ("Redmond", "Factoria", 9),
        ("Factoria", "Issaquah", 10),
        ("Issaquah", "Factoria", 10),
        ("Issaquah", "Redmond", 14),
        ("Redmond", "Issaquah", 14),
        ("Seattle", "Eastlake", 2),
        ("Eastlake", "Seattle", 2),
        ("Eastlake", "Northup", 8),
        ("Northup", "Eastlake", 8),
        ("Bellevue", "Northup", 1),
        ("Northup", "Bellevue", 1),
        ("Bellevue", "Redmond", 8),
        ("Redmond", "Bellevue", 8),
        ("Northup", "Redmond", 5),
        ("Redmond", "Northup", 5),
    ]

    new_routes = [
        {
            "from_city_id": city_id_map[from_city],
            "to_city_id": city_id_map[to_city],
            "distance": distance,
        }
        for from_city, to_city, distance in routes_data
    ]
    conn.execute(routes_table.insert(), new_routes)


def downgrade():
    conn = op.get_bind()
    # Специфическое удаление данных
    conn.execute(
        "DELETE FROM routes WHERE distance IN (12, 8, 1, 2, 9, 10, 14, 5)"
    )
    conn.execute(
        """
    DELETE FROM cities WHERE name IN (
        'Renton', 'SoDo', 'Factoria', 'Issaquah', 
        'Seattle', 'Bellevue', 'Redmond', 'Eastlake', 'Northup'
    )
    """
    )
