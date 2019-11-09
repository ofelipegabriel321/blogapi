from django.urls import path
from .views import *

urlpatterns = [

    path('jsonimporter/', JsonImporter.as_view()),
    path('profiles/', ProfileList.as_view()),
    path('profiles/<int:pk>/', ProfileDetail.as_view()),
    path('profile-posts/', ProfilePostList.as_view()),
    path('profile-posts/<int:pk>/', ProfilePostDetail.as_view()),
    path('posts-comments/', PostCommentList.as_view()),
    path('posts-comments/<int:pk>/', PostCommentDetail.as_view()),
    path('posts/<int:pk>/comments/', CommentList.as_view()),
    path('posts/<int:post_pk>/comments/<int:comment_pk>/', CommentDetail.as_view()),
    path('profile-posts-and-comments/', ProfilePostsAndCommentsList.as_view()),
    path('endpoints/', EndpointsList.as_view()),

]