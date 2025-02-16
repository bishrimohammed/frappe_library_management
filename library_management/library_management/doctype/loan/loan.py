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

		amended_from: DF.Link | None
		book: DF.Link
		date: DF.Date | None
		member: DF.Link
		type: DF.Literal["Borrow", "Return"]
	# end: auto-generated types

	def before_submit(self):
		if self.type == "Borrow":
			self.validate_borrow()
			self.validate_maximum_limit()
            # set the book status to be Borrowed
			book = frappe.get_doc("Book", self.book)
			book.status = "Borrowed"
			book.save()

		elif self.type == "Return":
			self.validate_return()
            # set the book status to be Available
			book = frappe.get_doc("Book", self.book)
			book.status = "Available"
			book.save()
	# check if 
	# def before_save(self):


	def validate_borrow(self):
		self.validate_membership()
		book = frappe.get_doc("Book", self.book)
        # book cannot be borrowed if it is already borrowed
		if book.status == "Borrow":
			frappe.throw("book is already Borrowed by another member")

	def validate_return(self):
		book = frappe.get_doc("Book", self.book)
        # book cannot be returned if it is not borrowed first
		if book.status == "Available":
			frappe.throw("Book cannot be returned without being Borrowed first")

	def validate_maximum_limit(self):
		max_books = frappe.db.get_single_value("Library Setting", "maximum_number_of_borrow_book")
		count = frappe.db.count(
            "Loan",
            {
                "member": self.member,
                "type": "Borrow",
                "docstatus": DocStatus.submitted(),
            },
        )
		if count >= max_books:
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

