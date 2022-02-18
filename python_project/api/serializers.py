from rest_framework import serializers
from . import models

class CustomerSerializer(serializers.Serializer):
    class Meta:
        model = models.Customer
        exclude = ['date_ajout', 'date_modification']
        depth = 1


class ActivitySerializer(serializers.Serializer):
    class Meta:
        model = models.Activity
        exclude = ['date_ajout', 'date_modification']


class RegistrationSerializer(serializers.Serializer):
    class Meta:
        model = models.Registration
        exclude = ['date_ajout', 'date_modification']
        depth = 1