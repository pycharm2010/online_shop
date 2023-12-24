from django.urls import path

from posts.views import (
    CategoryListAPIView,
    CategoryCreateAPIView,
    SubCategoryListAPIView,
    SubCategoryCreateAPIView,
    PostListApiView,
    PostCreateView,
    PostRetrieveUpdateDestroyView,
    PostImageCreateAPIView,
    PostImagesListAPIView,
    PostImageDeleteView,
    CategoryRetrieveUpdateDestroyAPIView,
    SubCategoryRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    PostLikeListAPIView,
    PostLikeAPIView,
)

urlpatterns = [
    # Category
    path("category-list/", CategoryListAPIView.as_view()),
    path("catete-category/", CategoryCreateAPIView.as_view()),
    path("<uuid:int>/category/", CategoryRetrieveUpdateDestroyAPIView.as_view()),
    # Sub Category
    path("sub_category-list/", SubCategoryListAPIView.as_view()),
    path("careate-subcategory/", SubCategoryCreateAPIView.as_view()),
    path("<uuid:int>/subcategory/", SubCategoryRetrieveUpdateDestroyAPIView.as_view()),
    # post curd
    path("list/", PostListApiView.as_view()),
    path("carete-post/", PostCreateView.as_view()),
    path("<uuid:id>/", PostRetrieveUpdateDestroyView.as_view()),
    # Image C R D
    path("careate-image/", PostImageCreateAPIView.as_view()),
    path("images/<uuid:post_id>/list/", PostImagesListAPIView.as_view()),
    path("images/<uuid:post_id>/delete/", PostImageDeleteView.as_view()),
    # Post Comment CRUD
    path("comment/", CommentListCreateAPIView.as_view()),
    path("<uuid:pk>/like", PostLikeListAPIView.as_view()),
    path("<uuid:pk>/create-delete-like/", PostLikeAPIView.as_view()),
]
