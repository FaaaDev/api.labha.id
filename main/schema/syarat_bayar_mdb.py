from ..shared.shared import ma

class RulesPaySchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'day', 'ket')


rpay_schema = RulesPaySchema()
rpays_schema = RulesPaySchema(many=True)