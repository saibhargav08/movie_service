from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Case, F, Sum, When
from django.db.models.functions import DenseRank, Coalesce
from django.db.models.fields import IntegerField
from django.db.models.expressions import Window

from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Movie, Comment
from .serializers import MovieSerializer, MovieRequestSerializer, CommentSerializer




import datetime


class MoviesView(ListModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'genre')
    ordering_fields = ('title', 'year')

    def create(self, request, *args, **kwargs):
        request = MovieRequestSerializer(data=request.data)

        if not request.is_valid():
            return Response(request.errors, status=HTTP_400_BAD_REQUEST)

        movie = Movie(
            title=request.data['title'],
            year=request.data['year'],
            genre=request.data['genre'],
            country=request.data['country'],
            plot=request.data['plot']
        )

        if Movie.objects.filter(title=request.data['Title']).exists():
            return Response({'error': 'Movie already exists'}, status=HTTP_409_CONFLICT)

        try:
            movie.save()
        except:
            return Response({'error': ''}, status=HTTP_409_CONFLICT)

        return Response(request.data, status=HTTP_201_CREATED)


class CommentsView(ListModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Optionally filter to `movie_id` passed in querystring."""
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise exceptions.ValidationError({
                    'movie_id': [
                        'Incorrect movie_id type. Expected int.',
                    ],
                })
            movie = get_object_or_404(Movie, id=movie_id)
            queryset = queryset.filter(movie_id=movie)
        return queryset


class TopView(APIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request):
        start = str(request.data.get('start'))
        end = str(request.data.get('end'))

        if not start or not end:
            return Response({'msg': 'Missing params'}, status=HTTP_400_BAD_REQUEST)

        try:
            start = datetime.datetime.strptime(start, '%d-%m-%Y')
            end = datetime.datetime.strptime(end, '%d-%m-%Y')
        except:
            return Response({'msg': 'Invalid date format, expected DD-MM-YYYY'}, status=HTTP_400_BAD_REQUEST)

        movies_query = Movie.objects.annotate(
            comments=Coalesce(
                Sum(Case(
                    When(comment__timestamp__range=[start, end], then=1),
                    output_field=IntegerField()
                )),
                0
            ),
            rank=Window(
                expression=DenseRank(),
                order_by=F('comments').desc()
            )
        ).order_by('-comments', 'id')

        movies = [{
            'id': movie.id,
            'comments': movie.comments,
            'rank': movie.rank
        } for movie in movies_query
        ]

        return Response(movies)
