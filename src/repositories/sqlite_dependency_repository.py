import sqlite3
from src.domain.dependency import Dependency


class SQLiteDependencyRepository(DependencyRepository):
    def __init__(self, db_path="dependencies.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS dependencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            version TEXT,
            type TEXT,
            source TEXT,
            is_used BOOLEAN,
            is_deprecated BOOLEAN,
            last_update TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save(self, dependency):
        query = """
        INSERT INTO dependencies 
        (name, version, type, source, is_used, is_deprecated, last_update)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (
            dependency.name,
            dependency.version,
            dependency.type,
            dependency.source,
            dependency.is_used,
            dependency.is_deprecated,
            dependency.last_update
        ))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT name, version, type, source, is_used, is_deprecated, last_update FROM dependencies")
        
        dependencies = []
        for row in cursor:
            dep = Dependency(
                name=row[0],
                version=row[1],
                dep_type=row[2],
                source=row[3]
            )
            dep.is_used = row[4]
            dep.is_deprecated = row[5]
            dep.last_update = row[6]

            dependencies.append(dep)

        return dependencies

    def find_by_name(self, name):
        cursor = self.conn.execute(
            "SELECT name, version, type, source, is_used, is_deprecated, last_update FROM dependencies WHERE name = ?",
            (name,)
        )

        row = cursor.fetchone()
        if row:
            dep = Dependency(row[0], row[1], row[2], row[3])
            dep.is_used = row[4]
            dep.is_deprecated = row[5]
            dep.last_update = row[6]
            return dep

        return None