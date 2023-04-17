from ..shared.shared import ma

class MsnSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'msn_code', 'msn_name', 'desc')


msn_schema = MsnSchema()
msns_schema = MsnSchema(many=True)