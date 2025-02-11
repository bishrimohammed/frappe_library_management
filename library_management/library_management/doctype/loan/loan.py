# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Loan(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		book: DF.Link
		due_date: DF.Date | None
		loan_date: DF.Date | None
		member: DF.Link
		return_date: DF.Date | None
		status: DF.Literal["Borrowed", "Returned"]
	# end: auto-generated types

	pass
