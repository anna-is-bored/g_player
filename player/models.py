from django.db import models


class Artist(models.Model):
    """ Model representing an artist.
       I could add more fields in here like for example a country (but then I would have to create model country)
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    def get_artists_total_songs_recent_played_truck(self):
        # the next step is to make it in more django ORMish way
        return Artist.objects.raw('SELECT player_artist.id, player_artist.name AS artist_name, '
                                      '(SELECT name FROM player_track WHERE artist_id = player_artist.id ORDER BY last_play DESC LIMIT 1) AS recently_played_track, '
                                      '(SELECT count(*) FROM player_track WHERE artist_id = player_artist.id GROUP BY artist_id) AS total_number_of_tracks '
                                      'FROM player_artist')


class Track(models.Model):
    """ Model representing a track."""

    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    duration = models.SmallIntegerField("Track Duration In Seconds")
    last_play = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', ]),
        ]

