# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

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

	def validate(self):
		if self.isbn and not self.is_valid_isbn(self.isbn):
			frappe.throw("Invalid ISBN. It must be either 10 or 13 characters long.")
		if self.publish_date:
			publish_date = datetime.strptime(str(self.publish_date), "%Y-%m-%d").date()
			today = datetime.today().date()

			if publish_date > today:
				frappe.throw("Publish Date cannot be in the future.")
			
	# check isbn is already exist
	def before_submit(self):
		if self.isbn:
			# check if isbn already exists

			existing = frappe.db.exists("Book", {"isbn": self.isbn})
			if existing:
				frappe.throw("ISBN already exists.")

	def is_valid_isbn(self, isbn):
		return len(isbn) in [10, 13] and isbn.isdigit()