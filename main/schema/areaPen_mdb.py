from main.shared.shared import ma

class AreaPenSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'areaPen_code', 'areaPen_name', 'areaPen_ket')


areaPen_schema = AreaPenSchema()
areaPens_schema = AreaPenSchema(many=True)