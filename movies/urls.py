from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from .views import MoviesView, CommentsView, TopView

router = SimpleRouter()
router.register(r'movies', MoviesView)
router.register(r'comments', CommentsView, base_name='comments')
urlpatterns = [
    url(r'top', TopView.as_view())
]

urlpatterns += router.urls
