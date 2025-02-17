# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class Membership(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        amended_from: DF.Link | None
        expire_date: DF.Date | None
        full_name: DF.Data | None
        member: DF.Link
        start_date: DF.Date | None
    # end: auto-generated types
    def validate(self):
        if self.expire_date and self.start_date:
            if self.expire_date <= self.start_date:
                frappe.throw("Expire date must be later than start date.")               
        
    
    def before_submit(self):
        exists = frappe.db.exists(
            "Membership",
            {
                "member": self.member,
                "docstatus": DocStatus.submitted(),
                # check if the membership's expire date is later than this membership's start date
                "expire_date": (">", self.start_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")
