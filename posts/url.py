from django.urls import path

from posts.views import CategoryListAPIView, CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView, \
    SubCategoryListAPIView, SubCategoryCreateAPIView, SubCategoryUpdateAPIView, SubCategoryDeleteAPIView, \
    PostListApiView, PostDetailView, PostCreateView, PostRetrieveUpdateDestroyView, PostImageCreateAPIView, \
    PostImagesListAPIView, PostImageDeleteView

urlpatterns = [
    # Category

    path('category-list/', CategoryListAPIView.as_view()),
    path('catete-category/', CategoryCreateAPIView.as_view()),
    path('edite/<uuid:int>/category/', CategoryUpdateAPIView.as_view()),
    path('delete/<uuid:int>/category/', CategoryDeleteAPIView.as_view()),

    # Sub Category

    path('sub_category-list/', SubCategoryListAPIView.as_view()),
    path('careate-subcategory/', SubCategoryCreateAPIView.as_view()),
    path('edit/<uuid:int>/subcategory/', SubCategoryUpdateAPIView.as_view()),
    path('delete/<uuid:int>/subcategory/', SubCategoryDeleteAPIView.as_view()),

    # post curd

    path('all-list/', PostListApiView.as_view()),
    path('detail/<uuid:id>/', PostDetailView.as_view(), ),
    path('carete-post/', PostCreateView.as_view()),
    path('upadte-delete/<uuid:id>/', PostRetrieveUpdateDestroyView.as_view()),

    # Image C R D

    path('careate-image/', PostImageCreateAPIView.as_view()),
    path('images/<uuid:post_id>/list/', PostImagesListAPIView.as_view()),
    path('images/<uuid:post_id>/delete/', PostImageDeleteView.as_view()),



]
