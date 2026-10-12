import os

import pymysql
try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

mcp = FastMCP("happy-paws")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3333")),
    "user": os.getenv("DB_USER", "happyuser"),
    "password": os.getenv("DB_PASSWORD", "happypassword"),
    "database": os.getenv("DB_NAME", "happy_paws"),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def init_db():
    """Create the pets table and add sample data if it is empty."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                species VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                adopted BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
        cur.execute("SELECT COUNT(*) AS n FROM pets")
        if cur.fetchone()["n"] == 0:
            cur.executemany(
                "INSERT INTO pets (name, species, age, adopted) VALUES (%s, %s, %s, %s)",
                [
                    ("Mochi", "dog", 3, False),
                    ("Luna", "cat", 2, False),
                    ("Biscuit", "rabbit", 1, True),
                ],
            )


@mcp.tool()
def list_pets(species: str | None = None, adopted: bool | None = None) -> list[dict]:
    """List pets, optionally filtered by species or adoption status."""
    sql = "SELECT * FROM pets WHERE 1=1"
    params = []
    if species:
        sql += " AND LOWER(species) = LOWER(%s)"
        params.append(species)
    if adopted is not None:
        sql += " AND adopted = %s"
        params.append(adopted)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@mcp.tool()
def get_pet(pet_id: int) -> dict:
    """Get one pet by id."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
        return cur.fetchone() or {"error": f"No pet with id {pet_id}"}


@mcp.tool()
def add_pet(name: str, species: str, age: int) -> dict:
    """Add a new pet to the shelter."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO pets (name, species, age) VALUES (%s, %s, %s)",
            (name, species, age),
        )
        cur.execute("SELECT * FROM pets WHERE id = %s", (cur.lastrowid,))
        return cur.fetchone()


@mcp.tool()
def adopt_pet(pet_id: int) -> str:
    """Mark a pet as adopted."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE pets SET adopted = TRUE WHERE id = %s", (pet_id,))
        if cur.rowcount == 0:
            return f"No pet with id {pet_id}, or it is already adopted."
    return f"Pet {pet_id} has been adopted!"


@mcp.tool()
def delete_pet(pet_id: int) -> str:
    """Remove a pet from the database."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
        if cur.rowcount == 0:
            return f"No pet with id {pet_id}."
    return f"Pet {pet_id} deleted."


@mcp.tool()
def run_select(query: str) -> list[dict]:
    """Run a read-only SELECT query on the happy_paws database."""
    if not query.strip().lower().startswith("select"):
        return [{"error": "Only SELECT queries are allowed."}]
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


if __name__ == "__main__":
    init_db()
    mcp.run(transport="stdio")