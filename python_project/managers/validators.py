from django.core.validators import validate_email
import re
from api import models

def is_email(email: str):
    
    try:
        validate_email(email)
        return True
    except:
        return False

def validate_phone_number(number: str):
    if not re.fullmatch('(^\d{2}([ -]\d{2}){4}$)|(^\d{10}$)', number):
        return False
    else: return True

def customer_exists(email: str):
    try:
        customer = models.Customer.objects.get(email=email)
        return True
    except models.Customer.DoesNotExist:
        return False