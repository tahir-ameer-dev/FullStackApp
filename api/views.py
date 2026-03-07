from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(user)
            print(movie.title)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                self.response = {'message': 'Rating Updated', 'result':serializer.data}
                return Response(self.response, status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                self.response = {'message': 'Rating Created', 'result':serializer.data}
                return Response(self.response, status=status.HTTP_200_OK)

        else:
            self.response = {'message': 'You Need to Provide Stars'}
            return Response(self.response, status.HTTP_200_OK)
            
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication, )
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        self.response = {'message': 'You Cant Update like that'}
        return Response(self.response, status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        self.response = {'message': 'You Cant Create like that'}
        return Response(self.response, status.HTTP_200_OK)