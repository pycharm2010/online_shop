from typing import List, Type

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, SubCategory, Image, Category, PostComment
from posts.serializers import PostSerializer, SubCategorySerializers, ImageSerializer, CategorySerializers, \
    PostCommitSerializer
from shred.custom_pagination import CustomPagination
from shred.permission import AdminPermission

from hitcount.views import View


# Category CRUD API View
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny, ]


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny, ]


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny, ]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category.save()
        return Response({

            "success": True,
            "code": status.HTTP_200_OK,
            "message": "Sub category successfully updated",
            "data": serializer.data
        })


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny, ]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully delete"
            }
        )


# Sub Category CRUD API View

class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]


class SubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]


class SubCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category.save()
        return Response({

            "success": True,
            "code": status.HTTP_200_OK,
            "message": "Sub category successfully updated",
            "data": serializer.data
        })


class SubCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully delete"
            }
        )


# Post Image CRUD API View
class PostListApiView(generics.ListAPIView, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [AdminPermission, ]
    serializer_class = PostSerializer

    lookup_field = 'id'

    def get_queryset(self):
        return Post.objects.all()


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [AdminPermission, ]
    serializer_class = PostSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Post successfully updated",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post successfully delete"
            }
        )


# Image CRUD API View
class PostImagesListAPIView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        return post.images.all()


class PostImageCreateAPIView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny, ]


class PostImageDeleteView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = ImageSerializer
    lookup_field = 'id'  # Agar primary key 'id' bo'lsa

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully deleted"
            }
        )


class PostCommitListAPIView(generics.ListAPIView):
    serializer_class = PostCommitSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset


