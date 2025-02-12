# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from frappe.model.docstatus import DocStatus 


class Loan(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		book: DF.Link
		loan_date: DF.Date | None
		member: DF.Link
		return_date: DF.Date | None
		type: DF.Literal["Borrow", "Return"]
	# end: auto-generated types

	def before_submit(self):
		if self.type == "Borrow":
			self.validate_borrow()
			self.validate_maximum_limit()
            # set the article status to be Issued
			book = frappe.get_doc("Book", self.book)
			book.status = "Borrowed"
			book.save()

		elif self.type == "Return":
			self.validate_return()
            # set the article status to be Available
			book = frappe.get_doc("Book", self.book)
			book.status = "Available"
			book.save()

	def validate_borrow(self):
		self.validate_membership()
		book = frappe.get_doc("Book", self.book)
        # book cannot be issued if it is already issued
		if book.status == "Borrow":
			frappe.throw("book is already Borrowed by another member")

	def validate_return(self):
		book = frappe.get_doc("Book", self.book)
        # book cannot be returned if it is not issued first
		if book.status == "Available":
			frappe.throw("Book cannot be returned without being Borrowed first")

	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value("Library Setting", "max_articles")
		count = frappe.db.count(
            "Loan",
            {
                "member": self.member,
                "type": "Borrow",
                "docstatus": DocStatus.submitted(),
            },
        )
		if count >= max_articles:
			frappe.throw("Maximum limit reached for Borrowing books")

	def validate_membership(self):
        # check if a valid membership exist for this library member
		valid_membership = frappe.db.exists(
            "Membership",
            {
                "member": self.member,
                "docstatus": DocStatus.submitted(),
                "start_date": ("<", self.date),
                "expire_date": (">", self.date),
            },
        )
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")

