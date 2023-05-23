from main.shared.shared import ma

class BtcprodSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'btc_id', 'prod_id', 'unit_id', 'loc_id', 'qty', 'qty_f', 'aloc')


bprod_schema = BtcprodSchema()
bprods_schema = BtcprodSchema(many=True)