from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = User.objects.get(id=1)
            print(movie.title)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                self.response = {'message': 'Object Updated'}
            except:
                Rating.objects.create(user=user, movie=movie, stars=stars)
                self.response = {'message': 'Object Created'}
            return Response(self.response, status.HTTP_200_OK)
        else:
            self.response = {'message': 'You Need to Provide Stars'}
            return Response(self.response, status.HTTP_200_OK)
            
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer