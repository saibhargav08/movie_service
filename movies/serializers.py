from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer, CharField
from .models import Movie, Comment


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'genre', 'country', 'plot')
        read_only_fields = ('year', 'genre', 'country', 'plot')


class MovieRequestSerializer(Serializer):
    """Checking if POST request is valid """
    title = CharField(max_length=100, required=True)

    def create(self, data):
        return {'title': data.get('title')}

    def update(self, instance, data):
        instance['title'] = data.get('title', instance['title'])


class CommentSerializer(ModelSerializer):
    movie_id = PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'text')


