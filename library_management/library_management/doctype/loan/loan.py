# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from frappe.model.docstatus import DocStatus 
from datetime import datetime

class Loan(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		book: DF.Link
		date: DF.Date
		due_date: DF.Date | None
		member: DF.Link
		type: DF.Literal["Borrow", "Return"]
	# end: auto-generated types

	def validate(self):
		if self.date and self.type=="Borrow":
			date = datetime.strptime(str(self.date), "%Y-%m-%d").date()
			today = datetime.today().date()
			
			if date < today:
				frappe.throw("Date cannot be in the past.")
	
	def before_submit(self):
		if self.type == "Borrow":
			self.loan_date= self.date
			self.validate_borrow()
			self.validate_maximum_limit()
            # set the book status to be Borrowed
			book = frappe.get_doc("Book", self.book)
			book.status = "Borrowed"
			book.save()
			# calculate and set due date from library setting loan perdion
			loan_period = frappe.db.get_single_value("Library Setting", "loan_period")					
			self.due_date= frappe.utils.add_days(self.date, loan_period or 30)

		elif self.type == "Return":
			self.validate_return()
            # set the book status to be Available
			book = frappe.get_doc("Book", self.book)
			book.status = "Available"
			book.save()

	def validate_borrow(self):
		self.validate_membership()
		book = frappe.get_doc("Book", self.book)
        # book cannot be borrowed if it is already borrowed
		if book.status == "Borrowed":
			frappe.throw("book is already Borrowed by another member")

	def validate_return(self):
		"""
		Main function to validate a book return.
		Calls helper functions for individual validation checks.
		"""
		self.validate_book_availability()  # Ensure the book was borrowed before returning
		self.validate_borrowed_by_member()  # Verify the returning member is the borrower
		self.validate_return_date()  # Ensure return date is after the borrow date
		self.cancel_borrow_transaction()  # Cancel the original borrow transaction


	def validate_book_availability(self):
		"""
		Checks if the book is available.
		A book cannot be returned if it is already marked as 'Available' in the system.
		"""
		book = frappe.get_doc("Book", self.book)
		if book.status == "Available":
			frappe.throw("Book cannot be returned without being Borrowed first")


	def validate_borrowed_by_member(self):
		"""
		Ensures that the book is being returned by the same member who borrowed it.
		If the book was not borrowed by this member, an error is raised.
		"""
		is_borrowed = frappe.db.exists(
			"Loan",
			{
				"book": self.book,
				"member": self.member,
				"type": "Borrow",
				"docstatus": DocStatus.submitted(),
			},
		)
		if not is_borrowed:
			frappe.throw("Book can only be returned by the member who borrowed it")


	def validate_return_date(self):
		"""
		Validates that the return date is after the borrow date.
		If the return date is earlier than the borrow date, an error is raised.
		"""
		is_greater = frappe.db.exists(
			"Loan",
			{
				"book": self.book,
				"member": self.member,
				"type": "Borrow",
				"docstatus": DocStatus.submitted(),
				"date": (">", self.date),
			},
		)
		if is_greater:
			frappe.throw("Return Date must be greater than loan date")


	def cancel_borrow_transaction(self):
		"""
		Cancels the original 'Borrow' transaction before returning the book.
		This ensures that the system does not count the borrowed book against the member's loan limit.
		"""
		borrow_loan = frappe.get_all(
			"Loan",
			filters={
				"book": self.book,
				"member": self.member,
				"type": "Borrow",
				"docstatus": DocStatus.submitted(),
			},
			fields=["name"],
		)

		if not borrow_loan:
			frappe.throw("No corresponding Borrowed Loan found for this Book")

    	# Fetch and cancel the borrowed transaction
		borrow_doc = frappe.get_doc("Loan", borrow_loan[0].name)
		borrow_doc.cancel()


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
                "start_date": ("<=", self.date),
                "expire_date": (">=", self.date),
            },
        )
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")