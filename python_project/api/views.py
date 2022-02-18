from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models, serializers
from managers import paginators, validators

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
        
        if not data.get('nom') or not data.get('prenom') or not data.get('tel') or not data.get('age'):
            return Response({'message': 'Veuillez remplir les champs requis !', 'success': False}, status=status.HTTP_200_OK)
        elif not validators.validate_phone_number(data.get('tel')):
            return Response({'message': "Veuillez saisir un numéro au format XX-XX-XX-XX-XX ou XX XX XX XX XX ", 'success': False}, status=status.HTTP_200_OK)
        else:
            if data.get('email'):
                if validators.validate_email(data.get('email')):
                    models.Customer.objects.create(
                        nom=data.get('nom'),
                        prenom=data.get('prenom'),
                        age=data.get('age'),
                        tel=data.get('tel'),
                        email=data.get('email')
                    )
                    
                    return Response({'message': "Client bien enregistré.", 'success': True}, status=status.HTTP_200_OK)
                else: return Response({'message': "Veuillez saisir un email valide", 'success': False}, status=status.HTTP_200_OK)
            else:
                models.Customer.objects.create(
                        nom=data.get('nom'),
                        prenom=data.get('prenom'),
                        age=data.get('age'),
                        tel=data.get('tel'),
                    )
                return Response({'message': "Client bien enregistré.", 'success': True}, status=status.HTTP_200_OK)

class CustomerAPIView(APIView):
    def get(self, request, pk):
        if not validators.customer_exists(pk):
            return Response({'message': "Ce client n'existe pas !"}, status=status.HTTP_200_OK)
        else:
            serializer = serializers.CustomerSerializer(models.Customer.objects.get(pk=pk))
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        if not validators.customer_exists(pk):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(pk=pk)
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Modification bien éffectuée.', 'success': True}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not validators.customer_exists(pk):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(pk=pk)
            customer.delete()
            return Response({'message': 'Client bien supprimé !', 'success': True}, status=status.HTTP_200_OK)