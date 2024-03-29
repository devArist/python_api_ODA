from django.core.validators import validate_email
import re
from api import models
from django.db.models import Q
from django.contrib.auth import get_user_model

def is_email(email: str):
    
    try:
        validate_email(email)
        return True
    except:
        return False

def validate_phone_number(number: str):
    if re.fullmatch("^[0-9]{2}[0-9]{8}$", number):
        return True
    else: return False

def customer_exists(data: str):
    return True if models.Customer.objects.filter(tel=data).exists() or get_user_model().objects.filter(email=data).exists() else False

def customer_exists_with_id(pk: int):
    try:
        models.Customer.objects.get(pk=pk)
        return True
    except models.Customer.DoesNotExist:
        return False