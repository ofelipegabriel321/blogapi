from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class JsonImporter(APIView):

    def post(self, request, format=None):
        posts = request.data['posts']
        comments = request.data['comments']
        profiles = request.data['users']

        for profile in profiles :
            profile_serializer = ProfileSerializer(data=profile)
            if profile_serializer.is_valid():
                profile_serializer.save()

        for post in posts:
            post_serializer = PostSerializer(data=post)
            if post_serializer.is_valid():
                post_serializer.save()

        for comment in comments:
            comment_serializer = CommentSerializer(data=comment)
            if comment_serializer.is_valid():
                comment_serializer.save()


class ProfileList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_serializer = ProfileSerializer(profiles, many=True)
        return Response(profile_serializer.data)

    def post(self, request, format=None):
        profile = request.data
        profile_serializer = ProfileSerializer(data=profile)
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_serializer = ProfileSerializer(profile, data=request.data)
        
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_200_OK)


class ProfilePostList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_post_serializer = ProfilePostSerializer(profiles, many=True)
        return Response(profile_post_serializer.data)


class ProfilePostDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_post_serializer = ProfilePostSerializer(profile)
        return Response(profile_post_serializer.data)


class PostCommentList(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        post_serializer = PostCommentSerializer(posts, many=True)
        return Response(post_serializer.data)


class PostCommentDetail(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        post_serializer = PostCommentSerializer(post)
        return Response(post_serializer.data)


class CommentList(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        comment_serializer = CommentSerializer(post.comments, many=True)
        return Response(comment_serializer.data)

    def post(self, request, pk, format=None):
        comment = request.data
        comment['postId'] = pk
        comment_serializer = CommentSerializer(data=comment)
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    def get_comment(self, post_pk, comment_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            try:
                comment =  post.comments.get(pk=comment_pk)
                return comment
            except Comment.DoesNotExist:
                raise Http404
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, comment_pk, format=None):
        comment = self.get_comment(post_pk,comment_pk)
        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data)

    def put(self, request, post_pk, comment_pk, format=None):
        comment = self.get_comment(post_pk,comment_pk)
        comment_data = request.data
        comment_data['postId'] = post_pk
        comment_serializer = CommentSerializer(comment, data=comment_data)
        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk, comment_pk, format=None):
        comment_serializer = CommentSerializer(data=request.data)
        comment = self.get_comment(post_pk,comment_pk)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class ProfilePostsAndCommentsList(APIView):

    def get(self, request, format=None):
        response = []
        profiles = Profile.objects.all()
        for profile in profiles:
            profile_data = {}
            
            profile_data['id'] = profile.id
            profile_data['name'] = profile.name

            count_posts = 0
            count_comments = 0

            for post in profile.posts.all():
                count_posts += 1
                for comment in post.comments.all():
                    count_comments += 1

            profile_data['total_posts'] = count_posts
            profile_data['total_comments'] = count_comments

            response.append(profile_data)

        return Response(response)


class EndpointsList(APIView):

    def get(self, request, format=None):
        root_url = 'http://ofelipegabriel321.pythonanywhere.com//'
        data = {
                'jsonimporter': root_url + 'jsonimporter/',
                'profiles-list': root_url + 'profiles',
                'profile-posts-list': root_url + 'profile-posts',
                'posts-comments-list': root_url + 'posts-comments',
                'profile-posts-and-comments-list': root_url + 'profile-posts-and-comments'
        }
        
        return Response(data)
