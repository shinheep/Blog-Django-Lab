from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from ..serializers.comment import CommentSerializer
from ..models.comment import Comment
from django.core.exceptions import PermissionDenied

from api.models import comment 

class CommentsView(APIView):
    def post(self, request):
        # Add the user id as author
        request.data['author'] = request.user.id
        comment = CommentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)  

    def get(self, request):
        # filter for mangos with our user id
        comments = Comment.objects.filter(author=request.user.id)
        data = CommentSerializer(comments, many=True).data
        return Response(data)

class CommentView(APIView):
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        data = CommentSerializer(comment).data
        return Response(data)
    
    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        # Ensure the owner field is set to the current user's ID
        request.data['author'] = request.user.id
        updated_comment = CommentSerializer(comment, data=request.data)
        if updated_comment.is_valid():
            updated_comment.save()
            return Response(updated_comment.data)
        return Response(updated_comment.errors, status=status.HTTP_400_BAD_REQUEST)