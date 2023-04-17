from ..shared.shared import ma

class CcostSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'ccost_code', 'ccost_name', 'ccost_ket')


ccost_schema = CcostSchema()
ccosts_schema = CcostSchema(many=True)