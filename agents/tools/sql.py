# tools/sql.py
import sqlite3
from typing import List, Annotated

from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

# Create a single connection for simplicity
conn = sqlite3.connect("db.sqlite")


def list_tables() -> str:
    """Return a list of all table names in the SQLite database."""
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


def run_sqlite_query(query: str):
    """Execute a SQL query and return results."""
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"


def describe_tables(table_names: List[str]):
    """Return the CREATE TABLE SQL for the given list of table names."""
    c = conn.cursor()
    if isinstance(table_names, str):
        table_names = [table_names]

    formatted = ", ".join(f"'{table}'" for table in table_names)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({formatted})"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


# --- Pydantic argument schemas ---
class RunQueryArgs(BaseModel):
    query: Annotated[str, Field(description="The SQL query to execute.")]


class DescribeTablesArgs(BaseModel):
    table_names: Annotated[List[str], Field(description="Names of tables to describe.")]


# --- Tools definitions (new API) ---
run_query_tool = StructuredTool.from_function(
    func=run_sqlite_query,
    name="run_sqlite_query",
    description="Run a SQL query against the SQLite database and return results.",
    args_schema=RunQueryArgs,
)

describe_tables_tool = StructuredTool.from_function(
    func=describe_tables,
    name="describe_tables",
    description="Given a list of tables, return their CREATE TABLE schema definitions.",
    args_schema=DescribeTablesArgs,
)
