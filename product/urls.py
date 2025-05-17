from django.urls import path
from .views import (
    CategoryListCreate, CategoryDetail,
    ProductListCreate, ProductDetail, ProductReviewsList,
    ReviewListCreate, ReviewDetail,
    RegisterView, ConfirmView
)

urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', ProductListCreate.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/reviews/', ProductReviewsList.as_view(), name='product-reviews'),
    path('reviews/', ReviewListCreate.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/confirm/', ConfirmView.as_view(), name='confirm'),
]