from ..shared.shared import ma

class MhdbSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'date', 'desc', 'imp', 'closing', 'user_id')


mhdb_schema = MhdbSchema()
mhdbs_schema = MhdbSchema(many=True)