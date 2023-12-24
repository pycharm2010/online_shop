from rest_framework import serializers

from posts.models import Post, Category, SubCategory, PostLike, Image, PostComment


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'ads_count', 'created_time')


class SubCategorySerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'title', 'category', 'created_time')


class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    post_like_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comment_count')
    me_liked = serializers.SerializerMethodField('get_me_likes')

    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'sub_category',
                  'price',
                  'contact',
                  'is_top',
                  'created_time',
                  'me_liked',
                  'hit_count',
                  'post_like_count',
                  'post_comments_count')

    def get_post_likes_count(self, obj):
        return obj.likes.count()

    def get_post_comment_count(self, obj):
        return obj.comments.count()

    def get_me_likes(self, obj):
        request = self.context.get('request', None)
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
        fields = ('id', 'post', 'image')


class PostCommitSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = serializers.UUIDField(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')


    class Meta:
        model = PostComment
        fields = ('id', 'author', 'post', 'comment', 'parent', 'created_time', 'replies')

    def get_replies(self, obj):
        if obj.child.exists():
            serializer = self.__class__(obj.child.all(), many=True, context=self.context)
            return serializer.data
        else:
            None
