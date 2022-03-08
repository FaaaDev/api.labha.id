from main.shared.shared import ma

class AttendanceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uid', 'date_checkin', 'image_in', 'location_in', 'date_checkout', 'location_out', 'image_out', 'location_out')


attendance_schema = AttendanceSchema()
attendaces_schema = AttendanceSchema(many=True)