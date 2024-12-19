from rest_framework import serializers
from posts.models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']
        read_only_fields = ['author']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'comments']

    def to_representation(self, post):
        representation = super().to_representation(post)
        representation['likes_count'] = post.likes.count()
        return representation