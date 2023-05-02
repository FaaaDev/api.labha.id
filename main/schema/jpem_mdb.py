from ..shared.shared import ma

class JpemSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'jpem_code', 'jpem_name', 'jpem_ket')


jpem_schema = JpemSchema()
jpems_schema = JpemSchema(many=True)