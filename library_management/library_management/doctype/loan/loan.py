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
		book = frappe.get_doc("Book", self.book)
        # book cannot be returned if it is not borrowed first
		if book.status == "Available":
			frappe.throw("Book cannot be returned without being Borrowed first")
		# check if book is borrowed by the same member who is returning it.
		isborrowed = frappe.db.exists("Loan",{
			"book": self.book,
			"member": self.member,
			"type": "Borrow",
			"docstatus": DocStatus.submitted(),
		})
		if not isborrowed:
			frappe.throw("Book can only be returned by the member who borrowed it")

		# check if loan date is greater than return date
		isGreater = frappe.db.exists("Loan",{
			"book": self.book,
			"member": self.member,
			"type": "Borrow",
			"docstatus": DocStatus.submitted(),
			"date": (">", self.date)			
		})
		if isGreater:
			frappe.throw("Return Date must be greater than loan date")
		
		borrow_loan = frappe.get_all(
			"Loan",
			filters={
				"book": self.book,
				"member": self.member,
				"type": "Borrow",
				"docstatus": DocStatus.submitted()
			},
			fields=["name"]
		)

		if not borrow_loan:
			frappe.throw("No corresponding Borrowed Loan found for this Book")

    	# Cancel the issued transaction
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
                "start_date": ("<", self.date),
                "expire_date": (">", self.date),
            },
        )
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")