from main.shared.shared import ma

class UnitSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'type', 'desc', 'active', 'qty', 'u_from', 'u_to')


unit_schema = UnitSchema()
units_schema = UnitSchema(many=True)