import os
from typing import List, Dict, Any
import psycopg
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """Manages PostgreSQL database connections and queries."""

    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")
        self.connection = None

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = psycopg.connect(
                self.connection_string,
                row_factory=psycopg.rows.dict_row,
                autocommit=True,  # Enable autocommit for read-only queries
                connect_timeout=10,  # Connection timeout in seconds
                keepalives=1,
                keepalives_idle=30,  # Send keepalive after 30 seconds of idle
                keepalives_interval=10,
                keepalives_count=5
            )
            print("✅ Database connected successfully")
            return True
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def get_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                if not self.connection or self.connection.closed:
                    self.connect()

                with self.connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        ORDER BY table_name;
                    """)
                    tables = [row['table_name'] for row in cursor.fetchall()]
                    return tables
            except Exception as e:
                print(f"Error fetching tables (attempt {attempt + 1}/{max_retries}): {e}")
                if self.connection:
                    try:
                        self.connection.close()
                    except:
                        pass
                    self.connection = None

                if attempt < max_retries - 1:
                    continue
                else:
                    return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a specific table."""
        try:
            if not self.connection:
                self.connect()

            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        column_name,
                        data_type,
                        is_nullable
                    FROM information_schema.columns
                    WHERE table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching schema for {table_name}: {e}")
            return []

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results."""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Check if connection is alive, reconnect if needed
                if not self.connection or self.connection.closed:
                    print(f"🔄 Connection closed, reconnecting... (attempt {attempt + 1})")
                    self.connect()

                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    print(f"✅ Query executed successfully: {len(results)} rows returned")
                    return results
            except Exception as e:
                print(f"❌ Query execution error (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"🔴 Failed query: {query}")

                # Close the bad connection and try to reconnect
                if self.connection:
                    try:
                        self.connection.close()
                    except:
                        pass
                    self.connection = None

                if attempt < max_retries - 1:
                    print("🔄 Retrying with new connection...")
                    continue
                else:
                    raise

    def get_database_context(self) -> str:
        """Get a summary of the database schema for context."""
        tables = self.get_tables()
        context = "Database Schema:\n\n"
        context += "IMPORTANT: Column names are case-sensitive and MUST be quoted with double quotes.\n\n"

        for table in tables:
            schema = self.get_table_schema(table)
            context += f"Table: {table}\n"
            context += "Columns:\n"
            for col in schema:
                # Show column names with quotes to indicate case-sensitivity
                context += f'  - "{col["column_name"]}" ({col["data_type"]})\n'

            # Add helpful hints for specific tables
            if table == "executions":
                context += "  Notes:\n"
                context += '    - Execution duration can be calculated: "updatedAt" - "createdAt"\n'
                context += '    - Use "remark" for process details/summaries\n'
                context += '    - "status" indicates execution state\n'
            elif table == "execution_logs":
                context += "  Notes:\n"
                context += '    - Contains detailed execution logs with "message" field\n'
                context += '    - Links to executions via "executionId"\n'

            context += "\n"

        return context
