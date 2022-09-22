from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .permissions import NewsPermission, CommentPermission, StatusPermission

from .models import News, Comment, Status, CommentStatus, NewsStatus
from .serializers import NewsSerializer, CommentSerializer, StatusSerializer
from account.models import User, Author


class NewsListCreateAPIView(ListCreateAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NewsPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class NewsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NewsPermission, ]


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CommentPermission, ]

    def get_queryset(self):
        return self.queryset.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news=get_object_or_404(News, id=self.kwargs['news_id'])
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [CommentPermission, ]


class StatusListCreateAPIView(ListCreateAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [StatusPermission, ]


class StatusRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [StatusPermission, ]


class NewsStatusLike(APIView):
    def get(self, request, news_id, status_slug):
        news = get_object_or_404(News, id=news_id)
        news_status = get_object_or_404(Status, slug=status_slug)
        try:
            like_dislike = NewsStatus.objects.create(news=news, author=request.user.author, status=news_status)
        except IntegrityError:
            like_dislike = NewsStatus.objects.get(news=news, author=request.user.author)
            if like_dislike.status == news_status:
                like_dislike.status = None
            else:
                like_dislike.status == news_status
            like_dislike.save()
            data = {"error": "You already added status"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Status added"}
            return Response(data, status=status.HTTP_201_CREATED)


# class CommentStatusLike(APIView):
#     def get(self, request, news_id, comment_id, status_slug):
#         comment = get_object_or_404(Comment, id=comment_id)
#         comment_status = get_object_or_404(Status, slug=status_slug)
#         news = get_object_or_404(News, id=news_id)
#         try:
#             like_dislike = CommentStatus.objects.create(comment=comment, author=request.user.author, status=news_status)
#         except IntegrityError:
#             like_dislike = CommentStatus.objects.get(comment=comment, author=request.user.author)
#             if like_dislike.status == comment_status:
#                 like_dislike.status = None
#             else:
#                 like_dislike.status == comment_status
#             like_dislike.save()
#             data = {"error": "You already added status"}
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             data = {"message": "Status added"}
#             return Response(data, status=status.HTTP_201_CREATED)
#
# class CommentStatusLike(APIView):
#     def get_queryset(self):
#         news_queryset = News.objects.all()
#         comment_id = self.request.query_params.get('comment_id')
#
#
        # comment_queryset = Comment.objects.filter(user__username=user)


        # if comment_id:
        #
        # search = self.request.query_params.get('search')


