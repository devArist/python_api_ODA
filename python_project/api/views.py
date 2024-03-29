from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models, serializers
from managers import paginators, validators
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
import re, requests

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
        
        if not data.get('nom') or data.get('nom').isspace() or not data.get('prenom') or data.get('prenom').isspace() or not data.get('tel')  or not data.get('age') or not data.get('email') or data.get('email').isspace() or not data.get('pwd1') or data.get('pwd1').isspace() or not data.get('pwd2') or data.get('pwd2').isspace():
            message = 'Veuillez remplir les champs requis !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        elif not validators.is_email(data.get('email')):
            message = 'Veuillez saisir un email valide !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        elif validators.customer_exists(data.get('email')):
            message = 'Cet email est déjà inscrit !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        elif data.get('pwd1') != data.get('pwd2'):
            message = 'Les mots de passe ne sont pas identiques !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        else:
            if not re.fullmatch('^[0-9]{2}[0-9]{8}$', data.get('tel')):
                message = "Veuillez saisir un numéro au format XXXXXXXXXX"
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            elif not isinstance(data.get('age'), int) or not data.get('age') >= 15:
                message = 'Veuillez saisir un âge supérieur ou égal à 15 ans'
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            elif validators.customer_exists(data.get('tel')):
                message = 'Un client existe déjà avec ce numéro !'
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            else:
                user = get_user_model().objects.create(
                    username=data.get('email'),
                    email=data.get('email'),
                    last_name=data.get('nom'),
                    first_name=data.get('prenom')
                    )
                user.set_password(data.get('pwd1'))
                user.save()
                models.Customer.objects.create(
                        utilisateur=user,
                        age=data.get('age'),
                        tel=data.get('tel')
                    )
                message = 'Client bien enregistré.'
                success = True
                return Response({'message': message, 'success': success}, status=status.HTTP_201_CREATED)

class CustomerAPIView(APIView):
    def get(self, request, pk):
        if not validators.customer_exists_with_id(pk):
            return Response({'message': "Ce client n'existe pas !"}, status=status.HTTP_200_OK)
        else:
            serializer = serializers.CustomerSerializer(models.Customer.objects.get(pk=pk))
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        if not validators.customer_exists_with_id(pk):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(pk=pk)
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Modification bien éffectuée.', 'success': True}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not validators.customer_exists_with_id(pk):
            return Response({'message': "Ce client n'existe pas !", "success": False}, status=status.HTTP_200_OK)
        else:
            customer = models.Customer.objects.get(pk=pk)
            customer.delete()
            return Response({'message': 'Client bien supprimé !', 'success': True}, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
def signin(request):
    url = "http://127.0.0.1:8000/api/token/"
    message = ''
    success = False
    if request.method == 'GET':
        return Response({'message':'Bienvenue sur la page de connexion', 'success':True})
    elif request.method == 'POST':
        data = request.data
        if not data.get('email') or data.get('email').isspace() or not data.get('password') or data.get('password').isspace():
            message = 'Veuillez remplir les champs vides !'
            return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
        else:
            user = authenticate(request, username=data.get('email'), password=data.get('password'))
            if not user:
                message = 'Email ou mot de passe incorrect !'
                return Response({'message': message, 'success': success}, status=status.HTTP_200_OK)
            else:
                res = requests.post(url, {'username':data.get('email'), 'password':data.get('password')}).json()
                return Response(res, status=status.HTTP_200_OK)