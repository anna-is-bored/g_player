from rest_framework import serializers

from .models import Artist, Track
from .validation import PlayerValidator


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist

        fields = ('id','name', 'description', 'created_at')


class ArtistStatsSerializer(serializers.ModelSerializer):
    recently_played_track = serializers.CharField()
    total_number_of_tracks = serializers.CharField()

    class Meta:
        model = Artist
        fields = ('id','name', 'recently_played_track', 'total_number_of_tracks')
        read_only_fields = (
            'recently_played_track', 'total_number_of_tracks'
        )


class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, required=False)

    class Meta:
        model = Track
        fields = ['name', 'last_play', 'artist', 'duration', 'created_at']


class TrackCreateSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TrackCreateSerializer, self).__init__(*args, **kwargs)
        # basic validation, more validation could be added, for example prevent duplication
        self.fields['name'].validators.append(PlayerValidator.validate_track_name)

    class Meta:
        model = Track
        fields = ['name', 'duration', 'artist']