from typing import List, Type

from rest_framework import generics, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, SubCategory, Image, Category, PostComment, PostLike
from posts.serializers import (
    PostSerializer,
    SubCategorySerializers,
    ImageSerializer,
    CategorySerializers,
    PostCommitSerializer,
    PostLikeSerializer,
)
from shred.custom_pagination import CustomPagination
from shred.permission import AdminPermission


# Category CRUD API View
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [
        AllowAny,
    ]


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated, AdminPermission]


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated, AdminPermission]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Sub category successfully updated",
                "data": serializer.data,
            }
        )

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully delete",
            }
        )


# Sub Category CRUD API View


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [
        AllowAny,
    ]


class SubCategoryCreateAPIView(generics.CreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [IsAuthenticated, AdminPermission]


class SubCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [IsAuthenticated, AdminPermission]
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Sub category successfully updated",
                "data": serializer.data,
            }
        )

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully delete",
            }
        )


# Post Image CRUD API View
class PostListApiView(generics.ListAPIView, ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        AllowAny,
    ]
    pagination_class = CustomPagination


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [
        AdminPermission,
    ]
    serializer_class = PostSerializer
    lookup_field = "id"

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
                "data": serializer.data,
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post successfully delete",
            }
        )


# Image CRUD API View
class PostImagesListAPIView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(pk=post_id)
        return post.images.all()


class PostImageCreateAPIView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [
        AllowAny,
    ]


class PostImageDeleteView(generics.DestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = ImageSerializer
    lookup_field = "id"  # Agar primary key 'id' bo'lsa

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Post image successfully deleted",
            }
        )


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = PostComment.objects.all()
    serializer_class = PostCommitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeListAPIView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return PostLike.objects.filter(post_id=post_id)


class PostLikeAPIView(APIView):

    def post(self, request, pk):
        try:
            post_like = PostLike.objects.get(
                author=self.request.user,
                post_id=pk,
            )
            post_like.delete()
            data = {
                "success": True,
                "message": "Post like muvaffaqiyatli o'chirildi...",
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author=self.request.user,
                post_id=pk,
            )
            serializer = PostLikeSerializer(post_like)

            data = {
                "success": True,
                "message": "Post like muvaffaqiyatli qo'shildi...",
                "data": serializer.data,
            }

            return Response(data, status=status.HTTP_201_CREATED)
