# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Book(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		author: DF.Data | None
		isbn: DF.Data | None
		publish_date: DF.Date | None
		status: DF.Literal["Available", "Borrowed"]
		title: DF.Data
	# end: auto-generated types

	pass
