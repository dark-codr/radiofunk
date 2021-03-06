from django.urls import path

from radio_funk.podcast.views import (
    create_playlist,
    podcast_detail,
    podcast_list,
    podcast_like,
    podcast_unlike,
    remove_favorite,
    playlist_detail,
    delete_playlist,
    delete_podcast,
)

app_name = "podcast"
urlpatterns = [
    path("", view=podcast_list, name="podcasts"),
    path('playlist/create/', view=create_playlist, name="create_playlist"),
    path('playlist/<slug>/', view=playlist_detail, name="playlist_detail"),
    path('playlist/<slug>/delete/', view=delete_playlist, name="delete_playlist"),
    path('<slug>/delete/', view=delete_podcast, name="delete_podcast"),

    # podcasts like and unlike
    path("<slug>/", view=podcast_detail, name="podcast_detail"),
    path("<slug>/like/", view=podcast_like, name="podcast_like"),
    path("<slug>/unlike/", view=podcast_unlike, name="podcast_unlike"),
    path("<slug>/unfavorite/", view=remove_favorite, name="unfavorite"),
]
