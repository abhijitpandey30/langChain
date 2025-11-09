# tools/report.py
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Annotated


def write_report(filename: str, html: str) -> None:
    """Write an HTML report to disk."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)


class WriteReportArgs(BaseModel):
    filename: Annotated[str, Field(description="The file name to save the HTML report as.")]
    html: Annotated[str, Field(description="The HTML content of the report.")]


write_report_tool = StructuredTool.from_function(
    func=write_report,
    name="write_report",
    description=(
        "Write an HTML file to disk. "
        "Use this tool whenever a user requests a report or HTML output."
    ),
    args_schema=WriteReportArgs,
)
