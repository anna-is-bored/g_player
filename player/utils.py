import datetime


class Utils:

    def convert_seconds_to_printed_track_duration(tracks):
        for track in tracks:
            track.duration = datetime.timedelta(seconds=track.duration)
        return tracks

    def add_form_control_class(self):
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
