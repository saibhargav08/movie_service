from django.db.models import Model, CharField, ForeignKey, TextField, DateTimeField, CASCADE, EmailField, IntegerField, \
    BooleanField

class Movie(Model):
    title = CharField(max_length=100)
    year = CharField(max_length=25)
    genre = CharField(max_length=50)
    country = CharField(max_length=50)
    plot = TextField()

    def __str__(self):
        return self.title

class Comment(Model):
    movie_id = ForeignKey(Movie, on_delete=CASCADE)
    text = TextField()
    timestamp = DateTimeField(auto_now_add=True)

