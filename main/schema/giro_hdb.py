from main.shared.shared import ma

class GiroSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'giro_date', 'giro_num', 'bank_id', 'pay_code', 'pay_date', 'sup_id', 'value', 'accp_date', 'status')


giro_schema = GiroSchema()
giros_schema = GiroSchema(many=True)