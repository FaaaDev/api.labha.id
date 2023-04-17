from ..shared.shared import ma

class SaldoAPSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'date', 'due_date', 'sup_id', 'type', 'nilai', 'user_id')


saap_schema = SaldoAPSchema()
saaps_schema = SaldoAPSchema(many=True)