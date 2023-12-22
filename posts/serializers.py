from rest_framework import serializers

from posts.models import Post, Category, SubCategory, PostLike


class CategorySerializers(serializers.ModelSerializer):
    model = Category
    fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'title')


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


