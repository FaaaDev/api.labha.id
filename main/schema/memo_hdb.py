from main.shared.shared import ma

class MhdbSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'date', 'desc')


mhdb_schema = MhdbSchema()
mhdbs_schema = MhdbSchema(many=True)