from ..shared.shared import ma

class JpelSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'jpel_code', 'jpel_name', 'jpel_ket')


jpel_schema = JpelSchema()
jpels_schema = JpelSchema(many=True)