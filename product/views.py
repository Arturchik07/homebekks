from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Product, Review, ConfirmationCode
from .serializers import (
    CategorySerializer, CategoryWithProductCountSerializer,
    ProductSerializer, ProductWithReviewsSerializer,
    ReviewSerializer, RegisterSerializer, ConfirmSerializer
)
from django.db.models import Count

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryWithProductCountSerializer
    permission_classes = [IsAuthenticated]

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductReviewsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductWithReviewsSerializer(products, many=True)
        return Response(serializer.data)

class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created. Please confirm your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                confirmation = ConfirmationCode.objects.get(code=code)
                user = confirmation.user
                user.is_active = True
                user.save()
                confirmation.delete()
                return Response({"message": "Account confirmed."}, status=status.HTTP_200_OK)
            except ConfirmationCode.DoesNotExist:
                return Response({"error": "Invalid code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)