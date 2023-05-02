from ..shared.shared import ma

class FmtrlSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'orm_id', 'prod_id', 'unit_id', 'qty', 'price')


fmtrl_schema = FmtrlSchema()
fmtrls_schema = FmtrlSchema(many=True)