import os
import sqlite3

from src.domain.dependency import Dependency
from src.repositories.dependency_repository import DependencyRepository


class SQLiteDependencyRepository(DependencyRepository):

    def __init__(self, db_folder, db_name="dependencies.db", reset_db=True):

        os.makedirs(db_folder, exist_ok=True)

        self.db_path = os.path.join(db_folder, db_name)

        if reset_db and os.path.exists(self.db_path):
            os.remove(self.db_path)

        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS dependencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            version TEXT,
            dep_type TEXT,
            source TEXT,
            purl TEXT
        )
        """

        self.conn.execute(query)
        self.conn.commit()

    def save(self, dependency):

        if self.exists(dependency.name, dependency.version, dependency.purl):
            return

        self.conn.execute(
            """
            INSERT INTO dependencies (
                name, version, dep_type, source, purl
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                dependency.name,
                dependency.version,
                dependency.dep_type,
                dependency.source,
                dependency.purl
            )
        )

        self.conn.commit()

    def exists(self, name, version, purl=None):

        cursor = self.conn.execute(
            """
            SELECT 1
            FROM dependencies
            WHERE name = ?
              AND version = ?
              AND (purl = ? OR (purl IS NULL AND ? IS NULL))
            LIMIT 1
            """,
            (name, version, purl, purl)
        )

        return cursor.fetchone() is not None

    def get_all(self):

        cursor = self.conn.execute("""
            SELECT name, version, dep_type, source, purl
            FROM dependencies
        """)

        return [
            Dependency(row[0], row[1], row[2], row[3], row[4])
            for row in cursor
        ]