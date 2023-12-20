from django.urls import path

from posts.views import PostListApiView, PostCreateView, SubCategoryView

urlpatterns = [
    path('all-list/', PostListApiView.as_view()),
    path('carete-post/', PostCreateView.as_view()),
    path('sub_category-list/', SubCategoryView.as_view())

]
