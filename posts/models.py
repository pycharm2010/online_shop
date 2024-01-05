import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint
from hitcount.models import HitCountMixin, HitCount
from django.contrib.sessions.models import Session
from shred.models import BaseModel


# Create your models here.


class Category(BaseModel):
    title = models.CharField(max_length=256, unique=True)
    image = models.ImageField(
        upload_to="category_image/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "heic", "heif"]
            )
        ],
    )



class SubCategory(BaseModel):
    title = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categores"
    )

    ads_count = models.IntegerField(default=0)

    def update_ads_count(self):
        self.ads_count = self.post_set.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_ads_count()

    def __str__(self):
        return f"SubCategory count {self.ads_count}"


class Post(BaseModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_categoryes')
    title = models.CharField(max_length=256)
    price = models.IntegerField(default=0)
    contact = models.TextField()
    is_top = models.BooleanField(default=False)
    add_count = models.IntegerField(default=0)


class Image(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        editable=False,
    )
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="post_image/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "heic", "heif"]
            )
        ],
    )


class PostComment(BaseModel):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child", null=True, blank=True
    )

    def __str__(self):
        return f"comment by {self.author}"


class PostLike(BaseModel):
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    like_count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["author", "post"], name="postLikeUnique")
        ]

    def __str__(self):
        return f"like by {self.author}"


class Purchase(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
