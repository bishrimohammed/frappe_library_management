# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _


# def execute(filters: dict | None = None):
# 	"""Return columns and data for the report.

# 	This is the main entry point for the report. It accepts the filters as a
# 	dictionary and should return columns and data. It is called by the framework
# 	every time the report is refreshed or a filter is updated.
# 	"""
# 	columns = get_columns()
# 	data = get_data()

# 	return columns, data


# def get_columns() -> list[dict]:
# 	"""Return columns for the report.

# 	One field definition per column, just like a DocType field definition.
# 	"""
# 	return [
# 		{
# 			"label": _("Column 1"),
# 			"fieldname": "column_1",
# 			"fieldtype": "Data",
# 		},
# 		{
# 			"label": _("Column 2"),
# 			"fieldname": "column_2",
# 			"fieldtype": "Int",
# 		},
# 	]


# def get_data() -> list[list]:
# 	"""Return data for the report.

# 	The report data is a list of rows, with each row being a list of cell values.
# 	"""
# 	return [
# 		["Row 1", 1],
# 		["Row 2", 2],
# 	]


import frappe
from frappe.utils import today

def execute(filters=None):
    columns = [
        {"label": "Loan ID", "fieldname": "name", "fieldtype": "Link", "options": "Loan"},
        {"label": "Member", "fieldname": "member", "fieldtype": "Link", "options": "Member"},
        {"label": "Member Name", "fieldname": "member_name", "fieldtype": "Data"},
        {"label": "Book", "fieldname": "book", "fieldtype": "Link", "options": "Book"},
        {"label": "Book Title", "fieldname": "book_title", "fieldtype": "Data"},
        {"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date"},
        {"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int"}
    ]

    data = frappe.db.sql("""
        SELECT 
            loan.name, 
            loan.member, 
            member.full_name AS member_name,            
            book.title AS book_title,
            loan.due_date,
            DATEDIFF(%s, loan.due_date) AS days_overdue
        FROM `tabLoan` AS loan
        LEFT JOIN `tabMember` AS member ON loan.member = member.name
        LEFT JOIN `tabBook` AS book ON loan.book = book.name
        WHERE loan.docstatus = 1
        AND loan.type = 'Borrow'
        AND loan.due_date < %s
        ORDER BY loan.due_date ASC
    """, (today(), today()), as_dict=True)

    return columns, data
