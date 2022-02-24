from rest_framework import serializers
from .models import Customer, Activity, Registration

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['date_ajout', 'date_modification','status', 'activites']
        depth = 1


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ['date_ajout', 'date_modification']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        exclude = ['date_ajout', 'date_modification']
        depth = 1
