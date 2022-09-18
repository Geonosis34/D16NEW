from django.urls import path, include
from .views import *


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   # comments
   path('<int:post_pk>/comments', CommentList.as_view(), name='comment_list'),
   path('<int:post_pk>/create_comment', CommentCreate.as_view(), name='comment_create'),
   path('<int:post_pk>/comments/<int:comment_pk>/accept', CommentAccept.as_view(), name='comment_accept'),
   path('<int:post_pk>/comments/<int:comment_pk>/reject', CommentReject.as_view(), name='comment_reject'),
   path('comments/<int:comment_pk>/delete', CommentDelete.as_view(), name='comment_delete'),
    ]