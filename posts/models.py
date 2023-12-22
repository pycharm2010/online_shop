from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint
from hitcount.models import HitCountMixin, HitCount
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from shred.models import BaseModel


# Create your models here.


class Category(BaseModel):
    title = models.CharField(max_length=256, unique=True)
    image = models.ImageField(upload_to='category_image/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])

    ads_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # SubCategory obyekti saqlanayotganda ads_count ni yangilab qo'yamiz
        self.ads_count = self.post_set.count()
        super().save(*args, **kwargs)


class SubCategory(BaseModel):
    title = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categores')

    ads_count = models.IntegerField(default=0)

    def update_ads_count(self):
        self.ads_count = self.post_set.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_ads_count()

    def __str__(self):
        return f"SubCategory count {self.ads_count}"


class Post(BaseModel, HitCountMixin):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    price = models.IntegerField(default=0)
    contact = models.TextField()
    is_top = models.BooleanField(default=False)
    hit_count = models.BigIntegerField(default=0)

    def update_hit_count(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        if not Session.objects.filter(session_key=session_key).exists():
            super().update_hit_count(request)

    @property
    def calculate_hit_count(self):
        # Post uchun yangi HitCount obyekti yaratish
        hit_count, created = HitCount.objects.get_or_create(content_type=None, object_pk=self.pk)
        return hit_count


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_image/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])



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

    def __str__(self):
        return f"comment by {self.author}"


class PostLike(BaseModel):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like_count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='postLikeUnique'
            )
        ]

    def __str__(self):
        return f"like by {self.author}"


