from django.urls import path

from posts.views import PostListApiView, PostCreateView, SubCategoryView, PostDetailView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('sub_category-list/', SubCategoryView.as_view()),
    # post curd
    path('all-list/', PostListApiView.as_view()),
    path('list/<uuid:id>/', PostDetailView.as_view(), ),
    path('carete-post/', PostCreateView.as_view()),
    path('upadte-delete/<uuid:id>/', PostRetrieveUpdateDestroyView.as_view())

]
