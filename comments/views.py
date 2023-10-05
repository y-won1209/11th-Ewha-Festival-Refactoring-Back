from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from event.models import *
from .serializers import *
from .permissions import IsAuthorOrReadOnly
# Create your views here.

class CommentView(views.APIView): 
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, event=event)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment
    def delete(self, request, pk, comment_pk):
        comment = self.get_object(pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_200_OK)
