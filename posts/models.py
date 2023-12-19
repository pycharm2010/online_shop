from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint

from shred.models import BaseModel


# Create your models here.


class Category(BaseModel):
    title = models.CharField(max_length=256, )
    image = models.ImageField(upload_to='category_image/', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])

    ads_count = models.IntegerField(default=0)


class SubCategory(BaseModel):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categores')

    ads_count = models.IntegerField(default=0)


class Post(BaseModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=256)
    price = models.IntegerField(default=0)
    contact = models.TextField()
    is_top = models.BooleanField(default=False)


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image/')


class PostComment(BaseModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        null=True,
        blank=True
    )


class PostLike(BaseModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='postLikeUnique'
            )
        ]
