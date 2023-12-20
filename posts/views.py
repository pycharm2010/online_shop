from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from posts.models import Post, SubCategory
from posts.serializers import PostSerializer, SubCategorySerializers
from shred.custom_pagination import CustomPagination
from shred.permission import AdminPermission


# Create your views here.


class PostListApiView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [AdminPermission, ]
    serializer_class = PostSerializer


class SubCategoryView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]


