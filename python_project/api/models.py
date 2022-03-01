from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

# Create your models here.
class Base(models.Model):
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, verbose_name='actif')
    
    class Meta:
        abstract = True


class Customer(Base):
    utilisateur = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True, related_name='customer')
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)])
    tel = models.CharField(
        max_length=20, 
        verbose_name='téléphone', 
        unique=True
        )
    activites = models.ManyToManyField('api.Activity', through='Registration')
    
    class Meta:
        verbose_name = 'client'
        db_table = 'client'
        
    def __str__(self):
        return f'{self.nom}, {self.prenom}'
    

class Activity(Base):
    nom = models.CharField(max_length=200, verbose_name='nom')
    age_requis = models.PositiveIntegerField(verbose_name='âge requis')
    description = models.TextField()
    prix = models.PositiveIntegerField(default=0, verbose_name='prix')
    
    class Meta:
        verbose_name = 'activité physique'
        db_table = 'activite'
        
    def __str__(self):
        return f'{self.nom}'


class Registration(Base):
    client = models.ForeignKey(
        'api.Customer', 
        on_delete=models.CASCADE, 
        verbose_name='client'
        )
    activite = models.ForeignKey(
        'api.Activity', 
        on_delete=models.SET_NULL, 
        verbose_name='activité physique',
        null=True
        )
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'inscription'
        db_table = 'inscription'
        constraints = [
            models.UniqueConstraint(fields=['client', 'activite'], name='registration_unique')
        ]
        
    def __str__(self):
        return f'{self.name}'