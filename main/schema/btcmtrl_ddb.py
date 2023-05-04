from main.shared.shared import ma

class BtcmtrlSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'btc_id', 'prod_id', 'unit_id', 'qty', 'qty_f', 'price', 't_price')


bmtrl_schema = BtcmtrlSchema()
bmtrls_schema = BtcmtrlSchema(many=True)