from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models, serializers
from managers import paginators, validators
from rest_framework.decorators import api_view

# Create your views here.

def index(request):
    return redirect('api:home')

class HomeAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'message': 'Merci pour la consommation de notre API !', 
                'success': True
            }, 
            status=status.HTTP_200_OK
        )


class CustomersAPIView(APIView):
    def get(self, request):
        customers = models.Customer.objects.all()
        serializer = serializers.CustomerSerializer(customers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        message = ''
        success = False
        
        if not data.get('nom') or data.get('nom').isspace() or not data.get('prenom') or data.get('prenom').isspace() or not data.get('tel') or data.get('tel').isspace() or not data.get('age') or not data.get('email') or data.get('email').isspace():
            message = 'Veuillez remplir les champs requis !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        elif not validators.is_email(data.get('email')):
            message = 'Veuillez saisir un email valide !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        elif validators.customer_exists(data.get('email')):
            message = 'Cet email est déjà inscrit !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        else:
            if not validators.validate_phone_number(data.get('tel')):
                message = "Veuillez saisir un numéro au format XX-XX-XX-XX-XX ou XX XX XX XX XX ou XXXXXXXXXX"
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            elif not isinstance(data.get('age'), int) or not data.get('age') >= 15:
                message = 'Veuillez saisir un âge supérieur ou égal à 15 ans'
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            else:
                models.Customer.objects.create(
                        nom=data.get('nom'),
                        prenom=data.get('prenom'),
                        age=data.get('age'),
                        tel=data.get('tel'),
                        email=data.get('email')
                    )
                message = 'Client bien enregistré.'
                success = True
                return Response({'message': message, 'success': success}, status=status.HTTP_201_CREATED)

class CustomerAPIView(APIView):
    def get(self, request, email):
        if not validators.customer_exists(email):
            return Response({'message': "Ce client n'existe pas !"}, status=status.HTTP_200_OK)
        else:
            serializer = serializers.CustomerSerializer(models.Customer.objects.get(email=email))
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, email):
        if not validators.customer_exists(email):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(email=email)
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Modification bien éffectuée.', 'success': True}, status=status.HTTP_200_OK)
    
    def delete(self, request, email):
        if not validators.customer_exists(email):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(email=email)
            customer.delete()
            return Response({'message': 'Client bien supprimé !', 'success': True}, status=status.HTTP_200_OK)