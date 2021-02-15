from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('artist', views.ListArtist.as_view(), name="artist_list"),
    path('', views.ListTrack.as_view(), name="track_list"),
    path('track/<int:pk>', views.DetailTrack.as_view(), name="track_detail"),
    path('track/create', views.CreateTrack.as_view(), name="track_create"),

    path('api/artist', views.APIArtistList.as_view()),
    path('api/track', views.APITrackList.as_view()),
    path('api/track/<int:pk>', views.APITrackDetail.as_view()),
    path('api/track/create', views.APICreateTrack.as_view()),
]
