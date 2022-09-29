from main.shared.shared import ma

class GiroIncSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'giro_date', 'giro_num', 'bank_id', 'pay_code', 'pay_date', 'cus_id', 'value', 'status')


grinc_schema = GiroIncSchema()
grincs_schema = GiroIncSchema(many=True)