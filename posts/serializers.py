from rest_framework import serializers

from .models import Post, Comment


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        slug_field='pk',
        many=True,
        queryset=Comment.objects.all(),
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'text',
            'created',
            'updated',
            'author',
            'image',
            'comments',
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        read_only_fields = ["id", "created", "updated", "author"]
        fields = "__all__"


class CommentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ["id", "created", "updated", "author"]
        fields = "__all__"


class CommentUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ["id", "created", "updated", "author", "post"]
        fields = "__all__"
