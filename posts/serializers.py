from rest_framework import serializers

from posts import models
from posts.models import Post, Category, SubCategory, PostLike, Image, PostComment, Purchase
from users.serializers import UserSerializer


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    add_count = serializers.SerializerMethodField('get_all_category')

    class Meta:
        model = Category
        fields = ("id", "title", "image", "add_count", "created_time")

    def get_all_category(self, obj):
        return obj.categores.count()


class SubCategorySerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    add_count = serializers.SerializerMethodField('get_all_category')

    class Meta:
        model = SubCategory
        fields = ("id", "title", "category", 'add_count', "created_time")

    def get_all_category(self, obj):
        return obj.sub_categoryes.count()


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    post_like_count = serializers.SerializerMethodField("get_post_likes_count")
    post_comments_count = serializers.SerializerMethodField("get_post_comment_count")
    me_liked = serializers.SerializerMethodField("get_me_likes")
    author = UserSerializer(read_only=True)



    class Meta:
        model = Post
        fields = (
            "author",
            "id",
            "title",
            "sub_category",
            "price",
            "contact",
            "is_top",
            "created_time",
            "me_liked",
            "post_like_count",
            "post_comments_count",

        )


    def get_post_likes_count(self, obj):
        return obj.likes.count()

    def get_post_comment_count(self, obj):
        return obj.comments.count()

    def get_me_likes(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            try:
                like = PostLike.objects.get(post=obj, author=request.user)
                return True
            except PostLike.DoesNotExist:
                return False
        return False


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "post", "image")


class PostCommitSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField("get_replies")

    class Meta:
        model = PostComment
        fields = (
            "id",
            "author",
            "comment",
            "post",
            "parent",
            "created_time",
            "replies",
        )

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(
                obj.child.all(), many=True, context=self.context
            )
            return serializer.data
        else:
            None


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ("id", "author", "post")


class PurchaseSerializer(serializers.ModelSerializer):
    model = Purchase
    fields = '__all__'
