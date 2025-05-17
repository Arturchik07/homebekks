from rest_framework import serializers
from .models import Category, Product, Review, ConfirmationCode
from django.contrib.auth.models import User
from django.db.models import Count

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryWithProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'average_rating']

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.stars for review in reviews) / len(reviews)
        return 0

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        import random
        code = ''.join(random.choices('0123456789', k=6))
        ConfirmationCode.objects.create(user=user, code=code)
        return user

class ConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)