from ..shared.shared import ma

class LocationSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'address', 'desc')


loct_schema = LocationSchema()
locts_schema = LocationSchema(many=True)