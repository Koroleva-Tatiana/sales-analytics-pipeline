"""Creating an Excel report from the SQLite database."""

import logging
import sqlite3
from pathlib import Path

import pandas as pd
from openpyxl.chart import LineChart, Reference

from analysis import CATEGORY_REVENUE_SQL, DB_PATH, MONTHLY_REVENUE_SQL, run_query

logger = logging.getLogger(__name__)

REPORT_PATH = Path("output/report.xlsx")


def create_report(conn: sqlite3.Connection, output_path: Path = REPORT_PATH) -> None:
    """Write monthly revenue and top categories to an Excel file with a chart."""
    monthly = run_query(MONTHLY_REVENUE_SQL, conn)
    categories = run_query(CATEGORY_REVENUE_SQL, conn)

    output_path.parent.mkdir(exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        monthly.to_excel(writer, sheet_name="Monthly revenue", index=False)
        categories.to_excel(writer, sheet_name="Top categories", index=False)

        sheet = writer.sheets["Monthly revenue"]
        chart = LineChart()
        chart.title = "Monthly revenue (delivered orders)"
        values = Reference(sheet, min_col=3, min_row=1, max_row=len(monthly) + 1)
        months = Reference(sheet, min_col=1, min_row=2, max_row=len(monthly) + 1)
        chart.add_data(values, titles_from_data=True)
        chart.set_categories(months)
        sheet.add_chart(chart, "G2")
                # column widths
        sheet.column_dimensions["A"].width = 12
        sheet.column_dimensions["B"].width = 10
        sheet.column_dimensions["C"].width = 16
        top = writer.sheets["Top categories"]
        top.column_dimensions["A"].width = 28
        top.column_dimensions["B"].width = 10
        top.column_dimensions["C"].width = 16

        # number format with thousands separator
        for ws in (sheet, top):
            for cell in ws["C"][1:]:
                cell.number_format = "#,##0.00"

    logger.info("Report saved: %s", output_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    conn = sqlite3.connect(DB_PATH)
    create_report(conn)
    conn.close()