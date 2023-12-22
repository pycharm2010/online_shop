from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, SubCategory
from posts.serializers import PostSerializer, SubCategorySerializers
from shred.custom_pagination import CustomPagination
from shred.permission import AdminPermission

from hitcount.views import View


# Create your views here.

class SubCategoryView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [AllowAny, ]


class PostListApiView(generics.ListAPIView, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AdminPermission, ]
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


class ImageAPIView(generics.ListAPIView):
    pass