from django.http import JsonResponse,HttpResponse
from .models import Product,Category,Brand,Inventory
from .serializers import ProductSerialaizer,InventorySerializer,InventoryFilter,InventorySerializerWithProduct
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication

def maketoken(request):
        admin_user = User.objects.get(username='admin')
        print(admin_user)
        # Create or retrieve the token for the user
        token, created = Token.objects.get_or_create(user = admin_user)

        # Retrieve the token key
        print(token.key)
        return HttpResponse("cool")


@api_view(['GET','POST'])

def products(request):
    
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerialaizer(products, many=True)
        return JsonResponse({'products':serializer.data})
    permission_classes = ([IsAuthenticated])
    if request.method == 'POST':
        serializer = ProductSerialaizer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)