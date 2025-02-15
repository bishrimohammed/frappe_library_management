# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BookCopy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		available_copies: DF.Int
		number_of_copies: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
