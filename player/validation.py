from django.core.exceptions import ValidationError


class PlayerValidator:

    def validate_track_name(name):
        name = name.lower()
        if len(name) < 2:
            raise ValidationError("Track name '%s' should be at least 2 characters long" % name)
