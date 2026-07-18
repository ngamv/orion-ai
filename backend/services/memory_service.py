from backend.database.database import get_connection

class MemoryService:

    def add(self, role, content):

        conn = get_connection()

        conn.execute(
            "INSERT INTO memory(role,content) VALUES(?,?)",
            (role, content)
        )

        conn.commit()
        conn.close()


    def history(self, limit=20):

        conn = get_connection()

        rows = conn.execute(
            """
            SELECT role,content,created_at
            FROM memory
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        conn.close()

        return [dict(r) for r in rows]
