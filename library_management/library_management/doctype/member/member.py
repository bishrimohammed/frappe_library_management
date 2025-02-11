# Copyright (c) 2025, Bishri Mohammed and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
from datetime import datetime

class Member(Document):
    def validate(self):
        if self.email and not validate_email_address(self.email, throw=False):
            frappe.throw(f"Invalid email address: {self.email}")
      
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'

   
