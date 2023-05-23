from ..shared.shared import ma

class DivisiSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'desc')


division_schema = DivisiSchema()
divisions_schema = DivisiSchema(many=True)