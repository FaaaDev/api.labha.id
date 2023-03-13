from main.shared.shared import ma

class SaldoARSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'date', 'due_date', 'cus_id', 'type', 'nilai', 'user_id')


saar_schema = SaldoARSchema()
saars_schema = SaldoARSchema(many=True)