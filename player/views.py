from django.views import generic
from rest_framework import generics
from .forms import TrackCreateForm, TrackSearchForm
from .models import Artist, Track
from .serializers import ArtistStatsSerializer, TrackCreateSerializer, TrackSerializer
from .utils import Utils

from rest_framework.response import Response

""" 
    There is no authentication added, as that wasn't in the requirements 

    If it would be a bigger application I could move api to the separate folder
"""


class ListTrack(generic.ListView):
    # List the first 100 most recently played tracks (most recent first)
    # Filter tracks by name

    model = Track
    template_name = 'track_list.html'
    paginate_by = 20
    form_class = TrackSearchForm

    def get_context_data(self, **kwargs):

        # if searching by name then return all results which matches search pattern,
        # otherwise return only 100 last played songs
        if bool(self.request.GET.get('name')):
            track = Track.objects.filter(name__icontains=self.request.GET.get('name'))
        else:
            track = Track.objects.order_by('-last_play')[:100]

        # convert track duration from seconds to minutes in nice readable format
        Utils.convert_seconds_to_printed_track_duration(track)

        # for pagination to work we need to pass object_list
        context = super().get_context_data(object_list=track, **kwargs)
        context['track_search_form'] = TrackSearchForm()
        return context


class DetailTrack(generic.DetailView):
    # Fetch a single track

    model = Track
    template_name = 'track_detail.html'


class CreateTrack(generic.CreateView):
    # Create a new track

    model = Track
    template_name = 'track_create.html'

    form_class = TrackCreateForm
    # return to the list of tracks
    success_url = "/"


class ListArtist(generic.ListView):
    model = Artist
    template_name = 'artist_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # List of artists contain artist name, the total number of tracks for that artist and their most recently played track.
        return super().get_context_data(object_list=Artist.get_artists_total_songs_recent_played_truck(self), **kwargs)


""" API """


class APITrackList(generics.ListAPIView):
    # List the first 100 most recently played tracks (most recent first)
    # Filter tracks by name

    serializer_class = TrackSerializer

    def get_queryset(self):
        if bool(self.request.GET.get('name')):
            return Track.objects.filter(name__icontains=self.request.GET.get('name'))
        else:
            return Track.objects.order_by('-last_play')[:100]


class APITrackDetail(generics.RetrieveAPIView):
    # Fetch a single track
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class APICreateTrack(generics.CreateAPIView):
    # Create a new track
    queryset = Track.objects.all()
    serializer_class = TrackCreateSerializer


class APIArtistList(generics.ListAPIView):
    def list(self, request):
        queryset = Artist.get_artists_total_songs_recent_played_truck(self)
        serializer = ArtistStatsSerializer(list(queryset), many=True)
        return Response(serializer.data)