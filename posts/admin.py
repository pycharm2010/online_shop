from django.contrib import admin

from posts.models import Post, Category, SubCategory, PostComment, PostLike, Image, Purchase

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(Image)
admin.site.register(Purchase)
