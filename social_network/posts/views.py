from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment, Like
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['post_id'],
                        author=self.request.user)


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if not Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.create(post=post, author=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.filter(post=post, author=request.user).delete()
        return Response(status=status.HTTP_200_OK)