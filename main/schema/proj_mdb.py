from ..shared.shared import ma

class ProjSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'proj_code', 'proj_name', 'proj_ket')


proj_schema = ProjSchema()
projs_schema = ProjSchema(many=True)