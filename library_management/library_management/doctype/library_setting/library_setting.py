# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LibrarySetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		loan_period: DF.Int
		maximum_number_of_borrow_book: DF.Int
	# end: auto-generated types

	pass
