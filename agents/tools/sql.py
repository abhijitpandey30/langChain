import sqlite3
from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List
conn = sqlite3.connect("db.sqlite");

def list_tables():
    c=conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)

def run_sqlite_query(query):
    try:
        c = conn.cursor();
        c.execute(query)
        return c.fetchall();
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"
    
def describe_tables(table_names):
    if isinstance(table_names, str):
        table_names = [table_names]
    print(f"table_names:{table_names}")
    c = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    print(f"tables:{tables}")
    rows = c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables})")
    return "\n".join(row[0] for row in rows if row[0] is not None)

class RunQueryArgsSchema(BaseModel):
    query:str

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema

)

class DescribeTablesArgsSchema(BaseModel):
    table_names:List[str]

describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of tables, returns the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema

)