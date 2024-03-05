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
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from .permission import IsOwnerOrReadOnly

# Create your views here.
class MyProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view"}, status=status.HTTP_200_OK)

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    print(permission_classes)
    filterset_class = InventoryFilter

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response({"message": "Item added to inventory successfully"}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid Data'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Item deleted from inventory successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Inventory updated successfully!"
        return Response({'message': message, 'data':serializer.data})



class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

