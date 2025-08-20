from django.urls import path

from .views import (
    PodcastSearchView,
    PodcastDetailView,
    PodcastEpisodesView
)


urlpatterns = [
    path("search", PodcastSearchView.as_view(), name="podcasts-search"),
    path("<str:showId>", PodcastDetailView.as_view(), name="podcasts-detail"),
    path("<str:showId>/episodes", PodcastEpisodesView.as_view(), name="podcasts-episodes"),
]
