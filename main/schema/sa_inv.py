from ..shared.shared import ma

class SaldoInvSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'loc_id', 'prod_id', 'qty', 'nilai', 'total', 'user_id')


sainv_schema = SaldoInvSchema()
sainvs_schema = SaldoInvSchema(many=True)