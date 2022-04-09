from main.shared.shared import ma

class ProjSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'keterangan')


proj_schema = ProjSchema()
projs_schema = ProjSchema(many=True)