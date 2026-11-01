"""Input Module: validates and structures the customer's email."""
from datetime import datetime


def build_email(customer_name: str, subject: str, email: str) -> dict:
    customer_name, subject, email = (x.strip() for x in (customer_name, subject, email))
    missing = [label for label, val in
               (("Customer Name", customer_name), ("Subject", subject), ("Email", email))
               if not val]
    if missing:
        raise ValueError("Please fill in: " + ", ".join(missing))
    return {
        "customer_name": customer_name,
        "subject": subject,
        "email": email,
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
